#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf_fetch.py — 文献全文 PDF 批量下载（DOI / PMID → 开放获取全文）

对应 SKILL.md Review Workflow「PDF Batch-download」功能（2026-08-20 补实现）。
⚠️ **opt-in 功能**：仅在用户明确要求（给出 DOI/PMID 列表并确认下载）时由 agent 调用。

数据源（免费、无密钥）：
  - DOI  → Unpaywall API（https://api.unpaywall.org/v2/<doi>?email=<EMAIL>），取
          best_oa_location.url_for_pdf；无 OA 副本则如实报告（不绕过付费墙）。
  - PMID → NCBI E-utilities elink（pubmed→pmc）+ PMC 全文 PDF 直链。
  - 多通道/预印本回退（2026-09-06 起上移 coze，本地只做调用）：
      * 服务端 publisher_pdf 工作流含 A 路径 + 补充链：Unpaywall →
        PPR 预印本(bioRxiv/medRxiv) → arXiv，按 DOI 反查元数据并做作者级同篇校验；
      * 本地仅保留「coze 不可用」时的直下降级（open_access_url / PMC），
        不再本地实现 PPR/arXiv 检索下载（原 _try_preprint_fallback 停用，保留为历史参考）。

用法：
  python pdf_fetch.py doi 10.1016/j.jclinepi.2024.01.001 10.1136/bmj-2023-076058
  python pdf_fetch.py pmid 38268826 37849447
  python pdf_fetch.py doi --input list.txt --out pdfs/        # 从文件读（每行一个 ID）
  python pdf_fetch.py doi --email you@example.com 10.xxxx/yy  # 指定 Unpaywall email
  # 付费墙/无法下载时：预印本回退自动由服务端补充链执行（bioRxiv/medRxiv/arXiv），无需本地开关
  python pdf_fetch.py doi 10.xxxx/yy
  python pdf_fetch.py pmid 38268826 37849447

输出：下载的 PDF 保存到 out_dir（默认 ./pdfs/），stdout 打印清单（含失败原因）。

