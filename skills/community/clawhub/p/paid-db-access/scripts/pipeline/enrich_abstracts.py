#!/usr/bin/env python3

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import sys

import sys, os




if sys.platform == "win32":

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

"""

统一摘要补全 · Unified Abstract Enrichment

==========================================



可插拔架构。每个数据库注册一个 Enricher，新增数据库只需写一个 enricher 并注册。



架构：



    merged_results.json

           │

           ▼

    ┌──────────────────────────────────────┐

    │  enrich_abstracts.py                 │

    │                                      │

    │  1. 按 _source_db 分组               │

    │  2. 查 ENRICHERS 注册表找对应 enricher │

    │  3. 调用 enricher.enrich(papers)     │

    │  4. 合回完整结果                      │

    └──────────────────────────────────────┘



Enricher 三类实现模式：

  - 🆓 缓存型  — paper-abstracts/ 本地文件命中，零开销（Tier 0）

  - API 型     — 有公开 API，批量 HTTP 调用取摘要（Tier 1: Semantic Scholar/OpenAlex）

  - Browser 型 — 无 API，AI 浏览器打开详情页预采集摘要（Tier 2：AI 用 browser.act evaluate 提取）

  - Builtin 型 — 搜索时已自带摘要，无需任何操作（如 IEEE）



--------------------------------------------------

🔌 如何新增数据库的摘要支持：

--------------------------------------------------



1. 在本文件 ENRICHERS 字典里加一行注册：



    ENRICHERS = {

        ...

        "acm": ACMEnricher(),   # ← 新增这一行

    }



2. 实现 ACMEnricher 类，继承 BaseEnricher，实现 enrich() 方法。



3. 同步更新 config.yaml（database 配置）+ SKILL.md（摘要获取说明）。



详细模板见本文件末尾的「新增 Enricher 模板」注释。



--------------------------------------------------

用法：

    # 标准流程（Tier 0 缓存 → Tier 1 免费 API → 文件持久化）

    python enrich_abstracts.py -i merged.json -o enriched.json



    # 附带浏览器预采集的摘要（Tier 2）

    python enrich_abstracts.py -i merged.json -o enriched.json \

        --browser-abstracts ev_abstracts.json



    # 不传参数 → 纯透传（所有论文原样输出）

    python enrich_abstracts.py -i merged.json -o enriched.json

"""



import argparse

import json

import sys

import time

import urllib.request

import urllib.parse

import urllib.error

import re

import os

from abc import ABC, abstractmethod

from pathlib import Path



from utils.doi_utils import normalize as _norm_doi, extract as _extract_doi, to_filename as _doi_to_filename, title_hash as _title_hash, doc_id_filename as _doc_id_filename, extract_doc_id as _extract_doc_id

from utils.pipeline_schema import validate, report, stamp, check_version, PIPELINE_VERSION



# ---------------------------------------------------------------------------

# Enricher 基类

# ---------------------------------------------------------------------------



class BaseEnricher(ABC):

    """

    摘要补全器的抽象基类。



    子类必须实现：

      - db_key:    str         数据库标识（与 _source_db 中的值匹配）

      - source:    str         摘要来源类型 "api" | "browser" | "builtin"

      - enrich():  list[dict] → list[dict]  补全摘要，返回同长度的论文列表

    """



    db_key: str

    source: str  # "api" | "browser" | "builtin"



    @abstractmethod

    def enrich(self, papers: list[dict], **kwargs) -> list[dict]:

        """接收论文列表，原地补全 abstract 字段，返回同一列表。"""

        ...



    @property

    def needs_api_key(self) -> bool:

        """是否需要 --api-key 参数。"""

        return self.source == "api"



    @property

    def needs_browser_abstracts(self) -> bool:

        """是否需要 --browser-abstracts 参数（预采集的详情页摘要 JSON）。"""

        return self.source == "browser"



    def describe(self) -> str:

        """一行描述，供日志输出。"""

        return f"{self.db_key} ({self.source})"





# ---------------------------------------------------------------------------

# Browser 型 Enricher — 需要浏览器打开详情页取摘要

# ---------------------------------------------------------------------------



