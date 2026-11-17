#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ref_verify.py — 参考文献真实核验（CrossRef + PubMed E-utilities）。

对每篇参考文献用 CrossRef API（DOI 解析）和/或 PubMed E-utilities（PMID 解析）做
**存在性 + 元数据** 真实查证，防止 AI 虚构参考文献（JAMA 2026-08 红线）。

API 端点（公共，无需密钥；CrossRef 有速率限制但 generous，适合小批量校验）：
  - CrossRef:  https://api.crossref.org/works/<DOI>  → title/authors/journal/year/DOI/type
  - PubMed esummary: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=<PMID>&retmode=json
  - PubMed efetch (retraction): 检查 PublicationType 含 RetractionNotice / RetractedArticle

用法：
  # 单条校验
  r = verify_reference(doi="10.1016/j.jclinepi.2024.01.001")
  r = verify_reference(pmid="38268826")
  r = verify_reference(doi="10.xxx", pmid="12345678")  # 双侧校验

  # 批量校验（自动去重、限速）
  results = verify_references([{"doi": "10.xxx", "title": "..."}, ...])

返回 dict：
  {
    "status": "ok" | "not_found" | "mismatch" | "retracted" | "unverified_offline" | "error",
    "doi": "...", "pmid": "...",
    "verified_title": "...",        # 来自 API 的真实标题（小写归一化后比较）
    "verified_first_author": "...", # 第一作者姓
    "year": 2024,
    "journal": "...",
    "type": "journal-article" | "retracted-article" | ...,
    "is_retracted": False,
    "source": "crossref" | "pubmed" | "both",
    "message": "...",
  }

零第三方依赖（纯 urllib + json）。网络失败时 status="error"/"unverified_offline"，不阻塞主流程。

状态语义（重要，防止红线误杀）：
  - not_found           = API 明确未收录（HTTP 404）→ 才可怀疑虚构引用
  - unverified_offline  = 网络/接口不可达 → **不得**判虚构，须联网重试
  - retracted           = API 判定，或上游/人工 is_retracted 标注