纯标准库（urllib），零第三方依赖。网络失败不阻塞，逐条独立重试。
"""

import argparse
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

DEFAULT_EMAIL = "meta-analysis@example.com"  # Unpaywall 要求合法 email，可 --email 覆盖


def _get(url: str, timeout: int = 30, retries: int = 2) -> bytes:
    """GET 带重试（跳过系统代理残留：Windows ProxyError → 直连）。"""
    last = None
    for _ in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "meta-analysis-skill/1.10"})
            # 强制跳过代理：系统代理（如 WorkBuddy 本机代理 63226）会杀死长连接或拦截
            # localhost 流量，导致 SSE 流断开、PDF 下载超时。no_proxy 环境变量未必生效
            #（urllib 仅在代理非空时读 no_proxy），故直接装一个空 ProxyHandler 绕过所有代理。
            proxy_handler = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy_handler)
            with opener.open(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 429):
                time.sleep(1)
                last = f"HTTP {e.code}"
                continue
            raise
        except Exception as e:  # URLError / ProxyError 等
            last = f"{type(e).__name__}: {e}"
            time.sleep(0.5)
    raise RuntimeError(str(last))


# ---------------------------------------------------------------------------
# 下载前类型探测（规律 R1 前移）：在发起 PDF 下载**之前**就读到 review/guideline
# 判定，直接终止下载链路（省下载 + 抽取 + 垃圾行全流程）。
# 双通道：① Europe PMC REST pubType（权威元数据，pmid/doi 均可查）；
#        ② 出版商条目页 article-type 徽标 / citation meta（URL 非直链 PDF 时）。
# ---------------------------------------------------------------------------
_EPMC_SEARCH = ("https://www.ebi.ac.uk/europepmc/webservices/rest/search"
                "?query={q}&format=json&resultType=core")

# 页面/元数据上的类型标签（严格短语，避免被参考文献列表污染）
_PAGE_TYPE_REVIEW = re.compile(
    r"review article|systematic review|meta[- ]?analysis|scoping review|"
    r"umbrella review|narrative review|literature review", re.I)
_PAGE_TYPE_GUIDELINE = re.compile(
    r"clinical practice guideline|practice guidelines?\b|guidelines? (statement|document)|"
    r"consensus (statement|conference|report|guidelines)|position statement|"
    r"presidential advisory|expert (consensus|panel)", re.I)
_PAGE_TYPE_META = re.compile(
    r"""name=["']citation_article_type["'][^>]*content=["']([^"']+)["']|"""
    r"""content=["']([^"']+)["'][^>]*name=["']citation_article_type["']""", re.I)


def epmc_pubtypes(pmid=None, doi=None):
    """查 Europe PMC REST 权威 pubType 列表（文章类型元数据，下载前零成本）。"""
    q = None
    if pmid:
        q = f"EXT_ID:{pmid}%20SRC:MED"
    elif doi:
        q = f'DOI:"{urllib.parse.quote(str(doi))}"'
    if not q:
        return []
    try:
        data = json.loads(_get(_EPMC_SEARCH.format(q=q), timeout=12, retries=1))
        hits = (data.get("resultList") or {}).get("result") or []
        for hit in hits:
            ptl = hit.get("pubTypeList") or {}
            pts = ptl.get("pubType") or []
            if isinstance(pts, str):
                pts = [pts]
            if pts:
                return [str(p) for p in pts]
    except Exception:  # noqa: BLE001 — 探测失败绝不阻断下载
        pass
    return []


def landing_type_text(url, timeout=10):
    """抓条目页 HTML（跳过直链 PDF），返回裁剪后的可见文本 + meta 区。"""
    if not url or not isinstance(url, str):
        return ""
    u = url.strip()
    if u.lower().endswith(".pdf") or "/pdf/" in u.lower() or "pdf" in u.lower().split("?")[0][-8:]:
        return ""
    try:
        raw = _get(u, timeout=timeout, retries=0)
        text = raw.decode("utf-8", errors="ignore")
    except Exception:  # noqa: BLE001
        return ""
    # meta 标签区 + head 区（徽标在正文前部）
    metas = " ".join(m.group(0) for m in _PAGE_TYPE_META.finditer(text))
    body = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", " ", text)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"\s+", " ", body)
    return metas + " " + body[:6000]


def screen_page_type(study):
    """下载前类型探测。返回 (excluded, reason, source) —— excluded 才终止下载。

    ① Europe PMC pubType（权威）；② 条目页徽标 / citation_article_type。
    任一命中 review/guideline 即排除；两通道皆失败 → 不排除（照常下载，
    由 PDF 层 classify_pdf 强制甄别兜底）。
    """
    if not isinstance(study, dict):
        return False, None, ""
    pmid = study.get("pmid")
    doi = study.get("doi")
    # ① pubType 元数据
    pts = epmc_pubtypes(pmid=pmid, doi=doi)
    for pt in pts:
        if re.search(r"review|meta[- ]?analysis", pt, re.I):
            return True, f"Europe PMC pubType 标注综述：{pt}", "epmc_pubtype"
        if re.search(r"guideline|consensus|position statement|advisory", pt, re.I):
            return True, f"Europe PMC pubType 标注指南/共识：{pt}", "epmc_pubtype"
    # ② 条目页徽标
    for u in (study.get("url"), study.get("open_access_url")):
        page = landing_type_text(u)
        if not page:
            continue
        m = _PAGE_TYPE_META.search(page)
        if m:
            val = (m.group(1) or m.group(2) or "").strip()
            if re.search(r"review|meta[- ]?analysis", val, re.I):
                return True, f"条目页 citation_article_type={val}", "page_meta"
            if re.search(r"guideline|consensus", val, re.I):
                return True, f"条目页 citation_article_type={val}", "page_meta"
        if _PAGE_TYPE_REVIEW.search(page):
            return True, ("条目页文章类型徽标："
                          + _PAGE_TYPE_REVIEW.search(page).group(0)), "page_badge"
        if _PAGE_TYPE_GUIDELINE.search(page):
            return True, ("条目页文章类型徽标："
                          + _PAGE_TYPE_GUIDELINE.search(page).group(0)), "page_badge"
        break  # 只试第一个有效页面，避免拖慢
    return False, None, ""


def doi_to_pdf(doi: str, email: str) -> str | None:
    """Unpaywall：返回可下载 PDF URL；无 OA 副本 / 查询失败均返回 None（不抛异常）。"""
    url = f"https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={urllib.parse.quote(email)}"
    try:
        raw = _get(url)
        data = json.loads(raw.decode("utf-8"))
    except Exception:
        # 422/超时/网络错：视为无 OA 副本，交由上层兜底（如 PMC 解析）
        return None
    if not data.get("is_oa"):
        return None
    loc = data.get("best_oa_location") or {}
    pdf = loc.get("url_for_pdf") or loc.get("url")
    return pdf


def doi_to_pmc_pdf(doi: str) -> str | None:
    """Europe PMC：按 DOI 查 PMC OA 全文 PDF 直链（出版商付费墙外的开放获取副本）。

    返回 PMC OA PDF URL；无 PMC OA 版本返回 None。免费、无密钥。
    """
    q = urllib.parse.quote(f'DOI:"{doi}"')
    url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
           f"?query={q}&format=json&resultType=core&pageSize=1")
    try:
        data = json.loads(_get(url).decode("utf-8"))
    except Exception:
        return None
    res = (data.get("resultList") or {}).get("result", [])
    if not res:
        return None
    rec = res[0]
    for ft in (rec.get("fullTextUrlList") or {}).get("fullTextUrl", []):
        if (ft.get("documentStyle") == "pdf"
                and str(ft.get("availability", "")).lower().startswith("open")):
            return ft.get("url")
    return None


def pmid_to_pdf(pmid: str) -> str | None:
    """PMID → PMC 全文 PDF 直链（经 NCBI elink）。"""
    elink = ("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi"
             f"?dbfrom=pubmed&db=pmc&id={pmid}&retmode=json")
    try:
        data = json.loads(_get(elink).decode("utf-8"))
        links = data.get("linksets", [{}])[0].get("linksetdbs", [])
        pmc_ids = []
        for lsdb in links:
            pmc_ids.extend(lsdb.get("links", []))
        if not pmc_ids:
            return None
        pmcid = pmc_ids[0]
        return f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/"
    except Exception:
        return None


def _sanitize(name: str) -> str:
    return re.sub(r"[^\w.-]+", "_", name)[:80] or "download"


def download(url: str, out_path: str) -> bool:
    try:
        data = _get(url, timeout=60)
        with open(out_path, "wb") as f:
            f.write(data)
        return len(data) > 1000  # 粗略校验：PDF 至少 ~1KB
    except Exception:
        return False