class BrowserEnricher(BaseEnricher):

    """

    无公开摘要 API 的数据库，需预先在浏览器中打开详情页获取摘要。



    工作流（由 AI 执行）：

      1. 对每篇论文，browser.navigate 到详情页 URL

      2. 运行对应数据库的 detail extractor（如 engineering_village_detail.js）

      3. 收集返回的 JSON，组成数组保存为文件

      4. 用 --browser-abstracts 传入该文件



    子类只需指定 db_key 和 matching_fields（用于匹配回原论文的字段）。

    """



    source = "browser"



    def __init__(self, db_key: str, matching_fields: list[str] | None = None):

        """

        matching_fields: 预采集的 abstracts 和原始 papers 之间的匹配字段。

                         默认 ["docId", "title"]，先精确 docId 再模糊 title。

        """

        self.db_key = db_key

        self.matching_fields = matching_fields or ["docId", "title"]



    def enrich(self, papers: list[dict], **kwargs) -> list[dict]:

        abstracts_path = kwargs.get("browser_abstracts")

        if not abstracts_path or not Path(abstracts_path).exists():

            print(f"  ⚠️  [{self.db_key}] No browser abstracts file — "

                  f"skipping {len(papers)} papers")

            return papers



        with open(abstracts_path, "r", encoding="utf-8") as f:

            abstracts_list = json.load(f)



        if not isinstance(abstracts_list, list):

            print(f"  ⚠️  [{self.db_key}] Invalid abstracts format (expected JSON array)")

            return papers



        # Build lookup: field_name → {value: abstract_data}

        lookups = {}

        for field in self.matching_fields:

            lookups[field] = {}

            for a in abstracts_list:

                val = a.get(field, "")

                if val:

                    lookups[field][self._normalize(val)] = a



        matched = 0

        for paper in papers:

            abstract_data = self._match(paper, lookups)

            if abstract_data:

                abs_text = abstract_data.get("abstract", "")

                if abs_text:

                    paper["abstract"] = abs_text

                # 顺便补其他丰富字段

                for extra in ["controlledTerms", "uncontrolledTerms",

                              "classCodes", "conference", "issn", "publisher"]:

                    val = abstract_data.get(extra)

                    if val:

                        paper[extra] = val

                matched += 1



        print(f"  [{self.db_key}] {matched}/{len(papers)} matched with abstracts "

              f"(via {' → '.join(self.matching_fields)})")

        return papers



    def _match(self, paper: dict, lookups: dict) -> dict | None:

        """按 matching_fields 优先级逐一尝试匹配。"""

        for field in self.matching_fields:

            val = self._normalize(paper.get(field, ""))

            if not val:

                continue

            if field == "docId":

                # docId 精确匹配（不分词）

                if val in lookups[field]:

                    return lookups[field][val]

            else:

                # 其他字段先精确再模糊

                if val in lookups[field]:

                    return lookups[field][val]

                # 模糊标题匹配（token overlap ≥ 70%）

                best = None

                best_score = 0.0

                for nv, data in lookups[field].items():

                    score = self._title_similarity(val, nv)

                    if score > best_score and score >= 0.70:

                        best_score = score

                        best = data

                if best:

                    return best

        return None



    @staticmethod

    def _normalize(text: str) -> str:

        if not text:

            return ""

        t = text.lower()

        t = re.sub(r'[^\w\s]', ' ', t)

        t = re.sub(r'\s+', ' ', t).strip()

        return t



    @staticmethod

    def _title_similarity(t1: str, t2: str) -> float:

        tokens1 = set(BrowserEnricher._normalize(t1).split())

        tokens2 = set(BrowserEnricher._normalize(t2).split())

        if not tokens1 or not tokens2:

            return 0.0

        overlap = tokens1 & tokens2

        return len(overlap) / max(len(tokens1), len(tokens2))





# ---------------------------------------------------------------------------

# 🆓 免费源 Enricher — Semantic Scholar → OpenAlex 链式尝试

# ---------------------------------------------------------------------------



