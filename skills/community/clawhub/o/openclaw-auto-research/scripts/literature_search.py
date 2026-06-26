#!/usr/bin/env python3
"""literature_search.py — arXiv + Semantic Scholar 双源文献搜索脚本

独立可运行，零外部依赖（仅 stdlib）。供 auto-research skill 的 Stage 4 使用。

用法:
    python3 literature_search.py \
        --queries "LLM agent self-evolution" "prompt optimization MCTS" \
        --output ./stage-4/ \
        --year-min 2023 \
        --limit 30

产出:
    <output>/candidates.jsonl   — 每行一个 JSON（去重后）
    <output>/references.bib     — BibTeX 引用库

架构灵感: AutoResearchClaw/researchclaw/literature/
  - arxiv_client.py: arXiv API + 断路器
  - semantic_scholar.py: S2 API + 断路器 + 限流
  - search.py: 多源合并 + DOI/arXiv ID/模糊标题去重
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field, asdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("literature_search")

# ============================================================
# Data Model
# ============================================================

@dataclass
class Paper:
    title: str = ""
    authors: list[str] = field(default_factory=list)
    year: int = 0
    abstract: str = ""
    venue: str = ""
    citation_count: int = 0
    doi: str = ""
    arxiv_id: str = ""
    url: str = ""
    source: str = ""  # "arxiv" | "semantic_scholar"

    def to_jsonl(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    def to_bibtex(self) -> str:
        """生成 BibTeX 条目"""
        key = self.arxiv_id or self.doi or re.sub(r"\W+", "_", self.title[:30]).lower()
        first_author = self.authors[0].split()[-1] if self.authors else "unknown"
        cite_key = f"{first_author}{self.year}_{key}"
        cite_key = re.sub(r"[^a-zA-Z0-9_]", "", cite_key)

        lines = [f"@article{{{cite_key},"]
        lines.append(f'  title = {{{self.title}}},')
        if self.authors:
            lines.append(f'  author = {{{" and ".join(self.authors)}}},')
        if self.year:
            lines.append(f"  year = {{{self.year}}},")
        if self.venue:
            lines.append(f'  journal = {{{self.venue}}},')
        if self.doi:
            lines.append(f'  doi = {{{self.doi}}},')
        if self.arxiv_id:
            lines.append(f'  eprint = {{{self.arxiv_id}}},')
            lines.append("  archiveprefix = {arXiv},")
        if self.url:
            lines.append(f'  url = {{{self.url}}},')
        lines.append("}")
        return "\n".join(lines)


# ============================================================
# arXiv API Client (stdlib only, 参考 AutoResearchClaw)
# ============================================================

ARXIV_API = "https://export.arxiv.org/api/query"  # 必须 HTTPS（http 会 301）
ARXIV_NS = {"atom": "http://www.w3.org/2005/Atom"}
ARXIV_RATE_LIMIT = 5.0  # arXiv 要求 >= 3s，多查询场景用 5s 更安全

_arxiv_last_request = 0.0


def _arxiv_rate_limit():
    """遵守 arXiv 3s 限流"""
    global _arxiv_last_request
    now = time.monotonic()
    elapsed = now - _arxiv_last_request
    if elapsed < ARXIV_RATE_LIMIT:
        time.sleep(ARXIV_RATE_LIMIT - elapsed)
    _arxiv_last_request = time.monotonic()


def search_arxiv(
    query: str,
    *,
    limit: int = 50,
    year_min: int = 0,
    sort_by: str = "relevance",
) -> list[Paper]:
    """通过 arXiv Atom API 搜索论文。

    参考: AutoResearchClaw/researchclaw/literature/arxiv_client.py
    简化版: 无断路器，保留限流和重试。
    """
    _arxiv_rate_limit()

    sort_map = {
        "relevance": "relevance",
        "submitted_date": "submittedDate",
        "last_updated": "lastUpdatedDate",
    }
    params = {
        "search_query": f"all:{query}",
        "start": "0",
        "max_results": str(min(limit, 200)),
        "sortBy": sort_map.get(sort_by, "relevance"),
        "sortOrder": "descending",
    }
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"

    for attempt in range(3):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8")
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                wait = 10 * (attempt + 1)  # 10s, 20s, 30s — 比原来 3s 更保守
                log.warning("arXiv rate-limited (429), retry %d/3 in %ds", attempt + 1, wait)
                time.sleep(wait)
                continue
            log.warning("arXiv HTTP %d for query %r", exc.code, query)
            return []
        except (urllib.error.URLError, OSError) as exc:
            wait = 5 * (attempt + 1)
            log.warning("arXiv request failed (%s), retry %d/3 in %ds", exc, attempt + 1, wait)
            time.sleep(wait)
    else:
        log.error("arXiv search exhausted retries for: %s", query)
        return []

    # 解析 Atom XML
    papers: list[Paper] = []
    try:
        root = ET.fromstring(body)
    except ET.ParseError as exc:
        log.error("arXiv XML parse error: %s", exc)
        return []

    for entry in root.findall("atom:entry", ARXIV_NS):
        try:
            paper = _parse_arxiv_entry(entry)
            if year_min > 0 and paper.year < year_min:
                continue
            papers.append(paper)
        except Exception as exc:
            log.debug("Failed to parse arXiv entry: %s", exc)

    log.info("arXiv: %d papers for %r", len(papers), query)
    return papers


def _parse_arxiv_entry(entry: ET.Element) -> Paper:
    """解析单个 arXiv Atom entry 为 Paper"""
    def text(tag: str) -> str:
        el = entry.find(f"atom:{tag}", ARXIV_NS)
        return (el.text or "").strip() if el is not None else ""

    title = re.sub(r"\s+", " ", text("title"))
    abstract = re.sub(r"\s+", " ", text("summary"))

    authors = []
    for author_el in entry.findall("atom:author", ARXIV_NS):
        name_el = author_el.find("atom:name", ARXIV_NS)
        if name_el is not None and name_el.text:
            authors.append(name_el.text.strip())

    # 提取 arXiv ID
    entry_id = text("id")  # e.g. http://arxiv.org/abs/2303.11366v4
    arxiv_id = ""
    m = re.search(r"(\d{4}\.\d{4,5})", entry_id)
    if m:
        arxiv_id = m.group(1)

    # 年份
    published = text("published")  # e.g. 2023-03-20T17:59:59Z
    year = int(published[:4]) if len(published) >= 4 else 0

    # DOI (arXiv 偶尔有)
    doi = ""
    for link in entry.findall("atom:link", ARXIV_NS):
        href = link.get("href", "")
        if "doi.org" in href:
            doi = href.split("doi.org/")[-1] if "doi.org/" in href else ""

    # 主分类
    category = ""
    cat_el = entry.find("{http://arxiv.org/schemas/atom}primary_category")
    if cat_el is not None:
        category = cat_el.get("term", "")

    url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else entry_id

    return Paper(
        title=title,
        authors=authors,
        year=year,
        abstract=abstract,
        venue=category,
        citation_count=0,
        doi=doi,
        arxiv_id=arxiv_id,
        url=url,
        source="arxiv",
    )


# ============================================================
# Semantic Scholar API Client (stdlib only, 参考 AutoResearchClaw)
# ============================================================

S2_API = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_FIELDS = "paperId,title,abstract,year,venue,citationCount,authors,externalIds,url"
S2_RATE_LIMIT = 1.5  # 保守限流（免费 tier 1 req/s）

_s2_last_request = 0.0
_s2_consecutive_429 = 0


def search_semantic_scholar(
    query: str,
    *,
    limit: int = 30,
    year_min: int = 0,
    api_key: str = "",
) -> list[Paper]:
    """通过 Semantic Scholar Graph API 搜索论文。

    参考: AutoResearchClaw/researchclaw/literature/semantic_scholar.py
    简化版: 保留限流和重试，简化断路器为计数器。
    """
    global _s2_last_request, _s2_consecutive_429

    # 断路器: 连续 3 次 429 后跳过
    if _s2_consecutive_429 >= 3:
        log.warning("S2 circuit breaker OPEN (3 consecutive 429s), skipping")
        return []

    # 限流
    now = time.monotonic()
    rate = 0.3 if api_key else S2_RATE_LIMIT
    elapsed = now - _s2_last_request
    if elapsed < rate:
        time.sleep(rate - elapsed)
    _s2_last_request = time.monotonic()

    params = {
        "query": query,
        "limit": str(min(limit, 100)),
        "fields": S2_FIELDS,
    }
    if year_min > 0:
        params["year"] = f"{year_min}-"

    url = f"{S2_API}?{urllib.parse.urlencode(params)}"

    headers: dict[str, str] = {"Accept": "application/json"}
    if api_key:
        headers["x-api-key"] = api_key

    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
            _s2_consecutive_429 = 0  # 成功，重置断路器
            break
        except urllib.error.HTTPError as exc:
            if exc.code == 429:
                _s2_consecutive_429 += 1
                wait = min(2 ** (attempt + 1) + 1, 60)
                log.warning("S2 rate-limited (429), retry %d/3 in %ds", attempt + 1, wait)
                time.sleep(wait)
                continue
            log.warning("S2 HTTP %d for query %r", exc.code, query)
            return []
        except (urllib.error.URLError, OSError, json.JSONDecodeError) as exc:
            wait = 3 * (attempt + 1)
            log.warning("S2 request failed (%s), retry %d/3 in %ds", exc, attempt + 1, wait)
            time.sleep(wait)
    else:
        log.error("S2 search exhausted retries for: %s", query)
        return []

    raw = body.get("data", [])
    if not isinstance(raw, list):
        return []

    papers: list[Paper] = []
    for item in raw:
        try:
            papers.append(_parse_s2_paper(item))
        except Exception:
            log.debug("Failed to parse S2 paper: %s", item)

    log.info("S2: %d papers for %r", len(papers), query)
    return papers


def _parse_s2_paper(item: dict[str, Any]) -> Paper:
    """解析 S2 JSON entry 为 Paper"""
    ext_ids = item.get("externalIds") or {}
    authors_raw = item.get("authors") or []
    authors = [a.get("name", "") for a in authors_raw if isinstance(a, dict)]

    return Paper(
        title=(item.get("title") or "").strip(),
        authors=authors,
        year=int(item.get("year") or 0),
        abstract=(item.get("abstract") or "").strip(),
        venue=(item.get("venue") or "").strip(),
        citation_count=int(item.get("citationCount") or 0),
        doi=(ext_ids.get("DOI") or "").strip(),
        arxiv_id=(ext_ids.get("ArXiv") or "").strip(),
        url=(item.get("url") or "").strip(),
        source="semantic_scholar",
    )


# ============================================================
# 多源合并 + 去重 (参考 AutoResearchClaw/literature/search.py)
# ============================================================

def _normalize_title(title: str) -> str:
    """标准化标题用于模糊匹配"""
    return re.sub(r"[^a-z0-9 ]", "", title.lower()).strip()


def _titles_match(a: str, b: str, threshold: float = 0.85) -> bool:
    """模糊标题匹配（SequenceMatcher ratio）"""
    na, nb = _normalize_title(a), _normalize_title(b)
    if not na or not nb:
        return False
    return SequenceMatcher(None, na, nb).ratio() >= threshold


def deduplicate(papers: list[Paper]) -> list[Paper]:
    """三级去重: DOI → arXiv ID → 模糊标题

    参考: AutoResearchClaw 的去重策略（DOI → arXiv ID → fuzzy title match）
    当两篇论文匹配时，保留引用数更高的版本。
    """
    seen_doi: dict[str, int] = {}
    seen_arxiv: dict[str, int] = {}
    seen_titles: list[tuple[str, int]] = []  # (normalized_title, index)
    result: list[Paper] = []

    for paper in papers:
        # Level 1: DOI 去重
        if paper.doi:
            if paper.doi in seen_doi:
                existing_idx = seen_doi[paper.doi]
                if paper.citation_count > result[existing_idx].citation_count:
                    result[existing_idx] = paper
                continue
            seen_doi[paper.doi] = len(result)

        # Level 2: arXiv ID 去重
        if paper.arxiv_id:
            if paper.arxiv_id in seen_arxiv:
                existing_idx = seen_arxiv[paper.arxiv_id]
                if paper.citation_count > result[existing_idx].citation_count:
                    result[existing_idx] = paper
                continue
            seen_arxiv[paper.arxiv_id] = len(result)

        # Level 3: 模糊标题去重
        dup = False
        for seen_title, existing_idx in seen_titles:
            if _titles_match(paper.title, seen_title):
                if paper.citation_count > result[existing_idx].citation_count:
                    result[existing_idx] = paper
                dup = True
                break
        if dup:
            continue

        idx = len(result)
        if paper.doi:
            seen_doi[paper.doi] = idx
        if paper.arxiv_id:
            seen_arxiv[paper.arxiv_id] = idx
        seen_titles.append((_normalize_title(paper.title), idx))
        result.append(paper)

    return result


def search_papers(
    queries: list[str],
    *,
    limit_per_query: int = 30,
    year_min: int = 0,
    s2_api_key: str = "",
) -> list[Paper]:
    """多查询 + 双源搜索 + 去重

    搜索顺序（参考原版优先级）: Semantic Scholar → arXiv
    S2 有引用数且限流更宽松，arXiv 补充最新 preprint。
    """
    all_papers: list[Paper] = []

    for i, query in enumerate(queries):
        log.info("=== Query %d/%d: %r ===", i + 1, len(queries), query)

        # Source 1: Semantic Scholar
        s2_papers = search_semantic_scholar(
            query, limit=limit_per_query, year_min=year_min, api_key=s2_api_key,
        )
        all_papers.extend(s2_papers)

        # Source 2: arXiv
        arxiv_papers = search_arxiv(
            query, limit=limit_per_query, year_min=year_min,
        )
        all_papers.extend(arxiv_papers)

    log.info("Total before dedup: %d papers", len(all_papers))
    deduped = deduplicate(all_papers)
    log.info("Total after dedup: %d papers", len(deduped))

    # 按引用数降序排列
    deduped.sort(key=lambda p: p.citation_count, reverse=True)
    return deduped


# ============================================================
# CLI 入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="arXiv + Semantic Scholar 双源文献搜索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 literature_search.py \\
      --queries "LLM agent self-evolution" "prompt optimization MCTS" \\
      --output ./stage-4/ --year-min 2023 --limit 30

  # 从 search_plan.yaml 读取查询词
  python3 literature_search.py \\
      --plan ./stage-3/search_plan.yaml \\
      --output ./stage-4/
        """,
    )
    parser.add_argument(
        "--queries", nargs="+", help="搜索查询词列表",
    )
    parser.add_argument(
        "--plan", type=str, help="search_plan.yaml 路径（自动提取查询词）",
    )
    parser.add_argument(
        "--output", type=str, default=".", help="输出目录 (default: .)",
    )
    parser.add_argument(
        "--year-min", type=int, default=0, help="最早年份过滤 (e.g. 2023)",
    )
    parser.add_argument(
        "--limit", type=int, default=30, help="每个查询每个源的最大结果数 (default: 30)",
    )
    parser.add_argument(
        "--s2-api-key", type=str, default="",
        help="Semantic Scholar API key (optional, 提高限流到 10 req/s)",
    )
    args = parser.parse_args()

    # 获取查询词
    queries: list[str] = []
    if args.plan:
        queries = _load_queries_from_plan(args.plan)
    if args.queries:
        queries.extend(args.queries)

    if not queries:
        log.error("No queries provided. Use --queries or --plan.")
        sys.exit(1)

    # 环境变量覆盖
    s2_key = args.s2_api_key or os.environ.get("S2_API_KEY", "")

    # 搜索
    papers = search_papers(
        queries,
        limit_per_query=args.limit,
        year_min=args.year_min,
        s2_api_key=s2_key,
    )

    # 写入输出
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # candidates.jsonl
    jsonl_path = output_dir / "candidates.jsonl"
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for paper in papers:
            f.write(paper.to_jsonl() + "\n")
    log.info("Wrote %d papers to %s", len(papers), jsonl_path)

    # references.bib
    bib_path = output_dir / "references.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        for paper in papers:
            f.write(paper.to_bibtex() + "\n\n")
    log.info("Wrote BibTeX to %s", bib_path)

    # 摘要统计
    arxiv_count = sum(1 for p in papers if p.source == "arxiv")
    s2_count = sum(1 for p in papers if p.source == "semantic_scholar")
    print(json.dumps({
        "total": len(papers),
        "sources": {"arxiv": arxiv_count, "semantic_scholar": s2_count},
        "queries": len(queries),
        "year_range": f"{args.year_min}-present" if args.year_min else "all",
        "output_dir": str(output_dir),
    }, indent=2))


def _load_queries_from_plan(plan_path: str) -> list[str]:
    """从 search_plan.yaml 提取查询词"""
    try:
        # 不依赖 PyYAML — 简单解析 YAML 列表
        queries = []
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 尝试用 PyYAML（如果可用）
        try:
            import yaml
            data = yaml.safe_load(content)
            if isinstance(data, dict):
                for key in ("primary_queries", "secondary_queries"):
                    items = data.get(key, [])
                    if isinstance(items, list):
                        queries.extend(str(q) for q in items if q)
            return queries
        except ImportError:
            pass

        # 回退: 正则提取 YAML 列表项
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("- ") and '"' in line:
                # 提取引号中的内容
                m = re.search(r'"([^"]+)"', line)
                if m:
                    queries.append(m.group(1))
            elif line.startswith("- ") and not line.startswith("- {"):
                # 无引号的简单值
                val = line[2:].strip().strip('"').strip("'")
                if val and not val.startswith("["):
                    queries.append(val)

        log.info("Loaded %d queries from %s", len(queries), plan_path)
        return queries

    except (OSError, ValueError) as exc:
        log.error("Failed to load plan from %s: %s", plan_path, exc)
        return []


if __name__ == "__main__":
    main()