# ---------------------------------------------------------------------------
# 同意墙 (Consent Wall) 自动同意处理
# 适用：OneTrust/Optanon 同意墙（Nature、Wiley、Sage、Taylor&Francis 等多家出版商）+ 
#       idp.nature.com 类型的 response_type=cookie 同意握手。
# 策略：种入 OneTrust「全部接受」cookie + 浏览器 UA/Accept 头，open 跟随重定向
#       时由 CookieJar 捕获 idp.nature.com 的 idp_session 握手。
# ⚠️ 已知局限（2026 实测验证）：Nature 边缘网关对自动化客户端做服务端 grade-c 分类 → 返
#   404「Page Not Found」；该层 bot 检测不在同意 cookie 范围，需真实浏览器 + 住宅代理方可
#   绕过。本函数对「仅靠 Optanon 同意 / idp 握手」的墙显著提高命中率。
# ---------------------------------------------------------------------------
_OPANON_CONSENT_ACCEPT_ALL = (
    "isIABGlobal=false&datestamp=Wed+Jan+01+2025+00%3A00%3A00.000Z&version=6.19.0"
    "&landingPath=NotApplicable&groups=C0001%2CC0002%2CC0003%2CC0004&hosts="
    "&legInt=C0002%2CC0003%2CC0004&consentLang=en&oasDisabled=false&AwaitingReconsent=false"
)
_BROWSER_UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


def _root_domain(host: str) -> str:
    """取 cookie 用的 parent domain：例如 www.nature.com → .nature.com。
    注：两段 TLD 足够覆盖 .com/.org/.gov 等常见出版商；对 .co.uk 等多段 TLD 略粗糙，
    实际仍能匹配同 eTLD+1 下的子域。"""
    parts = host.split(".")
    if len(parts) >= 2:
        return "." + ".".join(parts[-2:])
    return host


def _seed_optanon(cj: "http.cookiejar.CookieJar", host: str) -> None:
    """向 cookie jar 种入 OneTrust 「全部接受」cookie。"""
    dom = _root_domain(host)
    for name, val in [
        ("OptanonAlertBoxClosed", "2024-01-01T00:00:00.000Z"),
        ("OptanonConsent", _OPANON_CONSENT_ACCEPT_ALL),
    ]:
        c = http.cookiejar.Cookie(
            version=0, name=name, value=val, port=None, port_specified=False,
            domain=dom, domain_specified=True, domain_initial_dot=True,
            path="/", path_specified=True, secure=False, expires=None,
            discard=False, comment=None, comment_url=None, rest={}, rfc2109=False,
        )
        cj.set_cookie(c)


def _browser_opener(cj):
    """带 CookieJar + 浏览器头的 opener（默认 HTTPRedirectHandler 自动跟随重定向，
    借此完成 idp.nature.com 的 authorize→transit 握手）。"""
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [
        ("User-Agent", _BROWSER_UA),
        ("Accept", "text/html,application/xhtml+xml,application/pdf,*/*;q=0.8"),
        ("Accept-Language", "en-US,en;q=0.9"),
    ]
    return op


def consent_aware_download(url: str, out_path: str) -> bool:
    """同意墙感知下载：种入 OneTrust「全部接受」+ 浏览器头 + 跟随重定向（含 idp 握手）。
    返回 True 当且仅当真正落盘合法 PDF (%PDF- 头 + >=1KB)。"""
    try:
        host = urllib.parse.urlparse(url).hostname or ""
        cj = http.cookiejar.CookieJar()
        _seed_optanon(cj, host)
        op = _browser_opener(cj)
        # Referer：去掉 .pdf 后缀（模拟从文章页点下载）
        referer = url
        if referer.lower().endswith(".pdf"):
            referer = referer[: -len(".pdf")]
        req = urllib.request.Request(url, headers={"Referer": referer})
        with op.open(req, timeout=60) as r:
            data = r.read()
        if data[:4] != b"%PDF-" or len(data) < 1000:
            return False
        with open(out_path, "wb") as f:
            f.write(data)
        return True
    except Exception:
        return False


def nature_pdf_url(doi: str) -> str | None:
    """Nature 系列（含 s41598 / s41467 / nature 等前缀）直链 PDF URL。"""
    if not doi:
        return None
    bare = doi.split("doi.org/")[-1] if "doi.org/" in doi else doi
    return f"https://www.nature.com/articles/{bare}.pdf"


# ==== B2 (2026-09-04) 统一全文下载入口：open_access_url 优先 + 反爬委托 coze ====
# 背景：MDPI 等出版商对无头客户端反爬（带 UA+Referer 仍 403），本地 urllib 下不动；
# 而工作台 study 已采集 open_access_url（OpenAlex 直链，覆盖比 Unpaywall 广——实测
# Unpaywall 漏收该 MDPI 综述，OpenAlex 已给直链）。故下载顺序：
#   open_access_url → Unpaywall → Europe PMC(PMC OA)；本地失败且命中反爬出版商 →
#   委托 ct-search.coze.site/run 的 source=publisher_pdf（服务端 Playwright 真实浏览器）。
_ANTI_SCRAPE_HOSTS = ("mdpi.com", "mdpi-res.com", "mdpi-resilience.com")


def _is_anti_scrape(url: str) -> bool:
    """识别对无头客户端做反爬的出版商（命中且本地下载失败 → 委托 coze 服务端浏览器）。"""
    try:
        host = urllib.parse.urlparse(url).hostname or ""
    except Exception:
        return False
    return any(host == h or host.endswith("." + h) for h in _ANTI_SCRAPE_HOSTS)