class FreeAPIEnricher(BaseEnricher):

    """

    Tier 1 免费摘要源。链式尝试：Semantic Scholar → OpenAlex。



    设计原则（与下载流程一致）：

      - 免费优先，不消耗付费 API 配额

      - 不依赖浏览器，纯 HTTP

      - 失败不阻断，静默降级到 Tier 2

      - 🔑 标题交叉验证：DOI 匹配后校验返回标题，防止误匹配



    速率限制：

      - Semantic Scholar: ~100 次/5 分钟（无 API Key），返回 429 自动降级

      - OpenAlex: 无速率限制，但响应较慢

    """



    # ══════════════════════════════════════════════════════════

    # 标题交叉验证阈值

    # ══════════════════════════════════════════════════════════

    MIN_TITLE_SIMILARITY = 0.60   # 低于此值 → 拒绝，回退到 Tier 2



    db_key = "__free__"

    source = "api"



    def enrich(self, papers: list[dict], **kwargs) -> list[dict]:

        delay = kwargs.get("delay", 3.0)  # 3.0s/req — SS 免费限额 100/5min (=20/min)，3s ≈ 20/min 安全

        timeout = kwargs.get("timeout", 10)



        enriched = 0

        rejected = 0   # 标题不匹配被拒绝

        ss_ok = 0

        oa_ok = 0



        for i, paper in enumerate(papers):

            if paper.get("abstract") and len(paper["abstract"]) > 50:

                enriched += 1

                continue



            doi = _extract_doi(paper)

            if not doi:

                # 🏷️ 无 DOI → 标记为必须走 Tier 2 详情页提取

                paper["_needs_tier2"] = True

                paper["_tier2_reason"] = "no_doi"

                continue



            orig_title = paper.get("title", "")



            # Tier 1a: Semantic Scholar

            result = self._fetch_semantic_scholar(doi, timeout)

            if result:

                returned_title = result.get("title", "")

                if self._verify_title(orig_title, returned_title):

                    paper["abstract"] = result["abstract"]

                    enriched += 1

                    ss_ok += 1

                    progress = "." if enriched % 5 != 0 else str(enriched)

                    print(f"\r    [{i+1}/{len(papers)}] SS hit {progress}", end="", flush=True)

                    if i < len(papers) - 1:

                        time.sleep(delay)

                    continue

                else:

                    rejected += 1

                    # 不 sleep，立即尝试 OpenAlex



            # Tier 1b: OpenAlex

            result = self._fetch_openalex(doi, timeout)

            if result:

                returned_title = result.get("title", "")

                if self._verify_title(orig_title, returned_title):

                    paper["abstract"] = result["abstract"]

                    enriched += 1

                    oa_ok += 1

                else:

                    rejected += 1

                    # 标题不匹配 → 标记 Tier 2

                    paper["_needs_tier2"] = True

                    paper["_tier2_reason"] = "title_mismatch"

            else:

                # DOI 有但 SS 和 OpenAlex 都无数据 → 标记 Tier 2

                paper["_needs_tier2"] = True

                paper["_tier2_reason"] = "doi_not_found_in_free_api"



            # 进度点（每5个打印数字）

            if i % 5 == 0:

                print(f"\r    [{i+1}/{len(papers)}] ...", end="", flush=True)



            if i < len(papers) - 1:

                time.sleep(delay)



        print(f"  [free] SemanticScholar={ss_ok} OpenAlex={oa_ok} "

              f"rejected(标题不匹配)={rejected} total_enriched={enriched}/{len(papers)}")

        return papers



    @staticmethod

    def _fetch_semantic_scholar(doi: str, timeout: int = 10,

                                 max_retries: int = 2) -> dict | None:

        """Semantic Scholar API — 免费，返回 {title, abstract} 或 None。



        速率限制: 无 API Key 时 ~1 req/sec。429 时自动退避重试（2s → 4s）。

        """

        url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}" \
              f"?fields=title,abstract"

        headers = {"Accept": "application/json"}



        last_error = None

        for attempt in range(max_retries + 1):

            try:

                req = urllib.request.Request(url, headers=headers)

                with urllib.request.urlopen(req, timeout=timeout) as resp:

                    data = json.loads(resp.read().decode("utf-8"))

                    abstract = data.get("abstract", "")

                    title = data.get("title", "")

                    if abstract and len(abstract) > 50:

                        return {"title": title.strip(), "abstract": abstract.strip()}

                    return None

            except urllib.error.HTTPError as e:

                last_error = e

                if e.code == 404:

                    return None

                if e.code == 429 and attempt < max_retries:

                    wait = 2.0 * (attempt + 1)  # 2s, 4s

                    time.sleep(wait)

                    continue

                return None

            except Exception:

                return None



        return None



    @staticmethod

    def _fetch_openalex(doi: str, timeout: int = 10) -> dict | None:

        """OpenAlex API — 免费，返回 {title, abstract} 或 None。"""

        url = f"https://api.openalex.org/works/doi:{doi}"

        try:

            req = urllib.request.Request(url, headers={"Accept": "application/json"})

            with urllib.request.urlopen(req, timeout=timeout) as resp:

                data = json.loads(resp.read().decode("utf-8"))

        except urllib.error.HTTPError as e:

            if e.code == 404:

                return None

            return None

        except Exception:

            return None



        title = data.get("title", "")

        inv_idx = data.get("abstract_inverted_index")

        if not inv_idx or not isinstance(inv_idx, dict):

            return None



        try:

            words = {}

            for word, positions in inv_idx.items():

                for pos in positions:

                    words[pos] = word

            abstract = " ".join(words[k] for k in sorted(words))

            if abstract and len(abstract) > 50:

                return {"title": title.strip(), "abstract": abstract.strip()}

        except Exception:

            pass



        return None



    @classmethod

    def _verify_title(cls, orig_title: str, returned_title: str) -> bool:

        """交叉验证：源论文标题 vs API 返回标题。低于阈值 → 拒绝。"""

        if not orig_title or not returned_title:

            return False

        # 标准化

        t1 = re.sub(r'[^\w\s]', ' ', orig_title.lower())

        t1 = re.sub(r'\s+', ' ', t1).strip()

        t2 = re.sub(r'[^\w\s]', ' ', returned_title.lower())

        t2 = re.sub(r'\s+', ' ', t2).strip()

        # Token overlap

        tokens1 = set(t1.split())

        tokens2 = set(t2.split())

        if not tokens1 or not tokens2:

            return False

        # 双向：取较短的集合做分母，避免短文匹配长文

        overlap = tokens1 & tokens2

        score = len(overlap) / min(len(tokens1), len(tokens2))

        return score >= cls.MIN_TITLE_SIMILARITY



    @property

    def needs_api_key(self) -> bool:

        return False  # 免费，不需要 API Key



    @property

    def needs_browser_abstracts(self) -> bool:

        return False  # 纯 HTTP，不需要浏览器





