#!/usr/bin/env python3
"""
query_builder.py — 从结构化概念生成各数据库优化查询

AI 负责语义拆解（输出结构化 JSON），脚本负责语法拼装（数据库特定语法）。
两层各司其职，避免 AI 手拼查询时的随意性错误。

输入：结构化搜索概念 JSON
输出：各数据库的 URL/API 参数

用法：
  # 从文件读取概念
  python query_builder.py -c search_concept.json

  # 从 stdin 读取（AI 直接输出管道）
  echo '{"core_concepts":[...]}' | python query_builder.py -

  # 指定输出格式
  python query_builder.py -c search_concept.json --format urls      # URL 列表
  python query_builder.py -c search_concept.json --format commands   # 可执行命令
  python query_builder.py -c search_concept.json --format json       # JSON 输出

概念 JSON 格式：
{
  "core_concepts": ["autonomous scientific discovery", "AI automated research"],
  "synonyms": {
    "AI": ["LLM", "large language model", "artificial intelligence"],
    "research": ["scientific", "academic", "scholarly"]
  },
  "sub_topics": ["paper generation", "manuscript writing", "hypothesis generation"],
  "exclude": ["healthcare", "clinical", "medical imaging"],
  "year_range": "2023-2026",
  "databases": ["ieee", "scopus", "acm", "engineering_village"]
}
"""

import argparse
import json
import sys
import urllib.parse
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# 各数据库查询模板
# ---------------------------------------------------------------------------

class ScopusBuilder:
    """Scopus API 查询。语法：TITLE-ABS-KEY(phrase) + AND/OR/AND NOT"""

    @staticmethod
    def build(concept: dict) -> str:
        parts = []

        # 核心概念组（AND 连接）
        core_clauses = []
        for c in concept.get("core_concepts", []):
            core_clauses.append(f'TITLE-ABS-KEY("{c}")')
        if core_clauses:
            parts.append("(" + " OR ".join(core_clauses) + ")")

        # 同义词扩展
        syn_parts = []
        for term, syns in concept.get("synonyms", {}).items():
            syn_clause = " OR ".join(f'"{s}"' for s in [term] + syns)
            syn_parts.append(f"({syn_clause})")
        if syn_parts:
            parts.append("(" + " AND ".join(syn_parts) + ")")

        # 子主题（OR 连接）
        sub_clauses = []
        for st in concept.get("sub_topics", []):
            sub_clauses.append(f'TITLE-ABS-KEY("{st}")')
        if sub_clauses:
            parts.append("(" + " OR ".join(sub_clauses) + ")")

        # 排除项
        for ex in concept.get("exclude", []):
            parts.append(f'AND NOT TITLE-ABS-KEY("{ex}")')

        # 年份
        year = concept.get("year_range", "")
        if year:
            try:
                start_year = int(year.split('-')[0])
                parts.append(f"AND PUBYEAR > {start_year}")
            except (ValueError, IndexError):
                pass

        # 分离：普通部分（AND 连接）、后缀（年份等已带 AND）、排除（AND NOT）
        query_parts = [p for p in parts if not p.startswith("AND ")]
        suffix_parts = [p for p in parts if p.startswith("AND ") and not p.startswith("AND NOT")]
        exclude_parts = [p for p in parts if p.startswith("AND NOT")]

        query = " AND ".join(query_parts)
        if suffix_parts:
            query += " " + " ".join(suffix_parts)
        if exclude_parts:
            query += " " + " ".join(exclude_parts)

        return query.strip()


class IEEEBuilder:
    """IEEE Xplore URL 查询。语法：URL queryText 参数，OR 连接短语"""

    @staticmethod
    def build(concept: dict) -> str:
        terms = []

        # 核心概念
        for c in concept.get("core_concepts", []):
            terms.append(f'"{c}"')

        # 子主题
        for st in concept.get("sub_topics", []):
            terms.append(f'"{st}"')

        # 同义词（AND 组）
        for term, syns in concept.get("synonyms", {}).items():
            all_terms = [term] + syns
            syn_or = " OR ".join(f'"{s}"' for s in all_terms)
            terms.append(f"({syn_or})")

        # 排除
        for ex in concept.get("exclude", []):
            terms.append(f'NOT "{ex}"')

        query = " OR ".join(t for t in terms if not t.startswith("NOT "))
        not_terms = [t for t in terms if t.startswith("NOT ")]
        if not_terms:
            query += " " + " ".join(not_terms)

        encoded = urllib.parse.quote(query, safe='')
        url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={encoded}"

        year = concept.get("year_range", "")
        if year:
            url += f"&ranges={year.replace('-', '_')}_Year"

        return url


