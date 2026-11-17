#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
literature_probe.py — In-skill literature dedup probe for meta-analysis topic selection.

WHY THIS EXISTS
---------------
The meta-analysis skill must be **self-contained** for its core upstream gate
(topic selection / novelty dedup). It must NOT delegate every literature need
to another skill, and it must NOT fall back to "search-query templates only"
(the template-only path was the prior failure mode — it produced no real
evidence). This module runs a REAL, dependency-free probe against Europe PMC
(https://www.ebi.ac.uk/europepmc/webservices/rest/search) — the REST front-end
to MEDLINE + PubMed Central — and returns live hit counts + top titles for the
Cochrane and PubMed layers of the three-layer dedup.

PROVENANCE
----------
Field mapping and query syntax are adapted from ct-literature's verified
`adapters/fetch_europepmc.py` (Europe PMC fetcher) and its `http_utils`
retry/backoff policy. We re-implement a minimal, standalone version here so
meta-analysis has zero cross-skill import dependency and stays self-contained.
Key facts confirmed against the live API (2026-08-26):
  - Cochrane reviews live in journal "The Cochrane database of systematic reviews";
    the reliable filter restricts to that journal via
    `AND (JOURNAL:"The Cochrane database of systematic reviews")`
    (verified accurate; NOT `PUBLICATION_TYPE:"Cochrane Reviews"` which returns 0
    — the pubType value is "Systematic Review", not "Cochrane Reviews"; and NOT a
    bare quoted phrase, which overcounts papers that merely cite Cochrane).
  - Year filter field is `PUB_YEAR:[lo TO hi]`.
  - `resultType=core` is required to populate journalInfo / pubTypeList.

Zero third-party dependencies — standard library only (urllib, json, re, time,
datetime). No confidential data input; reads only public literature.
"""
import argparse
import datetime
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
UA = "meta-analysis-skill/2.1.1"

# Cochrane Database of Systematic Reviews — restrict to the journal itself
# (verified 2026-08-26: `JOURNAL:"The Cochrane database of systematic reviews"`
# returns accurate counts; the looser quoted-phrase match overcounts because it
# also catches papers that merely *cite* Cochrane). All sample journals matched
# by this filter are true Cochrane reviews.
COCHRANE_JOURNAL_FILTER = '(JOURNAL:"The Cochrane database of systematic reviews")'
COCHRANE_JOURNAL_MARK = "cochrane database of systematic reviews"


def _has_cjk(text):
    """True 若 text 含中日韩（CJK）字符。Europe PMC 索引的是英文摘要，
    纯中文查询串几乎必然 0 命中——调用方必须先翻译或要求提供英文检索词。
    （2026-09-22 补：选题探针此前直接把中文主题送 Europe PMC，导致「该选题无文献」
    的误报；这里用于提前拦截并改用英文检索词。）"""
    if not text:
        return False
    return bool(re.search(r"[\u3400-\u9fff\uf900-\ufaff\uff00-\uffef\u3040-\u30ff]", text))


def _get_json(url, timeout=30, max_retries=3, backoff=2.0):
    """GET `url`, parse JSON, with unified retry/backoff.

    Mirrors ct-literature http_utils policy, minimal form:
      - HTTP 429: honor `Retry-After` header; else exponential backoff.
      - 5xx / network / timeout: exponential backoff.
      - other 4xx: non-retryable, raised immediately.
    Raises RuntimeError after retries exhausted.
    """
    last = None
    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                ra = e.headers.get("Retry-After")
                wait = float(ra) if ra else backoff ** (attempt - 1)
                if attempt < max_retries:
                    time.sleep(wait)
                    continue
                last = e
                break
            if 500 <= e.code < 600:
                if attempt < max_retries:
                    time.sleep(backoff ** (attempt - 1))
                    continue
                last = e
                break
            raise  # 4xx other than 429 → non-retryable
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            if attempt < max_retries:
                time.sleep(backoff ** (attempt - 1))
                continue
            last = e
            break
    raise RuntimeError("Europe PMC request failed after %d retries: %s" % (max_retries, last))


def _strip_html(s):
    if not s:
        return s
    return re.sub(r"<[^>]+>", "", s)


def _extract(rec):
    """Normalize one Europe PMC record. Field names per fetch_europepmc._extract."""
    ji = rec.get("journalInfo") or {}
    journal = (ji.get("journal") or {}).get("title")
    pmid = rec.get("pmid")
    doi = rec.get("doi")
    year = None
    if rec.get("pubYear") and str(rec.get("pubYear")).isdigit():
        year = int(rec["pubYear"])
    ftl = rec.get("fullTextUrlList") or {}
    ft_urls = ftl.get("fullTextUrl") or []
    fulltext_url = ft_urls[0].get("url") if ft_urls else None
    title = _strip_html(rec.get("title") or "")
    pub_types = (rec.get("pubTypeList") or {}).get("pubType", []) or []
    cited = rec.get("citedByCount")
    return {
        "id": rec.get("id") or pmid,
        "pmid": pmid,
        "doi": doi,
        "title": title,
        "year": year,
        "journal": journal,
        "pub_types": pub_types,
        "cited_by_count": int(cited) if isinstance(cited, int) else 0,
        "url": fulltext_url or doi or None,
        "is_cochrane": bool(journal and COCHRANE_JOURNAL_MARK in journal.lower()),
    }


def _build_query(topic, review_type, year_from, year_to, cochrane_only):
    q = topic
    if cochrane_only:
        q += " AND " + COCHRANE_JOURNAL_FILTER
    else:
        if review_type == "meta-analysis":
            q += " AND meta-analysis"
        elif review_type == "systematic-review":
            q += " AND (systematic review OR meta-analysis)"
        elif review_type == "rct":
            q += " AND randomized controlled trial"
    if year_from or year_to:
        lo = str(year_from) if year_from else "1900"
        hi = str(year_to) if year_to else "3000"
        q += " AND (PUB_YEAR:[%s TO %s])" % (lo, hi)
    return q


def _build_ct_handoff(topic, layer, year_from=None, year_to=None):
    """Build the ct-literature command that reproduces this probe's search
    with full retrieval machinery (verify / evidence_log / merge / Excel /
    HTML / PRISMA). This is the seamless handoff from meta-analysis topic
    selection -> comprehensive literature retrieval.

    Both skills use the SAME Europe PMC journal-filter string for Cochrane,
    so the Cochrane hit counts match exactly; the only difference is depth
    (quick dedup count here vs. full records + anti-hallucination there).
    """
    _q = json.dumps(topic, ensure_ascii=False)  # double-quoted, shell-safe
    if layer == "cochrane":
        cmd = ("python scripts/ct_literature.py --topic %s --cochrane "
               "--with-europepmc --run --out-dir ./cochrane_out" % _q)
    else:
        yf = year_from if year_from else (datetime.date.today().year - 5)
        cmd = ("python scripts/ct_literature.py --topic %s --review-type "
               "systematic-review --year-from %s --with-europepmc --run "
               "--out-dir ./pubmed_out" % (_q, yf))
    return {
        "action": "run ct-literature for full retrieval",
        "command": cmd,
        "note": ("本探针只是选题去重的快速检查（真实命中数 + 前几篇标题），并非全面文献检索。"
                 "需要完整检索（反幻觉验证 / 证据溯源 / 合并去重 / Excel+HTML 报告 / PRISMA 筛选）时，"
                 "请先使用 ct-literature 技能——先 cd 到 ct-literature 技能目录再执行上面的命令。"),
        "same_filter": ("两技能使用同一 Europe PMC 期刊过滤串 "
                        '`(JOURNAL:"The Cochrane database of systematic reviews")`，'
                        "Cochrane 层计数完全一致，可无缝衔接。"),
    }


def probe(topic, layer="pubmed", review_type="systematic-review",
          year_from=None, year_to=None, max_results=10, topic_en=None):
    """Probe one dedup layer against Europe PMC.

    Args:
        topic: free-text PICO-derived query (e.g. "PD-1 inhibitors NSCLC 2nd line").
               作为面向用户的展示主题；实际检索串优先用 `topic_en`。
        layer: "cochrane" (Cochrane Library via Europe PMC) or "pubmed"
               (published SR/MA on PubMed/MEDLINE).
        review_type: for pubmed layer — meta-analysis | systematic-review | rct.
        year_from / year_to: inclusive publication-year bounds (None = open).
        max_results: cap on returned work records (hit_count is always the
                     full API total, not capped).
        topic_en: 英文检索词（可选）。提供时用于构建 Europe PMC 查询串——
           Europe PMC 索引英文摘要，中文主题直送几乎必 0 命中，故英文优先。

    Returns:
        dict with keys: layer, query, hit_count (int|None), cochrane_count (int),
        works (list), error (str|None), ct_handoff (dict). On request failure,
        hit_count=None and error is set — callers degrade gracefully (do NOT
        crash the workflow).
    """
    cochrane_only = (layer == "cochrane")
    # 英文检索词优先；缺失则退回原始主题（中文主题会命中极低，由调用方警示）
    q_topic = (topic_en or "").strip() or topic
    q = _build_query(q_topic, review_type, year_from, year_to, cochrane_only)
    collected = []
    hit_count = None
    page = 1
    per = 25
    while len(collected) < max_results:
        params = {
            "query": q,
            "format": "json",
            "resultType": "core",
            "pageSize": min(per, max_results - len(collected)),
            "page": page,
        }
        url = BASE + "?" + urllib.parse.urlencode(params)
        try:
            j = _get_json(url)
        except Exception as e:  # noqa: BLE001 - degrade, don't abort workflow
            return {"layer": layer, "query": q, "hit_count": None,
                    "cochrane_count": 0, "works": [], "error": str(e),
                    "ct_handoff": _build_ct_handoff(q_topic, layer, year_from, year_to)}
        if hit_count is None:
            hit_count = j.get("hitCount")
        results = (j.get("resultList") or {}).get("result", [])
        if not results:
            break
        for rec in results:
            collected.append(_extract(rec))
        if len(results) < per:
            break
        page += 1
        time.sleep(0.3)

    # For the pubmed layer, also count any Cochrane reviews that surfaced
    # (post-filter, robust against query-term variance).
    cochrane_count = sum(1 for w in collected if w.get("is_cochrane"))
    return {
        "layer": layer,
        "query": q,
        "hit_count": hit_count,
        "cochrane_count": cochrane_count,
        "works": collected[:max_results],
        "error": None,
        "ct_handoff": _build_ct_handoff(q_topic, layer, year_from, year_to),
    }


def dedup_probe(topic, year_from=None, year_to=None, max_results=8,
                cochrane_window_years=0, topic_en=None):
    """Run the self-contained two-layer dedup probe (Cochrane + PubMed SR/MA).

    This is the DEFAULT Stage-4 evidence source for topic selection — it runs
    live and returns real hit counts, so the novelty ranking (R7) is grounded
    in actual literature, not templates.

    Args:
        topic: PICO-derived query string.
        year_from / year_to: bounds for the PubMed layer (default: last 5 years
                             if both None).
        max_results: top titles to return per layer.
        cochrane_window_years: if >0, restrict Cochrane layer to the last N
                               years (default 0 = no year bound on Cochrane).

    Returns:
        dict: topic, layers {cochrane, pubmed_meta}, summary (human-readable
        dedup signal), any_error (bool).
    """
    if year_from is None and year_to is None:
        year_from = datetime.date.today().year - 5
    c_year_from = None
    if cochrane_window_years and cochrane_window_years > 0:
        c_year_from = datetime.date.today().year - cochrane_window_years

    # 中文主题 + 无英文检索词 → 自动翻译（2026-09-22 用户纠正）。
    # 技能（Agent）上下文里 LLM 在场、翻译是天然能力；网页端服务是独立进程、
    # Agent 不在回路里，此前只能让用户手填英文题名——等于把机器该干的活推给用户。
    # 现补上 `topic_translate`（复用 WorkBuddy 本机 OpenAI 兼容端点），网页端与
    # 技能上下文行为一致；只有**自动翻译也不可用**时才回退到索要英文检索词。
    _en = (topic_en or "").strip()
    auto_translated = False
    trans_error = None
    if not _en and _has_cjk(topic):
        try:
            from topic_translate import translate_to_english
            _en = (translate_to_english(topic) or "").strip()
        except Exception as e:  # noqa: BLE001 - 翻译不可用不能中断探针
            trans_error = "%s: %s" % (type(e).__name__, e)
        auto_translated = bool(_en)
    if _en:
        topic_en = _en

    # 自动翻译仍拿不到英文 → 拦下并显式索要（跑下去只会得到误导性的
    # 「Cochrane 0 篇 = 新颖选题」假信号，还白费一次请求与限流额度）。
    cjk_untranslated = _has_cjk(topic) and not (topic_en or "").strip()
    if cjk_untranslated:
        _why = ("自动翻译不可用（%s）" % trans_error) if trans_error else "未能自动翻译出合规的英文检索词"
        notice = ("⚠ 研究主题为中文，但 Europe PMC 索引的是英文摘要；%s，"
                  "故未能以英文检索，中文直检几乎必然 0 命中（并非真无文献）。\n"
                  "处理：在上方「英文检索词」框填入本主题的英文表达（如 "
                  "“SGLT2 inhibitors chronic kidney disease renal protection cardiovascular outcomes”）"
                  "后重新点「先帮我选题」即可看到真实命中。" % _why)
        _blocked = lambda layer, yf, yt: {
            "layer": layer, "query": None, "hit_count": None,
            "cochrane_count": 0, "works": [], "error": None,
            "untranslated": True,
            "ct_handoff": _build_ct_handoff(topic, layer, yf, yt),
        }
        return {
            "topic": topic,
            "topic_en": None,
            "cjk_untranslated": True,
            "auto_translated": False,
            "trans_error": trans_error,
            "notice": notice,
            "layers": {
                "cochrane": _blocked("cochrane", c_year_from, year_to),
                "pubmed_meta": _blocked("pubmed", year_from, year_to),
            },
            "summary": "中文主题未能自动翻译为英文且未提供英文检索词，探针已跳过执行"
                       "（避免以中文字符误检为 0 命中）。",
            "any_error": False,
            "ct_handoff": {
                "note": ("本探针只是选题去重的快速检查（真实命中数 + 前几篇标题），并非全面文献检索。"
                         "需要完整检索（反幻觉验证 / 证据溯源 / 合并去重 / Excel+HTML 报告 / PRISMA 筛选）时，"
                         "请先使用 ct-literature 技能。"),
                "same_filter": ("两技能使用同一 Europe PMC 期刊过滤串 "
                                '`(JOURNAL:"The Cochrane database of systematic reviews")`，'
                                "Cochrane 层计数完全一致，可无缝衔接。"),
                "cochrane": _build_ct_handoff(topic, "cochrane", c_year_from, year_to),
                "pubmed": _build_ct_handoff(topic, "pubmed", year_from, year_to),
                "cochrane_query": None,
                "pubmed_query": None,
            },
        }

    cochrane = probe(topic, layer="cochrane", year_from=c_year_from,
                     year_to=year_to, max_results=max_results, topic_en=topic_en)
    pubmed = probe(topic, layer="pubmed", review_type="systematic-review",
                   year_from=year_from, year_to=year_to, max_results=max_results,
                   topic_en=topic_en)

    parts = []
    if cochrane.get("hit_count") is not None:
        parts.append("Cochrane: %s review(s) on this topic" % cochrane["hit_count"])
    else:
        parts.append("Cochrane: probe unavailable")
    if pubmed.get("hit_count") is not None:
        parts.append("PubMed SR/MA (last %s y): %s" % (
            (datetime.date.today().year - (year_from or datetime.date.today().year)),
            pubmed["hit_count"]))
    else:
        parts.append("PubMed SR/MA: probe unavailable")
    summary = "; ".join(parts)

    _en_final = (topic_en or "").strip() or None
    _notice = None
    if auto_translated:
        _notice = ("ℹ 主题为中文，已自动翻译为英文检索式检索 Europe PMC："
                   "「%s」。如需更正，可在下方修订后重查。" % _en_final)
    return {
        "topic": topic,
        "topic_en": _en_final,
        "topic_en_source": "auto" if auto_translated else ("user" if _en_final else None),
        "auto_translated": auto_translated,
        "trans_error": trans_error,
        "cjk_untranslated": False,
        "notice": _notice,
        "layers": {"cochrane": cochrane, "pubmed_meta": pubmed},
        "summary": summary,
        "any_error": bool(cochrane.get("error") or pubmed.get("error")),
        "ct_handoff": {
            "note": ("本探针只是选题去重的快速检查（真实命中数 + 前几篇标题），并非全面文献检索。"
                     "需要完整检索（反幻觉验证 / 证据溯源 / 合并去重 / Excel+HTML 报告 / PRISMA 筛选）时，"
                     "请先使用 ct-literature 技能。"),
            "same_filter": ("两技能使用同一 Europe PMC 期刊过滤串 "
                            '`(JOURNAL:"The Cochrane database of systematic reviews")`，'
                            "Cochrane 层计数完全一致，可无缝衔接。"),
            "cochrane": _build_ct_handoff(topic, "cochrane", c_year_from, year_to),
            "pubmed": _build_ct_handoff(topic, "pubmed", year_from, year_to),
            "cochrane_query": cochrane.get("query"),
            "pubmed_query": pubmed.get("query"),
        },
    }


def _parse_authors(author_string):
    """Split Europe PMC `authorString` ("Mocking RJ, Harmsen I, Assies J.") into
    block_c._author_label-compatible records: [{"family": "Mocking"}, ...].

    Only the surname is taken (initials dropped) because in-text citations and
    reference lists of the manuscript use `Surname (Year)`.
    """
    if not isinstance(author_string, str) or not author_string.strip():
        return []
    out = []
    for chunk in author_string.split(","):
        chunk = chunk.strip().rstrip(".")
        if not chunk:
            continue
        # "Mocking RJ" -> family "Mocking", initials "RJ"
        parts = chunk.split()
        fam = parts[0] if parts else chunk
        ini = "".join(parts[1:])[:8]
        rec = {"family": fam}
        if ini:
            rec["initials"] = ini
        out.append(rec)
    return out


def _infer_study_type(pub_types):
    """Map Europe PMC pubType list -> short design label used by block_c._plur()."""
    pt = " ".join(str(x).lower() for x in (pub_types or []))
    if "meta-analysis" in pt:
        return "meta-analysis"
    if "systematic review" in pt:
        return "systematic review"
    if "randomized controlled trial" in pt:
        return "randomized controlled trial"
    if "clinical trial" in pt:
        return "clinical trial"
    if "review" in pt:
        return "review"
    if "observational" in pt or "cohort" in pt:
        return "observational study"
    return "study"


def _extract_rich(rec):
    """Normalize one Europe PMC record with manuscript-grounding fields.

    Superset of `_extract`: additionally keeps authors (parsed from authorString),
    abstract and study_type, which is what block_c needs to (i) build in-text
    citations, (ii) render the included-study table, (iii) write a grounded
    Background/Discussion. No numeric outcome is invented — only bibliographic
    facts returned by the API are kept.
    """
    base = _extract(rec)
    ji = rec.get("journalInfo") or {}
    base.update({
        "authors": _parse_authors(rec.get("authorString")),
        "abstract": _strip_html(rec.get("abstractText") or ""),
        "study_type": _infer_study_type(base.get("pub_types")),
        "journal_abbr": (ji.get("journal") or {}).get("medlineAbbreviation") or "",
        "is_open_access": bool(rec.get("isOpenAccess")),
    })
    return base


# Grounding-layer publication-type filters.
#
# Verified live against Europe PMC (2026-09-22):
#   - `PUBLICATION_TYPE:"..."` returns 0 hits (wrong field name).
#   - `PUB_TYPE:"Randomized Controlled Trial"` works (901 hits on the omega-3 /
#     depression probe) and the returned records really are RCTs.
#
# Deliberately NOT reusing `_build_query` (which appends free-text
# "AND randomized controlled trial") — that mixes reviews into the top results;
# and deliberately NOT passing `sort=CITED desc`: citation sorting overpowers
# relevance and returns unrelated mega-review papers (e.g. "Heart Disease and
# Stroke Statistics" annual reports on an omega-3 query). Default relevance
# ordering is kept, and `dedup_probe` behaviour is left untouched.
_GROUNDING_PUBTYPE = {
    "rct": ' AND (PUB_TYPE:"Randomized Controlled Trial")',
    # NOTE: `PUB_TYPE:"Meta-Analysis"` is NOT a valid Europe PMC value — the API
    # answers with an error (hitCount None) rather than 0 hits. The synthesis
    # layer therefore uses "Systematic Review", which is valid and semantically
    # right for "what syntheses already exist on this question".
    "systematic-review": ' AND (PUB_TYPE:"Systematic Review")',
}


def _build_grounding_query(topic, review_type, year_from=None, year_to=None):
    """Query for the manuscript-grounding layer (field-restricted pub types)."""
    q = (topic or "").strip()
    q += _GROUNDING_PUBTYPE.get(review_type, "")
    if year_from or year_to:
        lo = str(year_from) if year_from else "1900"
        hi = str(year_to) if year_to else "3000"
        q += " AND (PUB_YEAR:[%s TO %s])" % (lo, hi)
    return q


def _search_once(topic, review_type, max_results, year_from=None, year_to=None):
    """One Europe PMC layer, rich records. Returns (works, query, hit_count, error)."""
    q = _build_grounding_query(topic, review_type, year_from, year_to)
    params = {
        "query": q,
        "format": "json",
        "resultType": "core",
        "pageSize": min(50, max(1, max_results)),
        "page": 1,
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    try:
        j = _get_json(url)
    except Exception as e:  # noqa: BLE001 - degrade, never crash the workflow
        return [], q, None, str(e)
    hits = j.get("hitCount")
    results = (j.get("resultList") or {}).get("result", []) or []
    return [_extract_rich(r) for r in results[:max_results]], q, hits, None


def to_search_query(topic):
    """Turn a manuscript title into a tight Europe PMC query string.

    WHY: feeding the full title in as the query is actively harmful — the
    subtitle ("...: a systematic review and meta-analysis of randomized
    controlled trials") adds noise words that narrow the result set
    (138 hits -> 6 hits in testing) and shifts which papers come back.
    Keep the main title and drop stopwords; content words carry the search.
    """
    if not topic:
        return ""
    main = str(topic).split(":")[0].strip()
    words = [w for w in re.split(r"[^\w\-()]+", main)
             if w and w.lower() not in _STOP]
    # 括号在 Europe PMC 查询串里是分组语法，"(DHA)" 会让查询解析异常 ——
    # 去掉括号本身、保留里面的内容词。
    words = [w.strip("()") for w in words]
    q = " ".join(w for w in words if w).strip()
    return q or main


def search_evidence(topic, n_primary=12, n_synthesis=5, year_from=None):
    """Live Europe PMC search used to GROUND the C1 manuscript in real papers.

    Two layers, because a manuscript needs both:
      - `primary`: RCTs / clinical trials -> candidate included studies
        (in-text citations, characteristics table, reference list).
      - `synthesis`: existing meta-analyses / systematic reviews -> the
        "what is already known" backbone of Background and the comparison
        target of Discussion.

    Returns:
        {
          "ok": bool, "error": str|None,
          "query": {"primary": str, "synthesis": str},
          "hit_count": {"primary": int|None, "synthesis": int|None},
          "primary": [rec...], "synthesis": [rec...],
          "database": "Europe PMC (MEDLINE / PubMed Central)",
          "searched_on": "YYYY-MM-DD",
        }
    Callers MUST degrade gracefully on ok=False (network blocked, topic too
    narrow, etc.) — this is a best-effort grounding layer, never a hard gate.
    """
    if not (topic or "").strip():
        return {"ok": False, "error": "empty topic", "primary": [], "synthesis": [],
                "query": {}, "hit_count": {}, "searched_on": _today()}

    topic = to_search_query(topic)

    # Ask for a wide shortlist and let _rank prune: the relevance filter
    # typically keeps ~1/3, so a narrow page would leave too few citations.
    prim, q1, h1, e1 = _search_once(topic, "rct", max(25, n_primary * 3), year_from)
    time.sleep(1.0)  # Europe PMC 对连续查询敏感：间隔过短第二次会返回错误响应
    synth, q2, h2, e2 = _search_once(topic, "systematic-review",
                                     max(25, n_synthesis * 3), year_from)
    if h2 is None and not e2:
        # 静默失败（拿到响应但无 hitCount）= 被限流；等一拍重试一次。
        time.sleep(2.0)
        synth, q2, h2, e2 = _search_once(topic, "systematic-review",
                                         max(25, n_synthesis * 3), year_from)
    # Fallback: if the RCT filter is too narrow, retry with systematic reviews
    # so the manuscript is never left without any grounding citation.
    if not prim and e1 is None:
        prim, q1, h1, e1 = _search_once(topic, "systematic-review", n_primary, year_from)

    # 严格化 primary 层：PUB_TYPE 过滤后仍会混入 review（Europe PMC 的 pubType
    # 是多值的）。若候选里存在**真正的 RCT**，就只用真 RCT 建表 —— 否则
    # "randomized controlled trial" 这一列会出现 review，属于事实错误。
    # ⚠️ 必须在 _rank **之前**做：_rank 在结果太少时会放宽相关性门槛，若先放宽
    # 再按类型过滤，会把放宽进来的 review 又剔除掉，只剩寥寥几条（实测 10→3）。
    _rct = [w for w in prim
            if "randomized controlled trial" in (w.get("study_type") or "").lower()]
    if _rct:
        prim = _rct

    terms = _query_terms(topic)
    prim = _rank(prim, terms, n_primary)
    synth = _rank(synth, terms, n_synthesis)

    # 跨层去重：同一篇可能同时出现在两层（典型如 Cochrane 综述）。参考文献列表
    # 里出现重复条目是硬伤。
    def _key(w):
        return ((w.get("doi") or "").lower()
                or (w.get("title") or "").strip().lower()[:90])

    prim = _dedup(prim)
    _seen = {_key(w) for w in prim}
    synth = _dedup([w for w in synth if _key(w) not in _seen])

    err = e1 or e2
    return {
        "ok": bool(prim or synth),
        "error": err,
        "query": {"primary": q1, "synthesis": q2},
        "hit_count": {"primary": h1, "synthesis": h2},
        "primary": prim,
        "synthesis": synth,
        "database": "Europe PMC (MEDLINE / PubMed Central)",
        "searched_on": _today(),
    }


_STOP = {"the", "and", "for", "with", "of", "in", "on", "a", "an", "to", "vs",
         "versus", "randomized", "controlled", "trial", "trials", "study",
         "studies", "analysis", "meta", "systematic", "review", "adults",
         "patients", "participants", "using", "based", "among"}


def _dedup(works):
    """Drop repeated records (same DOI, else same title) keeping first occurrence."""
    seen = set()
    out = []
    for w in works:
        k = ((w.get("doi") or "").lower()
             or (w.get("title") or "").strip().lower()[:90])
        if not k or k in seen:
            continue
        seen.add(k)
        out.append(w)
    return out


def _query_terms(topic):
    """Content words of the query, used only for a relevance sanity filter."""
    if not topic:
        return []
    # CJK queries have no whitespace tokens — skip filtering rather than
    # guessing (their hit set is usually empty anyway).
    if not any(" " in str(topic) for t in [topic]):
        return []
    out = []
    for w in re.split(r"[^\w\-]+", str(topic).lower()):
        w = w.strip("-")
        if len(w) >= 3 and w not in _STOP and w not in out:
            out.append(w)
    return out


def _rank(works, terms, n, min_score=None):
    """Drop off-topic hits and order by how many query terms they actually match.

    Rationale: Europe PMC relevance ordering alone surfaced clearly unrelated
    RCTs (krill oil, blueberry supplementation) on an omega-3/depression query.
    A hit must match at least 2 distinct content words (when >=3 are available).

    If that leaves too few hits (narrow topics), the bar is relaxed to 1 term -
    a smaller but still on-topic citation set beats a naked manuscript.
    """
    if not works:
        return []
    need = 2 if len(terms) >= 3 else 1
    if min_score is not None:
        need = min_score

    def _keep(sc):
        return not terms or sc >= need

    scored = []
    for w in works:
        blob = ("%s %s" % (w.get("title") or "", w.get("abstract") or "")).lower()
        sc = sum(1 for t in terms if t in blob)
        w["relevance"] = sc
        if _keep(sc):
            scored.append(w)
    if len(scored) < max(3, n // 2) and min_score is None and need > 1:
        return _rank(works, terms, n, min_score=1)
    scored.sort(key=lambda x: -x.get("relevance", 0))
    return scored[:n]


def _today():
    return datetime.date.today().isoformat()


def main():
    ap = argparse.ArgumentParser(
        description="In-skill Europe PMC dedup probe (self-contained, no other skill needed).")
    ap.add_argument("--topic", required=True, help="PICO-derived query string")
    ap.add_argument("--layer", choices=["cochrane", "pubmed", "both"], default="both")
    ap.add_argument("--review-type", default="systematic-review",
                    choices=["meta-analysis", "systematic-review", "rct"])
    ap.add_argument("--year-from", type=int)
    ap.add_argument("--year-to", type=int)
    ap.add_argument("--max", type=int, default=8)
    ap.add_argument("--out")
    args = ap.parse_args()

    if args.layer == "both":
        res = dedup_probe(args.topic, args.year_from, args.year_to, args.max)
    elif args.layer == "cochrane":
        res = probe(args.topic, layer="cochrane", year_from=args.year_from,
                    year_to=args.year_to, max_results=args.max)
    else:
        res = probe(args.topic, layer="pubmed", review_type=args.review_type,
                    year_from=args.year_from, year_to=args.year_to, max_results=args.max)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        print("[OK] wrote probe result -> %s" % args.out)
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