# ---------------------------------------------------------------------------

# 🔀 分层 Enricher — Tier 1 (免费) → Tier 2 (付费/浏览器) 链式回退

# ---------------------------------------------------------------------------



class TieredEnricher(BaseEnricher):

    """

    分层摘要补全：先跑免费源（Tier 1），再跑付费/浏览器源（Tier 2）。



    与下载流程的分层策略完全对应。

    """



    source = "tiered"



    def __init__(self, db_key: str, tiers: list[BaseEnricher]):

        self.db_key = db_key

        self.tiers = tiers



    def enrich(self, papers: list[dict], **kwargs) -> list[dict]:

        remaining = papers

        for tier in self.tiers:

            remaining = [p for p in papers

                         if not (_resolve_abstract(p)  # 检查 _abstract_file 或 inline

                                 and len(_resolve_abstract(p)) > 50)]

            if not remaining:

                break



            tier_kwargs = {**kwargs}

            if tier.needs_api_key:

                tier_kwargs["api_key"] = kwargs.get("api_key")

            if tier.needs_browser_abstracts:

                tier_kwargs["browser_abstracts"] = kwargs.get("browser_abstracts")



            tier.enrich(remaining, **tier_kwargs)



        return papers



    @property

    def needs_api_key(self) -> bool:

        return any(t.needs_api_key for t in self.tiers)



    @property

    def needs_browser_abstracts(self) -> bool:

        return any(t.needs_browser_abstracts for t in self.tiers)





# ---------------------------------------------------------------------------

# 📋 Enricher 注册表 — 新增数据库在这里加一行

# ---------------------------------------------------------------------------