class ACMBuilder:
    """ACM Digital Library URL 查询。AllField 用引号短语 + AND 连接"""

    @staticmethod
    def build(concept: dict) -> str:
        clauses = []

        # 核心概念（引号短语）
        for c in concept.get("core_concepts", []):
            clauses.append(f'"{c}"')

        # 子主题（引号短语，OR 连接）
        subs = []
        for st in concept.get("sub_topics", []):
            subs.append(f'"{st}"')
        if subs:
            clauses.append("(" + " OR ".join(subs) + ")")

        # 同义词
        for term, syns in concept.get("synonyms", {}).items():
            all_terms = [f'"{s}"' for s in [term] + syns]
            clauses.append("(" + " OR ".join(all_terms) + ")")

        query = " AND ".join(clauses)

        # 排除
        for ex in concept.get("exclude", []):
            query += f' NOT "{ex}"'

        encoded = urllib.parse.quote(query, safe='')
        url = f"https://dl.acm.org/action/doSearch?AllField={encoded}&pageSize=25"

        year = concept.get("year_range", "")
        if year:
            try:
                after_year = int(year.split("-")[0])
                url += f"&AfterYear={after_year}"
            except (ValueError, IndexError):
                pass

        return url


class EVBuilder:
    """Engineering Village 搜索字符串（需用户手动输入或脚本填入搜索框）"""

    @staticmethod
    def build(concept: dict) -> str:
        parts = []

        # 核心概念
        core_phrases = []
        for c in concept.get("core_concepts", []):
            core_phrases.append(f'"{c}"')
        if core_phrases:
            parts.append("(" + " OR ".join(core_phrases) + ")")

        # 子主题
        sub_phrases = []
        for st in concept.get("sub_topics", []):
            sub_phrases.append(f'"{st}"')
        if sub_phrases:
            parts.append("(" + " OR ".join(sub_phrases) + ")")

        # 同义词
        for term, syns in concept.get("synonyms", {}).items():
            all_phrases = [f'"{s}"' for s in [term] + syns]
            parts.append("(" + " OR ".join(all_phrases) + ")")

        query = " AND ".join(parts)

        # 排除
        for ex in concept.get("exclude", []):
            query += f' NOT "{ex}"'

        return query.strip()