def _coze_pdf_download(doi: str, out_path: str) -> dict | None:
    """委托 ct-search.coze.site/stream_run 的 publisher_pdf_batch（服务端真实浏览器）下载 PDF。

    2026-09-07 起改用 stream_run SSE 批量契约（与 ct-literature pdf_download 同款），
    单 DOI 作为单元素列表传入。覆盖场景：本地 urllib 全部失败的出版商/预印本服务器
    ——MDPI 等反爬出版商、medRxiv 官网（对无头 403）、bioRxiv 频控 429 等。
    服务端含 A 路径(OA/PMC/EPMC) + 补充链(Unpaywall → PPR bioRxiv/medRxiv → arXiv，
    作者级同篇校验) + 可选浏览器 B。

    Returns: info dict（含 src/via/review_tag）或 None（委托不可用/未返回 PDF）。
    """
    try:
        from ctsearch_client import fetch_publisher_pdf  # 平铺导入
    except Exception:
        try:
            from adapters.ctsearch_client import fetch_publisher_pdf
        except Exception:
            return None
    res = fetch_publisher_pdf(doi, query_origin="meta-analysis:local")
    if res.get("ok") and res.get("pdf_bytes"):
        with open(out_path, "wb") as f:
            f.write(res["pdf_bytes"])
        return {"src": "coze_publisher_pdf", "via": "coze",
                "review_tag": res.get("review_tag")}
    if res.get("ok") and res.get("pdf_url"):
        via = "coze_s3" if res.get("s3") else "coze_direct"  # 区分预签名外置 vs 原链直下
        if download(res["pdf_url"], out_path):
            return {"src": "coze_publisher_pdf", "via": via,
                    "review_tag": res.get("review_tag")}
    return None


def _resolve_pdf_url(doi: str, study=None) -> tuple:
    """解析可下载 PDF URL，按优先级返回 (url, src) 或 (None, None)。"""
    if isinstance(study, dict):
        oa = study.get("open_access_url") or study.get("oa_url")
        if oa:
            return oa, "open_access_url"
    u = doi_to_pdf(doi, DEFAULT_EMAIL)
    if u:
        return u, "unpaywall"
    u = doi_to_pmc_pdf(doi)
    if u:
        return u, "europepmc"
    return None, None


def _title_from_doi(doi: str) -> str | None:
    """按 DOI 取标题（预印本回退需要标题检索，免费、无密钥）。"""
    q = urllib.parse.quote(f'DOI:"{doi}"')
    url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
           f"?query={q}&format=json&resultType=core&pageSize=1")
    try:
        data = json.loads(_get(url).decode("utf-8"))
        res = (data.get("resultList") or {}).get("result", [])
        if res:
            return res[0].get("title")
    except Exception:
        return None
    return None


# ==== 预印本同篇校验（作者级，「不能弄错」）====
# 原则：预印本按标题模糊匹配，标题相近 ≠ 同一篇。故每个候选需与原始文献作者逐姓氏比对，
# 宁可缺漏（丢弃候选）也不能弄错（下载到不同篇的预印本）。
# ⚠️ 实测（2026-09-04）：Europe PMC / arXiv 的 TITLE:"完整短语" 检索对标题原文逐字节敏感
# （特殊字符/长标题 → 0 命中），故两源检索均做两段式：短语精确优先 → 0 命中回退
# 「内容词 AND」检索（召回放宽，精度交给作者校验兜底）。
_PREPRINT_STOPWORDS = frozenset(
    "a an the and or of in on at by for to with without from into during after before "
    "between among against across within about over under up down out off is are was were "
    "be been being have has had do does did will would can could should may might must its "
    "it's its it this that these those their our your his her their as than so but not no "
    "nor if then else when where which who whom whose how why what vs versus via per et al "
    "and or".split())


def _title_tokens(title: str, maxn: int = 5) -> list:
    """标题 → 前 maxn 个内容词（小写、去标点、去停用词），用于词 AND 检索兜底。"""
    if not title:
        return []
    t = re.sub(r"[^a-z0-9\s]+", " ", title.lower())
    toks = [w for w in t.split() if len(w) > 1 and w not in _PREPRINT_STOPWORDS]
    return toks[:maxn]
def _norm_lastname(s: str) -> str:
    """归一化姓氏：小写、去标点/空格、只保留字母数字与汉字（中英文统一比对）。"""
    if not s:
        return ""
    s = str(s).strip().lower()
    s = re.sub(r"[^一-鿿a-z0-9]", "", s)  # 去连字符/撇号/空格/点
    return s


def _lastnames_from_authors(authors) -> list:
    """从多种作者表示解析有序 lastname 列表（保持作者顺序，第一作者即 [0]）。

    authors 可为：
      - Crossref/Unpaywall 风格: [{"family":"Zhang","given":"San"}, ...]
      - Europe PMC 风格:        [{"lastName":"Zhang","firstName":"San"}, ...]
      - 字符串列表:             ["Zhang San", "Li Si", ...]
      - 字符串(authorString):   "Liu B, Stepien S, Macartney K."（取每段末词为姓）
    返回归一化姓氏列表。
    """
    out = []
    if isinstance(authors, str):
        for part in re.split(r"[;,]", authors):
            toks = part.split()
            if toks:
                out.append(_norm_lastname(toks[-1]))
        return [x for x in out if x]
    if not isinstance(authors, (list, tuple)):
        return []
    for a in authors:
        if isinstance(a, dict):
            ln = (a.get("family") or a.get("lastName") or a.get("lastname") or "")
            if not ln:
                # 退化为 fullName / name 末词
                fn = (a.get("fullName") or a.get("name") or a.get("full_name") or "")
                toks = str(fn).split()
                ln = toks[-1] if toks else ""
            out.append(_norm_lastname(ln))
        elif isinstance(a, str):
            toks = a.split()
            if toks:
                out.append(_norm_lastname(toks[-1]))
    return [x for x in out if x]