class CacheEnricher(BaseEnricher):

    """

    Tier 0 缓存检查 — 查询 paper-abstracts/ 目录，命中则跳过后续所有层级。



    两步验证：

      1. os.path.exists() — 文件存在

      2. 读第 1 行标题 → token overlap ≥ 30% — 内容匹配



    两步都是微秒级，几乎零开销。

    命中则自动设置 _abstract_file 引用，后续 Tier 直接跳过。

    """



    db_key = "__cache__"

    source = "builtin"



    # 标题匹配阈值（低阈值足以区分"同一篇"vs"完全无关"）

    TITLE_MATCH_THRESHOLD = 0.30



    @staticmethod

    def _normalize(text: str) -> str:

        if not text:

            return ""

        t = text.lower()

        t = re.sub(r'[^\w\s]', ' ', t)

        t = re.sub(r'\s+', ' ', t).strip()

        return t



    @staticmethod

    def _title_overlap(t1: str, t2: str) -> float:

        """两个标题的 token overlap 比率。"""

        tokens1 = set(CacheEnricher._normalize(t1).split())

        tokens2 = set(CacheEnricher._normalize(t2).split())

        if not tokens1 or not tokens2:

            return 0.0

        overlap = tokens1 & tokens2

        return len(overlap) / min(len(tokens1), len(tokens2))



    def _find_cache(self, doi: str, title: str, doc_id: str = "") -> str | None:

        """

        查找缓存文件并验证标题匹配。

        返回文件路径（匹配）或 None（不存在/内容错配）。



        查找优先级：docId > DOI > 标题哈希

        """

        abstract_dir = "memory/paper-abstracts"

        candidate = None



        # 1. docId 查找（IEEE 等无 DOI 但有 document ID 的库）

        if doc_id:

            # 试 IEEE docId 模式

            filepath = os.path.join(abstract_dir, _doc_id_filename(doc_id, "ieee"))

            if os.path.exists(filepath):

                candidate = filepath

            # 也试无前缀的纯数字文件名（兼容旧缓存）

            if not candidate:

                filepath = os.path.join(abstract_dir, f"{doc_id}.txt")

                if os.path.exists(filepath):

                    candidate = filepath



        # 2. DOI 查找

        if not candidate:

            doi_normalized = _norm_doi(doi) if doi else None

            if doi_normalized:

                filepath = os.path.join(abstract_dir, _doi_to_filename(doi_normalized))

                if os.path.exists(filepath):

                    candidate = filepath



        # 3. 标题哈希回退

        if not candidate and title:

            filepath = os.path.join(abstract_dir, _title_hash(title))

            if os.path.exists(filepath):

                candidate = filepath



        if not candidate:

            return None



        # 🔑 标题校验：解析结构化格式的 Title: 行，token overlap ≥ 阈值

        try:

            with open(candidate, "r", encoding="utf-8") as f:

                first_line = f.readline().strip()

        except (IOError, UnicodeDecodeError):

            return None



        # 解析 "Title: xxx" 格式

        cached_title = ""

        if first_line.startswith("Title:"):

            cached_title = first_line[6:].strip()

        else:

            # 兼容旧格式（纯标题第一行）

            cached_title = first_line



        if not cached_title or not title:

            return None  # 无法校验时拒绝匹配，走 Tier 1



        overlap = self._title_overlap(title, cached_title)

        if overlap >= self.TITLE_MATCH_THRESHOLD:

            return candidate

        return None



    def enrich(self, papers: list[dict], **kwargs) -> list[dict]:

        found = 0

        for paper in papers:

            # 已有 _abstract_file 且文件存在 → 跳过

            existing = paper.get("_abstract_file", "")

            if existing and os.path.exists(existing):

                found += 1

                continue

            # 已有足够长的 inline abstract → 跳过（会在 persist 阶段写文件）

            abs_text = paper.get("abstract", "")

            if abs_text and len(abs_text) > 50:

                found += 1

                continue

            # 查缓存（含标题校验）

            doi = (paper.get("doi") or "").strip()

            title = (paper.get("title") or "").strip()

            doc_id = _extract_doc_id(paper) or ""

            cache_path = self._find_cache(doi, title, doc_id)

            if cache_path:

                paper["_abstract_file"] = cache_path

                found += 1



        print(f"  [cache] {found}/{len(papers)} abstracts cached (Tier 0 hit)")

        return papers



    @property

    def needs_api_key(self) -> bool:

        return False



    @property

    def needs_browser_abstracts(self) -> bool:

        return False





# 共享实例（避免重复实例化）

_CACHE_ENRICHER = CacheEnricher()

_FREE_ENRICHER = FreeAPIEnricher()