BUILDERS = {
    "scopus": ("Scopus API", ScopusBuilder.build),
    "ieee": ("IEEE Xplore", IEEEBuilder.build),
    "acm": ("ACM Digital Library", ACMBuilder.build),
    "engineering_village": ("Engineering Village", EVBuilder.build),
}


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def load_concept(input_path: str) -> dict:
    """从文件或 stdin 加载搜索概念。"""
    if input_path == "-":
        raw = sys.stdin.read()
    else:
        p = Path(input_path)
        if not p.exists():
            print(f"[ERROR] File not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        raw = p.read_text(encoding="utf-8")

    try:
        concept = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # 验证必要字段
    if not concept.get("core_concepts") and not concept.get("sub_topics"):
        print("[ERROR] At least one of 'core_concepts' or 'sub_topics' is required",
              file=sys.stderr)
        sys.exit(1)

    return concept


def validate_concept(concept: dict) -> list[str]:
    """验证并返回警告。"""
    warnings = []

    # 检查是否有任意查询要素
    has_content = (concept.get("core_concepts") or
                   concept.get("sub_topics") or
                   concept.get("synonyms"))
    if not has_content:
        warnings.append("No search terms: core_concepts, sub_topics, or synonyms required")

    # 检查 exclude 是否合理
    exclude = concept.get("exclude", [])
    if len(exclude) > 5:
        warnings.append(f"Many exclude terms ({len(exclude)}). May be too restrictive.")

    # 检查年份
    year = concept.get("year_range", "")
    if year and "-" not in year:
        warnings.append(f"year_range '{year}' should be format 'YYYY-YYYY'")

    # 检查数据库选择
    dbs = concept.get("databases", ["ieee", "scopus", "acm", "engineering_village"])
    for db in dbs:
        if db not in BUILDERS:
            warnings.append(f"Unknown database: '{db}'. Available: {list(BUILDERS.keys())}")

    return warnings


def build_all(concept: dict) -> dict:
    """为所有请求的数据库构建查询。"""
    dbs = concept.get("databases", list(BUILDERS.keys()))
    results = {}
    for db in dbs:
        if db in BUILDERS:
            name, builder = BUILDERS[db]
            try:
                query = builder(concept)
                results[db] = {
                    "name": name,
                    "query": query,
                    "type": "url" if db in ("ieee", "acm") else "string",
                    "note": _get_note(db),
                }
            except Exception as e:
                results[db] = {"name": name, "error": str(e)}
        else:
            results[db] = {"error": f"Unknown database: {db}"}
    return results


def _get_note(db: str) -> str:
    notes = {
        "scopus": "Use with scopus_search.py: python scripts/scopus_search.py -q \"<query>\" -k <key> -o results.json",
        "ieee": "Open in browser: browser.open(profile=\"openclaw\", url=\"<url>\")",
        "acm": "Open in browser: browser.open(profile=\"openclaw\", url=\"<url>\")",
        "engineering_village": "Type in search box on EV homepage, then evaluate with engineering_village.js",
    }
    return notes.get(db, "")


def print_urls(results: dict):
    """输出 URL 列表。"""
    for db, info in results.items():
        if "error" in info:
            print(f"# {db}: ERROR - {info['error']}")
        else:
            print(f"# {info['name']}")
            print(f"{info['query']}")
            print()


def print_commands(results: dict, concept: dict):
    """输出可执行命令。"""
    scopus_key = concept.get("scopus_api_key", "$SCOPUS_API_KEY")
    memory_dir = concept.get("memory_dir", "memory")

    for db, info in results.items():
        if "error" in info:
            print(f"# {db}: {info['error']}")
            continue

        print(f"# --- {info['name']} ---")
        if db == "scopus":
            print(f'python scripts/scopus_search.py -q "{info["query"]}" '
                  f'-k {scopus_key} -o {memory_dir}/scopus_results.json')
        elif db in ("ieee", "acm"):
            print(f'browser.open(profile="openclaw", url="{info["query"]}")')
            extractor = f"extractors/{db}.js"
            print(f"read {extractor}")
            print(f"browser.act(profile=\"openclaw\", kind=\"evaluate\", fn=<script>)")
        elif db == "engineering_village":
            print(f'# Copy this into EV search box:')
            print(f'#   {info["query"]}')
            print(f'browser.open(profile="openclaw", '
                  f'url="https://www.engineeringvillage.com/app/search/quick/?")')
            print(f"# Then type the query and click Search")
            print(f"read extractors/engineering_village.js")
            print(f"browser.act(profile=\"openclaw\", kind=\"evaluate\", fn=<script>)")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate optimized database queries from structured search concepts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python query_builder.py -c concept.json
  python query_builder.py -c concept.json --format commands
  cat concept.json | python query_builder.py -

Concept JSON format:
  {
    "core_concepts": ["autonomous scientific discovery"],
    "synonyms": {"AI": ["LLM", "artificial intelligence"]},
    "sub_topics": ["paper generation", "hypothesis generation"],
    "exclude": ["healthcare", "clinical"],
    "year_range": "2023-2026",
    "databases": ["scopus", "ieee", "acm"]
  }
        """,
    )
    parser.add_argument("-c", "--concept", required=True,
                        help="Concept JSON file path, or '-' for stdin")
    parser.add_argument("--format", choices=["urls", "commands", "json"],
                        default="urls", help="Output format (default: urls)")
    args = parser.parse_args()

    concept = load_concept(args.concept)

    warnings = validate_concept(concept)
    for w in warnings:
        print(f"[WARN] {w}", file=sys.stderr)

    results = build_all(concept)

    if args.format == "json":
        output = {
            "concept": concept,
            "warnings": warnings,
            "queries": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif args.format == "commands":
        print_commands(results, concept)
    else:
        print_urls(results)


if __name__ == "__main__":
    main()