def _authors_from_doi(doi: str) -> list:
    """从 Crossref 反查原始文献作者 lastname 列表（覆盖所有文献，不限于 OA）。

    失败（网络/不存在）返回 [] —— 调用方据「不能弄错」原则将因缺作者而缺漏（不下载）。
    """
    bare = doi.split("doi.org/")[-1] if "doi.org/" in doi else doi
    url = f"https://api.crossref.org/works/{urllib.parse.quote(bare)}"
    try:
        d = json.loads(_get(url, timeout=20).decode("utf-8"))
        msg = d.get("message") or {}
        return _lastnames_from_authors(msg.get("author") or [])
    except Exception:
        return []


def _author_check(orig_ln: list, cand_ln: list) -> tuple:
    """作者校验：宁可缺漏不能弄错。返回 (passed:bool, reason:str)。

    规则（由严到宽）：
      1. 任一方缺作者信息 → 不通过（缺漏，无法校验）
      2. 无共同姓氏       → 不通过（明显不同篇）
      3. 第一作者都能解析且不一致 → 不通过（最强信号，不能弄错）
      4. 否则通过（第一作者一致且有共同姓氏）
    """
    if not orig_ln or not cand_ln:
        return False, "missing_author_info"
    o = set(orig_ln)
    p = set(cand_ln)
    inter = o & p
    if not inter:
        return False, "no_shared_author"
    # 第一作者硬约束（不能弄错）：双方都能解析出第一作者时，必须一致
    if orig_ln and cand_ln and orig_ln[0] != cand_ln[0]:
        return False, "first_author_mismatch"
    return True, f"{len(inter)}_shared_first_author_match"


def _cscl_official_pdf(doi: str) -> str | None:
    """CSHL 双库（bioRxiv/medRxiv，DOI 均 10.1101 前缀）官网 PDF 直链。

    经 api.biorxiv.org 按 collection 解析版本号 → 拼 <server>.org/content/<doi>v<ver>.full.pdf。
    ⚠️ 实测（2026-09-04）：bioRxiv 官网对无头客户端放行（200 application/pdf）；
    medRxiv 官网对无头 403（反爬），URL 仍返回、由下载层如实失败（走 coze 浏览器可救）。
    失败返回 None。
    """
    bare = doi.split("doi.org/")[-1] if "doi.org/" in doi else doi
    if not bare.startswith("10.1101/"):
        return None
    for coll in ("biorxiv", "medrxiv"):
        try:
            d = json.loads(_get(
                f"https://api.biorxiv.org/details/{coll}/{urllib.parse.quote(bare)}",
                timeout=20).decode("utf-8"))
            items = d.get("collection") or []
            if items:
                ver = items[0].get("version")
                if ver:
                    return f"https://www.{coll}.org/content/{bare}v{ver}.full.pdf"
        except Exception:
            continue
    return None


def _epmc_preprint_search(title: str) -> list:
    """Europe PMC 预印本合集（PPR）按标题检索 bioRxiv / medRxiv 候选。

    返回候选列表：[{doi, venue, pdf_url, authors}]；venue ∈ {biorxiv, medrxiv,
    biorxiv_medrxiv, other}（other 被开关过滤）。
    两段式检索：TITLE:"完整短语" 优先 → 0 命中回退「内容词 AND」（召回放宽，
    精度交给作者校验兜底）。⚠️ 实测：Europe PMC 的 src=PPR 是软过滤，可能混入
    src=MED 的 CSHL 期刊（DOI 也 10.1101 前缀），故只收 source=="PPR"。
    """
    if not title or len(title.strip()) < 8:
        return []

    def _run(q_expr: str, page_size: int = 15) -> list:
        url = (f"https://www.ebi.ac.uk/europepmc/webservices/rest/search"
               f"?query={urllib.parse.quote(q_expr)}&format=json&resultType=core"
               f"&pageSize={page_size}&src=PPR")
        try:
            d = json.loads(_get(url).decode("utf-8"))
            return (d.get("resultList") or {}).get("result", [])
        except Exception:
            return []

    recs = [r for r in _run(f'(TITLE:"{title.strip()}")')
            if str(r.get("source", "")).upper() == "PPR"]
    if not recs:
        # 短语段无 PPR 命中（含短语命中但全是 src=MED 期刊的情况）→ 内容词 AND 兜底
        toks = _title_tokens(title)
        if len(toks) >= 3:  # 内容词太少退化为短语结果（空）
            q2 = "(" + " AND ".join(f"TITLE:{w}" for w in toks) + ")"
            recs = [r for r in _run(q2)
                    if str(r.get("source", "")).upper() == "PPR"]
    out = []
    for rec in recs:
        # 此处 recs 已确保全部为 PPR（软过滤混入的 src=MED CSHL 期刊——DOI 也 10.1101
        # 前缀，如 gad.*/cshperspect.*——已在上面两段各滤除一次）
        # Europe PMC 全文仓未必收录该预印本 PDF：fullTextUrl 常只有 documentStyle=doi
        # （isOpenAccess=N）。此时 pdf_url 留空，由下载层官网直链兜底（_cscl_official_pdf，
        # bioRxiv 可无头直下、medRxiv 403 如实失败），保证候选不漏。
        pdf_url = ""
        for ft in (rec.get("fullTextUrlList") or {}).get("fullTextUrl", []):
            if (ft.get("documentStyle") == "pdf"
                    and str(ft.get("availability", "")).lower().startswith("open")):
                pdf_url = ft.get("url")
                break
        # venue 判定：host 命中精确标注 bioRxiv/medRxiv；PPR 但 host 是 Europe PMC 代理
        # （europepmc.org/api/fulltextRepo）或缺失时按 DOI 前缀 10.1101（CSHL 双库）标模糊
        # biorxiv_medrxiv；其余 PPR 源（Research Square 10.21203 等）标 other → 被开关过滤。
        host = (urllib.parse.urlparse(pdf_url).hostname or "").lower() if pdf_url else ""
        doi = str(rec.get("doi", ""))
        if "medrxiv.org" in host:
            venue = "medrxiv"
        elif "biorxiv.org" in host:
            venue = "biorxiv"
        elif doi.startswith("10.1101"):
            venue = "biorxiv_medrxiv"
        else:
            venue = "other"
        # 解析作者（Europe PMC authorList 有序，第一作者即 [0]）用于同篇校验
        cand_authors = _lastnames_from_authors((rec.get("authorList") or {}).get("author", []))
        out.append({"doi": doi, "venue": venue,
                    "pdf_url": pdf_url, "authors": cand_authors})
    return out