ENRICHERS: dict[str, BaseEnricher] = {

    # --- Tiered（缓存 → 免费 API → AI 浏览器详情页回退）---

    "ieee":                TieredEnricher("ieee", [

                               _CACHE_ENRICHER,                        # Tier 0: 本地缓存

                               _FREE_ENRICHER,                          # Tier 1: 免费 API

                               BrowserEnricher("ieee", ["docId", "title"]),  # Tier 2: AI 浏览器预采集

                           ]),

    "scopus":              TieredEnricher("scopus", [

                               _CACHE_ENRICHER,

                               _FREE_ENRICHER,

                               BrowserEnricher("scopus", ["doi", "title"]),

                           ]),

    "engineering_village": TieredEnricher("engineering_village", [

                               _CACHE_ENRICHER,

                               _FREE_ENRICHER,

                               BrowserEnricher("engineering_village", ["docId", "title"]),

                           ]),

    "acm":                 TieredEnricher("acm", [

                               _CACHE_ENRICHER,

                               _FREE_ENRICHER,

                               BrowserEnricher("acm", ["doi", "title"]),

                           ]),



    # === 新增数据库模板 ===

    # "wos": TieredEnricher("wos", [

    #            _CACHE_ENRICHER,

    #            _FREE_ENRICHER,

    #            BrowserEnricher("wos", ["doi", "title"]),

    #        ]),

}





# ---------------------------------------------------------------------------

# 摘要文件持久化 · Abstract File Persistence

# ---------------------------------------------------------------------------



def _persist_abstracts_to_files(papers: list, abstracts_dir: str = "memory/paper-abstracts",

                                 clear_inline: bool = True) -> dict:

    """

    将每篇论文的摘要写出到独立文件，JSON 中替换为 _abstract_file 引用。



    返回统计：{"written": int, "skipped": int, "reused": int}

    - written: 新写出文件

    - skipped: 无摘要可写

    - reused: 文件已存在（跨查询复用！）

    """

    os.makedirs(abstracts_dir, exist_ok=True)

    written = 0

    skipped = 0

    reused = 0



    for paper in papers:

        abstract = (paper.get("abstract") or "").strip()

        if not abstract or len(abstract) < 50:

            skipped += 1

            continue



        # 生成文件名（优先 docId → DOI → 标题哈希回退）

        doc_id = _extract_doc_id(paper)

        doi = _extract_doi(paper)

        if doc_id:

            # 判断来源库

            sources = paper.get("_source_db", [])

            if not isinstance(sources, list):

                sources = [sources] if sources else []

            db = "ieee" if "ieee" in sources else "unknown"

            filename = _doc_id_filename(doc_id, db)

        elif doi:

            filename = _doi_to_filename(doi)

        else:

            title = paper.get("title") or "unknown"

            filename = _title_hash(title)



        filepath = os.path.join(abstracts_dir, filename)



        # 已存在 → 跳过写入，下次查询直接复用

        if os.path.exists(filepath):

            reused += 1

        else:

            # 🔑 统一模板 — 与 memory/paper-abstracts/ 现有格式一致

            content = (

                f"Title: {paper.get('title', '')}\n"

                f"Authors: {paper.get('authors', '')}\n"

                f"Year: {paper.get('year', '')}\n"

                f"Venue: {paper.get('venue', '')}\n"

                f"DOI: {paper.get('doi', '')}\n"

                f"Citations: {paper.get('citations', '')}\n"

                f"\nAbstract:\n{abstract}"

            )

            with open(filepath, "w", encoding="utf-8") as f:

                f.write(content)

            written += 1



        # 存储文件引用

        paper["_abstract_file"] = filepath

        if clear_inline:

            paper["abstract"] = ""



    print(f"  [Persist] {written} new + {reused} reused (cache) + "

          f"{skipped} skipped → {abstracts_dir}/")

    return {"written": written, "reused": reused, "skipped": skipped}





def _resolve_abstract(paper: dict) -> str:

    """

    解析论文摘要：优先从 _abstract_file 读文件 → 回退到 inline abstract 字段。



    文件格式（统一模板）：

      Title: ...

      Authors: ...

      ...

      Abstract:

      <摘要正文>



    提取规则：定位 "\nAbstract:\n" 标记，返回其后全部内容。

    兼容旧格式（无元数据头，全文即为摘要）。



    供 ai_rerank.py / ai_summarize.py / 任何需要读摘要的脚本使用。

    """

    abs_file = paper.get("_abstract_file", "")

    if abs_file and os.path.exists(abs_file):

        try:

            with open(abs_file, "r", encoding="utf-8") as f:

                content = f.read()

            # 定位 Abstract: 标记

            idx = content.find("\nAbstract:\n")

            if idx >= 0:

                return content[idx + len("\nAbstract:\n"):].strip()

            # 兼容旧格式：无 Abstract: 标记，全文即为摘要

            return content.strip()

        except (IOError, UnicodeDecodeError):

            pass



    # 回退：inline abstract（兼容旧 JSON）

    abstract = paper.get("abstract", "")

    if abstract and abstract != "[已缓存]" and len(abstract) > 20:

        return abstract.strip()



    return ""





