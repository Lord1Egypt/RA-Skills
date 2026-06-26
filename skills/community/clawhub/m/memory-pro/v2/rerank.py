import os
import time
import hashlib
import requests


def _env_bool(name: str, default: bool = False) -> bool:
    v = os.getenv(name, str(default)).lower()
    return v in ("1", "true", "yes", "on")


def _sample_hit(query: str) -> bool:
    """
    灰度抽樣：按 query hash 做穩定抽樣。
    MEMORY_PRO_RERANK_SAMPLE_PCT=100 代表全量。
    """
    pct = int(os.getenv("MEMORY_PRO_RERANK_SAMPLE_PCT", "100"))
    pct = max(0, min(100, pct))
    if pct >= 100:
        return True
    if pct <= 0:
        return False
    h = int(hashlib.md5(query.encode("utf-8")).hexdigest(), 16) % 100
    return h < pct


def should_rerank(query: str) -> bool:
    if not _env_bool("MEMORY_PRO_ENABLE_RERANK", False):
        return False
    return _sample_hit(query)


def rerank_candidates(query: str, candidates: list):
    """
    回傳 (reranked_candidates, meta)
    - candidates: [{score, sentence, ...}, ...]
    - 失敗時丟 Exception，呼叫方負責 fallback
    """
    provider = os.getenv("MEMORY_PRO_RERANK_PROVIDER", "none").lower()
    timeout_ms = int(os.getenv("MEMORY_PRO_RERANK_TIMEOUT_MS", "2500"))
    topn = int(os.getenv("MEMORY_PRO_RERANK_TOPN", "20"))
    blend = float(os.getenv("MEMORY_PRO_RERANK_BLEND", "0.6"))

    blend = max(0.0, min(1.0, blend))
    topn = max(1, min(topn, len(candidates)))

    work = candidates[:topn]
    if not work:
        return candidates, {"applied": False, "reason": "no_candidates"}

    t0 = time.perf_counter()

    if provider == "jina":
        endpoint = os.getenv("MEMORY_PRO_RERANK_ENDPOINT", "https://api.jina.ai/v1/rerank")
        api_key = os.getenv("MEMORY_PRO_RERANK_API_KEY", "")
        model = os.getenv("MEMORY_PRO_RERANK_MODEL", "jina-reranker-v2-base-multilingual")

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model,
            "query": query,
            "documents": [c.get("sentence", "") for c in work],
            "top_n": topn,
        }
        r = requests.post(endpoint, json=payload, headers=headers, timeout=timeout_ms / 1000)
        r.raise_for_status()
        data = r.json()
        # jina 常見格式: {results:[{index,relevance_score},...]}
        rows = data.get("results", [])
        rerank_map = {int(x.get("index", -1)): float(x.get("relevance_score", 0.0)) for x in rows if int(x.get("index", -1)) >= 0}

    elif provider == "openai_compatible":
        endpoint = os.getenv("MEMORY_PRO_RERANK_ENDPOINT", "")
        api_key = os.getenv("MEMORY_PRO_RERANK_API_KEY", "")
        model = os.getenv("MEMORY_PRO_RERANK_MODEL", "")
        if not endpoint or not model:
            raise RuntimeError("openai_compatible rerank requires ENDPOINT and MODEL")

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        payload = {
            "model": model,
            "query": query,
            "documents": [c.get("sentence", "") for c in work],
            "top_n": topn,
        }
        r = requests.post(endpoint, json=payload, headers=headers, timeout=timeout_ms / 1000)
        r.raise_for_status()
        data = r.json()
        rows = data.get("results", data.get("data", []))
        rerank_map = {}
        for x in rows:
            idx = int(x.get("index", x.get("id", -1)))
            if idx < 0:
                continue
            score = float(x.get("relevance_score", x.get("score", 0.0)))
            rerank_map[idx] = score

    else:
        raise RuntimeError(f"rerank provider not enabled: {provider}")

    # normalize rerank scores to [0,1]
    vals = list(rerank_map.values())
    if vals:
        lo, hi = min(vals), max(vals)
        if hi - lo < 1e-9:
            rerank_norm = {k: 1.0 for k in rerank_map}
        else:
            rerank_norm = {k: (v - lo) / (hi - lo) for k, v in rerank_map.items()}
    else:
        rerank_norm = {}

    for i, c in enumerate(work):
        original = float(c.get("score", 0.0))
        rr = float(rerank_norm.get(i, 0.0))
        c["score"] = blend * rr + (1.0 - blend) * original
        c.setdefault("_debug_rerank", {})
        c["_debug_rerank"].update({
            "original_score": original,
            "rerank_score": rr,
            "blend": blend,
        })

    work.sort(key=lambda x: x.get("score", 0.0), reverse=True)
    merged = work + candidates[topn:]

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return merged, {
        "applied": True,
        "provider": provider,
        "topn": topn,
        "elapsed_ms": round(elapsed_ms, 2),
        "blend": blend,
    }
