import json
import math
import os
import pickle
import re
from collections import Counter
from datetime import datetime, timezone
from preprocess import CJK_RE


def _safe_parse_iso(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


def _age_days(created_at):
    dt = _safe_parse_iso(created_at)
    if not dt:
        return 3650.0
    now = datetime.now(tz=timezone.utc)
    return max(0.0, (now - dt.astimezone(timezone.utc)).total_seconds() / 86400.0)


def _normalize_scores(score_map):
    if not score_map:
        return {}
    vals = list(score_map.values())
    lo, hi = min(vals), max(vals)
    if hi - lo < 1e-9:
        return {k: 1.0 for k in score_map}
    return {k: (v - lo) / (hi - lo) for k, v in score_map.items()}


def _tokenize(text):
    text = (text or "").lower()
    latin = re.findall(r"[a-z0-9_]+", text)
    cjk = CJK_RE.findall(text)
    return latin + cjk


def _bm25_search(query, bm25_payload, top_k=40):
    docs = bm25_payload.get("tokenized_docs", [])
    idf = bm25_payload.get("idf", {})
    avgdl = bm25_payload.get("avgdl", 1.0) or 1.0
    k1 = bm25_payload.get("k1", 1.5)
    b = bm25_payload.get("b", 0.75)

    q_terms = _tokenize(query)
    if not q_terms:
        return {}

    scores = {}
    for i, doc in enumerate(docs):
        if not doc:
            continue
        tf = Counter(doc)
        dl = len(doc)
        score = 0.0
        for t in q_terms:
            if t not in tf:
                continue
            term_idf = idf.get(t, 0.0)
            f = tf[t]
            denom = f + k1 * (1 - b + b * dl / avgdl)
            score += term_idf * (f * (k1 + 1)) / (denom + 1e-9)
        if score > 0:
            scores[i] = score

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return dict(ranked)


def _load_meta(meta_path, n_fallback=0):
    if not os.path.exists(meta_path):
        return [{
            "id": i,
            "text": "",
            "source_file": "unknown",
            "source_type": "unknown",
            "created_at": None,
            "scope": "global",
            "importance": 0.5,
            "token_len": 0,
            "tags": [],
        } for i in range(n_fallback)]

    rows = []
    with open(meta_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def _importance_multiplier(importance: float) -> float:
    # importance in [0,1], default 0.5 -> x1.0
    imp = min(1.0, max(0.0, float(importance)))
    return 0.7 + 0.6 * imp


def _length_norm(token_len: int, anchor: int = 300, alpha: float = 0.35) -> float:
    l = max(1, int(token_len))
    if l <= anchor:
        return 1.0
    return 1.0 / (1.0 + alpha * math.log2(l / float(anchor)))


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _norm(a):
    return math.sqrt(sum(x * x for x in a)) + 1e-9


def _cosine(a, b):
    return _dot(a, b) / (_norm(a) * _norm(b))


def _mmr_diversify(items, emb_lookup, top_k, mmr_lambda=0.75, sim_threshold=0.88):
    """
    簡化版 MMR：避免 top 結果高度重複。
    """
    if not items:
        return []

    selected = []
    remaining = items[:]

    while remaining and len(selected) < top_k:
        if not selected:
            selected.append(remaining.pop(0))
            continue

        best_idx = 0
        best_mmr = -1e9
        for i, cand in enumerate(remaining):
            cand_id = cand.get("_id")
            cand_emb = emb_lookup.get(cand_id)
            if cand_emb is None:
                mmr_score = cand["score"]
            else:
                max_sim = 0.0
                for sel in selected:
                    sel_emb = emb_lookup.get(sel.get("_id"))
                    if sel_emb is None:
                        continue
                    max_sim = max(max_sim, _cosine(cand_emb, sel_emb))

                # 高度相似直接重罰
                penalty = 0.4 if max_sim >= sim_threshold else 0.0
                mmr_score = mmr_lambda * cand["score"] - (1 - mmr_lambda) * max_sim - penalty

            if mmr_score > best_mmr:
                best_mmr = mmr_score
                best_idx = i

        selected.append(remaining.pop(best_idx))

    return selected


def hybrid_search(query, *, model, index, sentences, top_k=3, scope=None, include_debug=False):
    """
    混合檢索：Vector + BM25 + Recency + Importance + LengthNorm + Hard Min + MMR-lite。
    若 BM25/metadata 不可用，回退 vector-only。
    """
    # env tunables
    vector_weight = float(os.getenv("MEMORY_PRO_VECTOR_WEIGHT", "0.7"))
    bm25_weight = float(os.getenv("MEMORY_PRO_BM25_WEIGHT", "0.3"))
    hard_min_score = float(os.getenv("MEMORY_PRO_HARD_MIN_SCORE", "0.30"))
    dual_hit_bonus = float(os.getenv("MEMORY_PRO_DUAL_HIT_BONUS", "0.03"))
    recency_half_life_days = float(os.getenv("MEMORY_PRO_RECENCY_HALF_LIFE_DAYS", "14"))
    recency_weight = float(os.getenv("MEMORY_PRO_RECENCY_WEIGHT", "0.08"))
    length_norm_anchor = int(os.getenv("MEMORY_PRO_LENGTH_NORM_ANCHOR", "300"))
    length_norm_alpha = float(os.getenv("MEMORY_PRO_LENGTH_NORM_ALPHA", "0.35"))
    mmr_lambda = float(os.getenv("MEMORY_PRO_MMR_LAMBDA", "0.75"))
    mmr_sim_threshold = float(os.getenv("MEMORY_PRO_MMR_SIM_THRESHOLD", "0.88"))
    enable_mmr = os.getenv("MEMORY_PRO_ENABLE_MMR", "false").lower() in ("1", "true", "yes", "on")
    scope_strict = os.getenv("MEMORY_PRO_SCOPE_STRICT", "false").lower() in ("1", "true", "yes", "on")

    candidate_pool = max(20, int(os.getenv("MEMORY_PRO_CANDIDATE_POOL", "40")))

    # vector candidates
    q_emb = model.encode([query])
    # 與索引向量同樣做 L2 normalize，保持分數一致性
    try:
        import faiss
        faiss.normalize_L2(q_emb)
    except Exception:
        pass
    distances, indices = index.search(q_emb, candidate_pool)

    vector_raw = {}
    for dist, idx in zip(distances[0], indices[0]):
        if idx == -1:
            continue
        if 0 <= idx < len(sentences):
            # Smaller L2 dist is better -> invert for ranking
            vector_raw[idx] = float(1.0 / (1.0 + max(0.0, float(dist))))

    # load bm25 payload (optional)
    bm25_path = os.getenv("MEMORY_PRO_BM25_PATH", "bm25_corpus.pkl")
    bm25_raw = {}
    if os.path.exists(bm25_path):
        try:
            with open(bm25_path, "rb") as f:
                bm25_payload = pickle.load(f)
            bm25_raw = _bm25_search(query, bm25_payload, top_k=candidate_pool)
        except Exception:
            bm25_raw = {}

    # normalize both channels
    vector_norm = _normalize_scores(vector_raw)
    bm25_norm = _normalize_scores(bm25_raw)

    # metadata
    meta_path = os.getenv("MEMORY_PRO_META_PATH", "memory_meta.jsonl")
    meta_rows = _load_meta(meta_path, n_fallback=len(sentences))

    # fuse candidates
    all_ids = set(vector_norm.keys()) | set(bm25_norm.keys())
    fused = []

    # prepare embedding lookup for MMR-lite diversity (optional; disabled by default for latency)
    emb_lookup = {}
    if enable_mmr:
        try:
            cand_ids_sorted = sorted([i for i in all_ids if 0 <= i < len(sentences)])
            if cand_ids_sorted:
                cand_texts = [sentences[i] for i in cand_ids_sorted]
                cand_embs = model.encode(cand_texts)
                for i, emb in zip(cand_ids_sorted, cand_embs):
                    emb_lookup[i] = emb.tolist() if hasattr(emb, "tolist") else list(emb)
        except Exception:
            emb_lookup = {}

    for idx in all_ids:
        if not (0 <= idx < len(sentences)):
            continue
        meta = meta_rows[idx] if idx < len(meta_rows) else {}

        # scope filter
        row_scope = (meta.get("scope") or "global")
        if scope:
            if scope_strict:
                if row_scope != scope:
                    continue
            else:
                # non-strict: requested scope + global fallback
                if scope != "global" and row_scope not in ("global", scope):
                    continue

        base = vector_weight * vector_norm.get(idx, 0.0) + bm25_weight * bm25_norm.get(idx, 0.0)
        if idx in vector_norm and idx in bm25_norm:
            base += dual_hit_bonus

        # recency boost
        age = _age_days(meta.get("created_at"))
        recency = math.exp(-age / max(0.1, recency_half_life_days))

        # importance + length normalization
        importance = float(meta.get("importance", 0.5))
        token_len = int(meta.get("token_len", len(sentences[idx].split())))
        imp_mul = _importance_multiplier(importance)
        len_mul = _length_norm(token_len, anchor=length_norm_anchor, alpha=length_norm_alpha)

        score = (base + recency_weight * recency) * imp_mul * len_mul

        if score < hard_min_score:
            continue

        item = {
            "_id": int(idx),
            "score": float(score),
            "sentence": sentences[idx],
        }
        if include_debug:
            item["debug"] = {
                "id": int(idx),
                "vector": vector_norm.get(idx, 0.0),
                "bm25": bm25_norm.get(idx, 0.0),
                "recency": recency,
                "importance": importance,
                "importance_mul": imp_mul,
                "length_mul": len_mul,
                "scope": row_scope,
                "scope_strict": scope_strict,
                "source_file": meta.get("source_file"),
            }
        fused.append(item)

    fused.sort(key=lambda x: x["score"], reverse=True)

    # Optional rerank (Phase 3): timeout-safe + fallback
    rerank_meta = {"applied": False}
    try:
        from rerank import should_rerank, rerank_candidates
        if should_rerank(query):
            fused, rerank_meta = rerank_candidates(query, fused)
    except Exception:
        # fail-open: keep original fused ranking
        rerank_meta = {"applied": False}

    if enable_mmr:
        fused = _mmr_diversify(fused, emb_lookup, top_k=top_k, mmr_lambda=mmr_lambda, sim_threshold=mmr_sim_threshold)

    # attach rerank metadata to debug (if enabled)
    if include_debug and rerank_meta.get("applied"):
        for item in fused:
            if "debug" in item:
                item["debug"]["rerank"] = rerank_meta
                if "_debug_rerank" in item:
                    item["debug"]["rerank_item"] = item.get("_debug_rerank")

    # graceful fallback if hybrid too strict or bm25/meta missing
    if not fused:
        fallback = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            if 0 <= idx < len(sentences):
                fallback.append({
                    "score": float(1.0 / (1.0 + max(0.0, float(dist)))),
                    "sentence": sentences[idx],
                })
        return fallback[:top_k]

    out = []
    for item in fused[:top_k]:
        clean = {"score": item["score"], "sentence": item["sentence"]}
        if "debug" in item:
            clean["debug"] = item["debug"]
        out.append(clean)
    return out