def _arxiv_search(title: str) -> list:
    """arXiv API 按标题检索候选（返回 [{arxiv_id, pdf_url, authors}]）。

    两段式：ti:"完整短语" → 0 命中回退「内容词 AND」（ti:w1 AND ti:w2 ...）。
    """
    if not title or len(title.strip()) < 8:
        return []

    def _run(q_expr: str) -> str:
        url = (f"http://export.arxiv.org/api/query?search_query="
               f"{urllib.parse.quote(q_expr)}&max_results=5&sortBy=relevance")
        try:
            return _get(url, timeout=30).decode("utf-8", "ignore")
        except Exception:
            return ""

    def _parse(text: str) -> list:
        out = []
        # 解析 Atom <entry>：id 形如 http://arxiv.org/abs/2401.12345v1
        for m in re.finditer(r"<entry>(.*?)</entry>", text, re.S):
            entry = m.group(1)
            idm = re.search(r"<id>(.*?)</id>", entry, re.S)
            if not idm:
                continue
            aid = idm.group(1).strip().rsplit("/", 1)[-1]  # 取末尾 arxiv id
            if not re.match(r"\d{4}\.\d{4,5}", aid):
                continue
            # 解析作者（<author><name> 末词为姓，有序，第一作者即 [0]）用于同篇校验
            cand_authors = []
            for am in re.finditer(r"<author>(.*?)</author>", entry, re.S):
                nm = re.search(r"<name>(.*?)</name>", am.group(1), re.S)
                if nm:
                    toks = nm.group(1).strip().split()
                    if toks:
                        cand_authors.append(_norm_lastname(toks[-1]))
            out.append({"arxiv_id": aid, "pdf_url": f"https://arxiv.org/pdf/{aid}",
                        "authors": cand_authors})
        return out

    out = _parse(_run(f'ti:"{title.strip()}"'))
    if not out:
        toks = _title_tokens(title)
        if len(toks) >= 3:
            out = _parse(_run(" AND ".join(f"ti:{w}" for w in toks)))
    return out