"""

from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
import urllib.error

# ---------------------------------------------------------------------------
# 内部 HTTP
# ---------------------------------------------------------------------------
_UA = "meta-analysis-ref-verify/1.0 (mailto:meta-analysis@example.com)"  # CrossRef 要求的 polite pool


def _get(url: str, timeout: int = 20) -> dict | None:
    """兼容包装：GET JSON dict，任何失败返回 None（不区分失败原因）。

    内部统一走 `_get2`；需要区分「明确未收录(404)」与「网络不可达」时请直接用 `_get2`
    （`_get` 无法区分，误用会把断网当成文献不存在）。
    """
    return _get2(url, timeout)[0]


def _get2(url: str, timeout: int = 20):
    """GET 并区分状态：返回 (data|None, state)，state ∈ "ok" | "not_found" | "error"。

    区分「API 明确未收录（HTTP 404）」与「网络/接口不可达」——只有前者才可怀疑虚构；
    后者必须降级为「未能核验」，否则断网时真实文献会被误判为虚构（C3 红线误杀）。
    """
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": _UA,
            "Accept": "application/json",
        })
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8")), "ok"
    except urllib.error.HTTPError as e:
        if getattr(e, "code", None) == 404:
            return None, "not_found"
        return None, "error"            # 429/5xx 等可重试错误
    except (urllib.error.URLError, TimeoutError, OSError,
            json.JSONDecodeError, UnicodeDecodeError):
        return None, "error"
    except Exception:
        return None, "error"


# ---------------------------------------------------------------------------
# 文本归一化（用于标题/作者比较）
# ---------------------------------------------------------------------------
def _norm(s: str | None) -> str:
    """小写 + 去标点/空格，供模糊比较。"""
    if not s:
        return ""
    s = s.lower().strip()
    s = re.sub(r"[^\w]+", "", s)  # 仅保留字母数字
    return s


def _first_author_lastname(author_str: str | None) -> str | None:
    """从作者字符串提取第一作者姓（简单启发式）。"""
    if not author_str:
        return None
    # "Smith J" / "Smith, John" / "John Smith"
    author_str = author_str.strip()
    if "," in author_str:
        return author_str.split(",")[0].strip().lower()
    parts = author_str.split()
    return parts[-1].lower() if parts else None


# ---------------------------------------------------------------------------
# CrossRef API
# ---------------------------------------------------------------------------
def _crossref_verify(doi: str):
    """CrossRef API 解析 DOI。返回 (payload|None, state)；state ∈ ok|not_found|error。"""
    bare = doi.split("doi.org/")[-1] if "doi.org/" in doi else doi
    url = f"https://api.crossref.org/works/{urllib.parse.quote(bare, safe='/:')}"
    data, state = _get2(url)
    if state != "ok" or not data:
        return None, state
    msg = data.get("message") or {}
    if not msg:
        return None, "not_found"

    title_list = msg.get("title") or []
    verified_title = title_list[0] if title_list else None

    authors = msg.get("author") or []
    first_author = None
    if authors:
        a = authors[0]
        first_author = (a.get("family") or a.get("name") or "").strip()

    # 期刊: container-title 优先，短名次之
    container = msg.get("container-title") or []
    short = msg.get("short-container-title") or []
    journal = (container[0] if container else (short[0] if short else None))

    # 年份: published-print → published-online → created
    year = None
    for k in ("published-print", "published-online", "published", "created"):
        v = msg.get(k)
        if v and "date-parts" in v and v["date-parts"]:
            dp = v["date-parts"][0]
            if dp and dp[0]:
                year = dp[0]
                break

    # 类型 + 撤稿检查
    rtype = msg.get("type") or ""
    is_retracted = (
        "retraction" in rtype.lower()
        or "retraction" in (msg.get("title") or [""])[0].lower()
    )
    # CrossRef 撤稿文献通常有 related-item + retractionOf
    if not is_retracted:
        for ri in (msg.get("relation") or {}).get("is-retraction-of", []):
            if ri:
                is_retracted = True
                break

    return {
        "verified_title": verified_title,
        "verified_first_author": first_author.lower() if first_author else None,
        "year": year,
        "journal": journal,
        "type": rtype,
        "is_retracted": is_retracted,
    }, "ok"


# ---------------------------------------------------------------------------
# PubMed E-utilities API
# ---------------------------------------------------------------------------
def _pubmed_verify(pmid: str):
    """PubMed esummary 解析 PMID。返回 (payload|None, state)；state ∈ ok|not_found|error。"""
    if not pmid or not re.match(r"^\d+$", str(pmid).strip()):
        return None, "not_found"        # PMID 格式非法 → 该库不可能收录
    pmid = str(pmid).strip()

    # 1) esummary — 基础元数据
    url = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
           f"?db=pubmed&id={pmid}&retmode=json")
    data, state = _get2(url)
    if state != "ok" or not data or "result" not in data:
        return None, state

    rec = (data["result"].get(pmid) or {})
    if not rec or rec.get("error"):
        return None, "not_found"

    # 标题
    verified_title = rec.get("title")

    # 作者
    authors = rec.get("authors") or []
    first_author = None
    if authors:
        # esummary 返回 name 字段（"Smith J" 或 "Smith JA"）
        name = authors[0].get("name") or ""
        first_author = name.split()[0].lower() if name else None

    # 期刊 + 年份
    journal = rec.get("fulljournalname") or rec.get("source")
    pubdate = rec.get("pubdate") or rec.get("sortpubdate") or ""
    year = None
    m = re.search(r"\b(19|20)\d{2}\b", pubdate)
    if m:
        year = int(m.group(0))

    # 撤稿检查：esummary 的 pubtype 可能含 "Retraction"
    pubtypes = rec.get("pubtype") or []
    is_retracted = any("retraction" in str(p).lower() for p in pubtypes)

    # DOI（PubMed 记录的 DOI）
    articleids = rec.get("articleids") or []
    pmid_doi = None
    for aid in articleids:
        if str(aid.get("idtype")).lower() == "doi":
            pmid_doi = aid.get("value")
            break

    return {
        "verified_title": verified_title,
        "verified_first_author": first_author,
        "year": year,
        "journal": journal,
        "type": ",".join(pubtypes) if pubtypes else None,
        "is_retracted": is_retracted,
        "doi_from_pubmed": pmid_doi,
    }, "ok"


# ---------------------------------------------------------------------------
# 单条核验
# ---------------------------------------------------------------------------
def verify_reference(doi: str | None = None, pmid: str | None = None,
                     title: str | None = None,
                     first_author: str | None = None,
                     year: int | None = None,
                     journal: str | None = None) -> dict:
    """单条参考文献核验。至少提供 doi 或 pmid 其一。

    双侧都有时，两侧都查，交叉验证 DOI/PMID 对应同一实体（防拼接幻觉）。
    """
    result = {
        "status": "ok",
        "doi": doi,
        "pmid": pmid,
        "verified_title": None,
        "verified_first_author": None,
        "year": None,
        "journal": None,
        "type": None,
        "is_retracted": False,
        "source": None,
        "message": "",
    }

    if not doi and not pmid:
        result["status"] = "error"
        result["message"] = "无 DOI 且无 PMID，无法真实核验"
        return result

    crossref = None
    pubmed = None
    states = []

    if doi:
        crossref, cs = _crossref_verify(doi)
        states.append(cs)
    if pmid:
        pubmed, ps = _pubmed_verify(pmid)
        states.append(ps)

    # 双侧交叉验证
    if crossref and pubmed:
        result["source"] = "both"
        # PubMed 返回的 DOI 与传入 DOI 交叉核对
        if doi and pubmed.get("doi_from_pubmed"):
            pdoi = pubmed["doi_from_pubmed"].lower().strip()
            if pdoi != doi.lower().strip() and not doi.lower().startswith(pdoi):
                result["status"] = "mismatch"
                result["message"] = (
                    f"DOI 交叉不一致：传入 {doi}，PubMed 记录 {pdoi}")
        # 标题交叉核对
        ct = _norm(crossref.get("verified_title"))
        pt = _norm(pubmed.get("verified_title"))
        if ct and pt and ct != pt:
            # 不完全相等，检查子串包含
            if ct not in pt and pt not in ct:
                result["status"] = "mismatch"
                result["message"] += ("；标题交叉不一致：CrossRef=" +
                                      str(crossref.get("verified_title")) +
                                      " PubMed=" +
                                      str(pubmed.get("verified_title")))
        # 取更全的字段
        result["verified_title"] = (crossref.get("verified_title")
                                     or pubmed.get("verified_title"))
        result["verified_first_author"] = (
            crossref.get("verified_first_author")
            or pubmed.get("verified_first_author"))
        result["year"] = crossref.get("year") or pubmed.get("year")
        result["journal"] = crossref.get("journal") or pubmed.get("journal")
        result["type"] = crossref.get("type") or pubmed.get("type")
        result["is_retracted"] = crossref.get("is_retracted", False) or pubmed.get("is_retracted", False)

    elif crossref:
        result["source"] = "crossref"
        result["verified_title"] = crossref.get("verified_title")
        result["verified_first_author"] = crossref.get("verified_first_author")
        result["year"] = crossref.get("year")
        result["journal"] = crossref.get("journal")
        result["type"] = crossref.get("type")
        result["is_retracted"] = crossref.get("is_retracted", False)

    elif pubmed:
        result["source"] = "pubmed"
        result["verified_title"] = pubmed.get("verified_title")
        result["verified_first_author"] = pubmed.get("verified_first_author")
        result["year"] = pubmed.get("year")
        result["journal"] = pubmed.get("journal")
        result["type"] = pubmed.get("type")
        result["is_retracted"] = pubmed.get("is_retracted", False)
        if pubmed.get("doi_from_pubmed"):
            result["doi"] = pubmed["doi_from_pubmed"]

    else:
        if states and all(s == "error" for s in states):
            # 网络/接口不可达：不得判「疑似虚构」，降级为「未能核验」
            result["status"] = "unverified_offline"
            result["message"] = "网络/接口不可达，未能核验（请联网重试；非缺失证据）"
        else:
            result["status"] = "not_found"
            result["message"] = "CrossRef / PubMed 均未查到该记录"
        return result

    # 标题/作者交叉比较（传入值 vs 真实值）
    if title and result.get("verified_title"):
        nt = _norm(title)
        vt = _norm(result["verified_title"])
        if nt and vt and nt != vt and nt not in vt and vt not in nt:
            # 不立即标 mismatch（中文标题常见差异），仅加警告
            if result["status"] == "ok":
                result["message"] += ("；标题略有差异（传入：" +
                                      str(title)[:60] + "，API：" +
                                      str(result["verified_title"])[:60] + "）")

    if first_author and result.get("verified_first_author"):
        fa = first_author.lower().strip()
        vfa = result["verified_first_author"].lower().strip()
        if fa and vfa and fa != vfa and fa not in vfa and vfa not in fa:
            result["status"] = "mismatch"
            result["message"] += (f"；第一作者不一致（传入 {first_author}，"
                                  f"API {result['verified_first_author']}）")

    # 撤稿最终确认
    if result.get("is_retracted"):
        result["status"] = "retracted"
        result["message"] = "⚠️ 该文献已被标记为撤稿/撤回：" + result["message"]

    if result["status"] == "ok" and not result["message"]:
        result["message"] = "CrossRef/PubMed 真实查到，元数据一致"

    return result


# ---------------------------------------------------------------------------
# 批量核验
# ---------------------------------------------------------------------------
def verify_references(references: list, delay: float = 0.25) -> list:
    """逐条核验引用列表，返回 [{...}, ...]。delay 控制速率（CrossRef polite pool）。"""
    results = []
    seen_keys = set()
    for idx, r in enumerate(references or []):
        if not isinstance(r, dict):
            results.append({"status": "error", "message": "非法引用格式"})
            continue
        doi = r.get("doi")
        pmid = r.get("pmid")
        # 去重只对「有标识」条目按 DOI+PMID 生效；无标识条目用下标唯一化，
        # 避免多条无 DOI/PMID 的参考被静默丢弃（同一 key "|" 全被去重跳过）。
        if doi or pmid:
            key = f"{doi or ''}|{pmid or ''}"
            if key in seen_keys:
                continue
            seen_keys.add(key)
        else:
            key = f"no-id#{idx}"

        vr = verify_reference(
            doi=doi, pmid=pmid,
            title=r.get("title"),
            first_author=r.get("first_author") or (r.get("authors", [""])[0] if isinstance(r.get("authors"), list) else None),
            year=r.get("year"),
            journal=r.get("journal"),
        )
        # 采纳上游/人工标注的撤稿提示：无 DOI/PMID 时 API 无法判定，必须以此兜底，
        # 否则已知撤稿文献会绕过 C3 reference_verification 红线。
        if r.get("is_retracted") and vr.get("status") != "retracted":
            vr["is_retracted"] = True
            vr["status"] = "retracted"
            _base = vr.get("message") or ""
            vr["message"] = ("⚠️ 该文献已被标记为撤稿/撤回（依据上游/人工标注）"
                             + ("：" + _base if _base else ""))
        vr["key"] = key
        vr["input_index"] = idx
        results.append(vr)
        if delay and (doi or pmid):
            time.sleep(delay)  # polite rate-limit
    return results


# ---------------------------------------------------------------------------
# CLI（调试用）
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    ap = argparse.ArgumentParser(description="参考文献真实核验（CrossRef/PubMed）")
    ap.add_argument("--doi", help="DOI")
    ap.add_argument("--pmid", help="PMID")
    ap.add_argument("--title", help="标题（用于交叉核对）")
    args = ap.parse_args()
    r = verify_reference(doi=args.doi, pmid=args.pmid, title=args.title)
    print(json.dumps(r, ensure_ascii=False, indent=2))