# ---------------------------------------------------------------------------

# 主流程

# ---------------------------------------------------------------------------



def enrich_all(input_path: str, output_path: str | None = None,

               browser_abstracts: str | None = None,

               delay: float = 3.0, timeout: int = 10):

    """

    统一摘要补全入口。



    1. 加载论文 → 2. 按 _source_db 分组 → 3. 对每组调用对应 Enricher → 4. 输出

    """

    with open(input_path, "r", encoding="utf-8") as f:

        data = json.load(f)



    if isinstance(data, dict) and "papers" in data:

        papers = data["papers"]

    elif isinstance(data, list):

        papers = data

    else:

        print(f"[ERROR] Unrecognized input format: {type(data)}", file=sys.stderr)

        sys.exit(1)



    # --- 分组 ---

    groups: dict[str, list[dict]] = {}

    for p in papers:

        sources = p.get("_source_db", [])

        if not isinstance(sources, list):

            sources = [sources] if sources else []

        # 一篇论文可能来自多个库，取第一个有 enricher 的

        db = next((s for s in sources if s in ENRICHERS), "__unknown__")

        groups.setdefault(db, []).append(p)



    total = len(papers)



    # --- 日志：分组情况 ---

    parts = []

    for db, grp in groups.items():

        has_enricher = "✅" if db in ENRICHERS else "❌"

        parts.append(f"{has_enricher} {db}: {len(grp)}")

    print(f"[Enrich] {total} papers → {' | '.join(parts)}\n")



    # --- 逐组补全 ---

    for db, grp in groups.items():

        enricher = ENRICHERS.get(db)

        if enricher is None:

            print(f"  ⏭️  [{db}] No enricher registered — {len(grp)} papers pass-through")

            continue



        kwargs = {"delay": delay, "timeout": timeout}

        if enricher.needs_browser_abstracts:

            kwargs["browser_abstracts"] = browser_abstracts



        enricher.enrich(grp, **kwargs)



    # --- 汇总 ---

    with_abs = sum(1 for p in papers if p.get("abstract") and len(p["abstract"]) > 50)

    enriched_dbs = {db for db, grp in groups.items()

                    if db in ENRICHERS and ENRICHERS[db].source != "builtin"}



    print(f"\n{'─' * 50}")

    print(f"[Enrich] {with_abs}/{total} papers have abstracts")



    if enriched_dbs:

        print(f"[Enrich] Enriched from: {', '.join(sorted(enriched_dbs))}")



    unregistered = {db for db in groups if db not in ENRICHERS and db != "__unknown__"}

    if unregistered:

        print(f"[Enrich] ⚠️  No enricher for: {', '.join(sorted(unregistered))} "

              f"— add to ENRICHERS registry")



    # --- 摘要持久化到文件 ---

    persist_stats = _persist_abstracts_to_files(papers)



    with_abs = sum(1 for p in papers

                   if _resolve_abstract(p))



    print(f"\n{'─' * 50}")

    print(f"[Enrich] {with_abs}/{total} papers have abstracts "

          f"({persist_stats['written']} new files + {persist_stats['reused']} cached)")



    enriched_dbs = {db for db, grp in groups.items()

                    if db in ENRICHERS and ENRICHERS[db].source != "builtin"}

    if enriched_dbs:

        print(f"[Enrich] Enriched from: {', '.join(sorted(enriched_dbs))}")



    # --- 校验 + 报告 ---

    ok, issues = validate(papers, stage="enriched")

    if issues:

        report(issues, stage="enriched")



    # --- 输出 ---

    if isinstance(data, dict) and "papers" in data:

        data["papers"] = papers

        output_data = data

    else:

        output_data = {"papers": papers}



    if output_path:

        out = Path(output_path)

        out.parent.mkdir(parents=True, exist_ok=True)

        stamp(output_data, stage="enriched")

        with open(out, "w", encoding="utf-8") as f:

            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Saved to {out}")

    else:

        # NEVER print paper data (with abstracts) to stdout — AI context pollution.

        with_abs = sum(1 for p in papers if p.get("abstract") and len(p.get("abstract", "")) > 50)

        print(f"[Enrich] Use -o to write enriched results to file. "

              f"{with_abs}/{len(papers)} papers have abstracts.")