def _try_preprint_fallback(title: str | None, out_path: str,
                           preprint: dict, doi: str = "",
                           orig_authors: list | None = None,
                           allow_coze: bool = True) -> tuple:
    # ⚠️ 2026-09-06 起停用：本地 PPR/arXiv 预印本回退已上移 coze publisher_pdf
    #    服务端补充链（Unpaywall → PPR → arXiv，作者级同篇校验）。本函数与下方
    #    _epmc_preprint_search / _arxiv_search 等保留仅为历史参考，不再被 fetch_pdf 调用。
    """主路径失败（付费墙/无法下载）后的预印本回退。命中即下载作为候选。

    preprint: {biorxiv:bool, medrxiv:bool, arxiv:bool}（opt-in 开关）。
    orig_authors: 原始文献作者归一化姓氏列表（用于同篇校验，宁可缺漏不能弄错）。
    allow_coze: 本地 urllib 全败（medRxiv 官网 403 / bioRxiv 频控 429 等）时，
                委托 ct-search 服务端真实浏览器（source=publisher_pdf）取 PDF。
    Returns: (ok, info)  —— 命中返回 ok=True, via=preprint_fallback, venue 标注来源 + author_check 结果。
    """
    wb = preprint.get("biorxiv")
    wm = preprint.get("medrxiv")
    wa = preprint.get("arxiv")
    if not (wb or wm or wa):
        return False, {}
    if not title:
        title = _title_from_doi(doi)
    if not title:
        return False, {"src": None, "via": "preprint_skip",
                       "error": "无标题，无法检索预印本（需 study.title 或 DOI 可解析）"}
    # 宁可缺漏：无原始文献作者可校验 → 不下载任何预印本候选（不能弄错）
    if not orig_authors:
        return False, {"src": None, "via": "preprint_skip",
                       "error": "无原始文献作者可校验（需 study.authors / --authors / DOI 可 Crossref 反查），"
                                "按「不能弄错」原则跳过预印本回退"}
    candidates = []
    if wb or wm:
        for c in _epmc_preprint_search(title):
            v = c["venue"]
            # biorxiv/medrxiv 精确命中各自开关；biorxiv_medrxiv（CSHL 模糊）任一开关即放行
            if (v == "biorxiv" and wb) or (v == "medrxiv" and wm) \
                    or (v == "biorxiv_medrxiv" and (wb or wm)):
                candidates.append(("epmc", v, c["pdf_url"], c.get("authors") or [],
                                   c.get("doi") or ""))
    if wa:
        for c in _arxiv_search(title):
            candidates.append(("arxiv", "arxiv", c["pdf_url"], c.get("authors") or [], ""))
    rejected = []  # (venue, reason) 记录被作者校验丢弃的候选，供 info 审计
    for src_label, venue, pdf_url, cand_authors, cdoi in candidates:
        passed, reason = _author_check(orig_authors, cand_authors)
        if not passed:
            rejected.append((venue, reason))
            continue
        # 预印本落盘到独立候选文件，避免覆盖/混淆已尝试的主路径
        base, _ = os.path.splitext(out_path)
        cand_path = f"{base}__preprint_{venue}.pdf"
        if consent_aware_download(pdf_url, cand_path) or download(pdf_url, cand_path):
            return True, {"src": src_label, "via": "preprint_fallback", "venue": venue,
                          "pdf_path": cand_path,
                          "author_check": "passed", "author_note": reason,
                          "note": "付费墙文献的预印本候选（非发表版全文，作者校验通过）"}
        # 官网直链兜底：Europe PMC 未存全文的 CSHL 预印本（bioRxiv 无头可下；
        # medRxiv 官网 403 会如实失败——反爬需浏览器通道）
        if venue in ("biorxiv", "biorxiv_medrxiv") and cdoi:
            off = _cscl_official_pdf(cdoi)
            if off and off != pdf_url:
                if consent_aware_download(off, cand_path) or download(off, cand_path):
                    return True, {"src": "official", "via": "preprint_fallback", "venue": venue,
                                  "pdf_path": cand_path,
                                  "author_check": "passed", "author_note": reason,
                                  "note": "付费墙文献的预印本候选（官网直链，作者校验通过）"}
                # 官网仍失败（medRxiv 403 / bioRxiv 频控 429）→ coze 服务端浏览器
                if allow_coze:
                    cinfo = _coze_pdf_download(cdoi, cand_path)
                    if cinfo:
                        cinfo.update({"via": "preprint_fallback", "venue": venue,
                                      "pdf_path": cand_path, "author_check": "passed",
                                      "author_note": reason,
                                      "note": "付费墙文献的预印本候选（coze 浏览器通道，作者校验通过）"})
                        return True, cinfo
    if not candidates:
        return False, {"src": None, "via": "preprint_none",
                       "error": "未检索到预印本候选（标题在 PPR/arXiv 无命中或候选无开放 PDF）"}
    return False, {"src": None, "via": "preprint_none",
                   "error": "预印本候选作者校验未通过（宁可缺漏，未下载不同篇的预印本）",
                   "rejected": rejected}


def fetch_pdf(doi: str, study=None, out_path=None, email: str = DEFAULT_EMAIL,
              allow_coze: bool = True, preprint: dict | None = None,
              authors: list | None = None) -> tuple:
    """统一全文下载入口（B2，2026-09-06 架构收敛）。

    流程（多通道算法一律上移 coze，本地技能端只做调用）：
      1) 委托 ct-search.coze.site/run 的 source=publisher_pdf —— 服务端含
         A 路径(OA/PMC/EPMC) + A 补充链(Unpaywall → PPR bioRxiv/medRxiv → arXiv，
         作者级同篇校验) + 可选浏览器 B（默认关）；
      2) coze 不可用（未配置/未升级/调用失败）→ 本地降级：open_access_url /
         Unpaywall / Europe PMC PMC-OA 直下（原本地解析保留为离线降级通道）；
      3) 本地 PPR/arXiv 预印本回退已停用（能力上移服务端补充链，本地不再实现）。
    主路径仍失败（付费墙 / 确实无法下载）→ 如实返回失败。

    Args:
        preprint: 兼容保留参数。语义自 2026-09-06 起并入服务端补充链
                  （本地不再执行预印本下载），仅用于错误文案提示。
        authors: 原始文献作者（任意表示，将归一化为姓氏列表）。服务端补充链会
                 自行反查元数据做同篇校验；本地保留仅供降级诊断/旧契约。
    Returns: (ok:bool, info:dict)  —— info 含 src/via/venue/review_tag/error 诊断键。
    """
    if out_path is None:
        out_path = os.path.join("pdfs", f"{_sanitize(doi)}.pdf")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    # 2026-09-06 起：同篇校验由服务端补充链按 DOI 反查元数据完成，本地不再为
    # 预印本回退预取 title/authors（省去 Crossref 反查请求）；保留参数供旧契约兼容。
    url, src = _resolve_pdf_url(doi, study)  # 预解析：仅作 coze 断线降级与诊断
    if allow_coze:
        # ── 1) 主路径：委托 coze（服务端含 A 路径 + Unpaywall/PPR/arXiv 补充链）──
        cinfo = _coze_pdf_download(doi, out_path)
        if cinfo:
            return True, cinfo
        main_via, main_err = "coze_failed", (
            "coze publisher_pdf 未返回 PDF（端点未升级/补充链未命中）——"
            "服务端含 A 路径 + Unpaywall/PPR/arXiv 补充链（2026-09-06 上移）")
        # ── 2) coze 不可用 → 本地降级（仅直下，不实现多通道算法）──
        if url and consent_aware_download(url, out_path):
            return True, {"src": src, "via": "local_fallback"}
    else:
        main_via, main_err = "no_coze", "coze 委托关闭"
        if url and consent_aware_download(url, out_path):
            return True, {"src": src, "via": "local"}
    # ── 3) 本地 PPR/arXiv 预印本回退已停用（能力上移服务端补充链）；付费墙/无法下载如实失败 ──
    if preprint:
        main_err = f"{main_err}（preprint 开关已并入服务端补充链，本地不再另行回退）"
    return False, {"src": src, "via": main_via, "error": main_err}


def main() -> int:
    ap = argparse.ArgumentParser(description="DOI/PMID → 开放获取全文 PDF 批量下载（opt-in）")
    ap.add_argument("idtype", choices=["doi", "pmid"], help="ID 类型")
    ap.add_argument("ids", nargs="*", help="DOI 或 PMID（也可 --input 文件逐行读取）")
    ap.add_argument("--input", help="从文件逐行读取 ID（每行一个）")
    ap.add_argument("--out", default="pdfs", help="输出目录（默认 ./pdfs）")
    ap.add_argument("--email", default=DEFAULT_EMAIL, help="Unpaywall 查询邮箱")
    # 预印本回退（兼容保留，2026-09-06 起由服务端 publisher_pdf 补充链统一执行：
    # Unpaywall → PPR bioRxiv/medRxiv → arXiv，作者级同篇校验；本地不再另行回退。
    # 传这些开关仅作提示/审计，不影响本地下载路径。）
    ap.add_argument("--with-biorxiv", action="store_true",
                    help="(兼容) bioRxiv 预印本回退已并入服务端补充链，本地自动生效")
    ap.add_argument("--with-medrxiv", action="store_true",
                    help="(兼容) medRxiv 预印本回退已并入服务端补充链，本地自动生效")
    ap.add_argument("--with-arxiv", action="store_true",
                    help="(兼容) arXiv 预印本回退已并入服务端补充链，本地自动生效")
    ap.add_argument("--authors", default=None,
                    help="原始文献作者（逗号分隔，如 'Vaswani, Shazeer, Parmar'）；"
                         "用于预印本同篇校验，缺省自动从 Crossref 反查 DOI 作者")
    a = ap.parse_args()

    ids = list(a.ids)
    if a.input:
        with open(a.input, encoding="utf-8") as f:
            ids += [ln.strip() for ln in f if ln.strip()]
    if not ids:
        ap.error("请提供至少一个 ID（或 --input 文件）")
    os.makedirs(a.out, exist_ok=True)
    preprint = {"biorxiv": a.with_biorxiv, "medrxiv": a.with_medrxiv, "arxiv": a.with_arxiv}
    preprint_on = any(preprint.values())

    print(f"== 开始下载 {len(ids)} 篇全文（{a.idtype}，目标 {a.out}）=="
          + ("  [预印本回退: bioRxiv=%s medRxiv=%s arXiv=%s]" % (
              a.with_biorxiv, a.with_medrxiv, a.with_arxiv) if preprint_on else ""))
    ok, fail = 0, 0
    for i, ident in enumerate(ids, 1):
        try:
            if a.idtype == "pmid":
                # PMID 路径：PMC 直连（无反爬，不经 coze 委托；预印本回退暂不覆盖 pmid）
                pdf_url = pmid_to_pdf(ident)
                if not pdf_url:
                    print(f"[{i}/{len(ids)}] {ident}  → 无开放获取全文（跳过）")
                    fail += 1
                    continue
                out = os.path.join(a.out, f"{_sanitize(ident)}.pdf")
                if download(pdf_url, out):
                    print(f"[{i}/{len(ids)}] {ident}  → OK  {out}")
                    ok += 1
                else:
                    print(f"[{i}/{len(ids)}] {ident}  → 下载失败或文件过小（{pdf_url}）")
                    fail += 1
                continue
            # DOI 路径：走统一入口 fetch_pdf（open_access_url 优先 + 反爬委托 coze + 预印本回退）
            out = os.path.join(a.out, f"{_sanitize(ident)}.pdf")
            cli_authors = None
            if a.authors:
                cli_authors = _lastnames_from_authors(
                    [x.strip() for x in a.authors.split(",") if x.strip()])
            ok_flag, info = fetch_pdf(ident, out_path=out, email=a.email,
                                      preprint=preprint, authors=cli_authors)
            if ok_flag:
                via = info.get("via")
                if via == "preprint_fallback":
                    print(f"[{i}/{len(ids)}] {ident}  → 预印本候选 OK ({info.get('venue')}, "
                          f"作者校验:{info.get('author_note')})  {info.get('pdf_path')}  "
                          f"⚠ 非发表版全文")
                else:
                    print(f"[{i}/{len(ids)}] {ident}  → OK ({via})  {out}")
                ok += 1
            else:
                # 打印被作者校验丢弃的候选，便于审计（宁可缺漏）
                rej = info.get("rejected")
                extra = ""
                if rej:
                    extra = " [作者校验拒绝: " + ", ".join(f"{v}={r}" for v, r in rej) + "]"
                print(f"[{i}/{len(ids)}] {ident}  → 失败: {info.get('error')}{extra}")
                fail += 1
        except Exception as e:
            print(f"[{i}/{len(ids)}] {ident}  → 错误: {e}")
            fail += 1
    print(f"== 完成：成功 {ok} / 失败 {fail} ==")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