# ---------------------------------------------------------------------------

# CLI

# ---------------------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(

        description="Unified abstract enrichment — pluggable per-database enrichers",

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog=f"""

Registered enrichers:

{chr(10).join(f'  {k:22s} → {v.describe()}' for k, v in ENRICHERS.items())}



How to add a new database:

  1. Implement an Enricher subclass (API / Browser / Builtin)

  2. Add one line to the ENRICHERS dict at the top of this file

  3. Update config.yaml + SKILL.md



See file header for detailed template.

        """,

    )

    parser.add_argument("--input", "-i",

                        help="Input JSON (merged results or single-DB results)")

    parser.add_argument("--output", "-o",

                        help="Output file (default: stdout)")

    parser.add_argument("--browser-abstracts", "-b",

                        help="Pre-collected browser abstracts JSON for browser-type enrichers "

                             "(currently: EV, future: ACM, WoS)")

    parser.add_argument("--delay", "-d", type=float, default=3.0,

                        help="API call delay in seconds (default: 3.0 — <=100 req/5min for Semantic Scholar free tier)")

    parser.add_argument("--timeout", "-t", type=int, default=10,

                        help="HTTP timeout per request (default: 10)")

    parser.add_argument("--list", action="store_true",

                        help="List registered enrichers and exit")

    args = parser.parse_args()



    if args.list:

        print("Registered enrichers:\n")

        for key, enc in ENRICHERS.items():

            print(f"  {key:22s}  {enc.source:8s}  needs_api={enc.needs_api_key}  "

                  f"needs_browser={enc.needs_browser_abstracts}")

        return



    if not args.input:

        parser.error("--input/-i is required (use --list to see registered enrichers)")



    # Warn if missing args that some enrichers need

    browser_requesters = [k for k, e in ENRICHERS.items() if e.needs_browser_abstracts]



    if not args.browser_abstracts and browser_requesters:

        print(f"💡 Tip: --browser-abstracts not set. "

              f"Browser enrichers for {browser_requesters} will be skipped.\n")



    enrich_all(

        args.input, args.output,

        browser_abstracts=args.browser_abstracts,

        delay=args.delay,

        timeout=args.timeout,

    )





if __name__ == "__main__":

    main()





# ===========================================================================

# 📋 新增 Enricher 模板

# ===========================================================================

#

# 场景 A：新数据库有公开摘要 API（如 PubMed Entrez）

# ─────────────────────────────────────────────

#

#   class PubMedAPIEnricher(BaseEnricher):

#       db_key = "pubmed"

#       source = "api"

#

#       def enrich(self, papers, **kwargs):

#           api_key = kwargs.get("api_key")

#           if not api_key:

#               print(f"  ⚠️  No API key — skipping")

#               return papers

#           for paper in papers:

#               pmid = paper.get("pmid")

#               if pmid:

#                   # 调用 PubMed API 取摘要

#                   paper["abstract"] = self._fetch(pmid, api_key)

#           return papers

#

#   然后在 ENRICHERS 里加一行：

#       "pubmed": PubMedAPIEnricher(),

#

# 场景 B：新数据库无 API，需浏览器开详情页（如 ACM DL）

# ─────────────────────────────────────────────

#

#   直接复用 BrowserEnricher，指定匹配字段：

#

#       "acm": BrowserEnricher("acm", ["doi", "title"]),

#

#   然后确保：

#     1. extractors/acm_detail.js 存在（提取详情页摘要的脚本）

#     2. SKILL.md 里写了 AI 用浏览器逐篇打开详情页取摘要的工作流

#     3. 采集的 JSON 格式：每篇一个 {doi, title, abstract, ...}

#

# 场景 C：搜索时已带摘要，无需额外操作

# ─────────────────────────────────────

#

#       "ieee": BuiltinEnricher("ieee"),

#

#   就这么一行。

# ===========================================================================

