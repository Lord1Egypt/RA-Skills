#!/usr/bin/env python3
"""
免费 API 查询预检 · Free Pre-check
===================================

在正式搜索付费数据库之前，用 OpenAlex 免费 API 快速检查：
- 查询是否过窄（0 结果 → 核心概念 AND 冲突）
- 查询是否过宽（> 2000 结果 → 需要加约束）
- 查询是否合理（3-2000 → 可以上付费库）

纯粹 HTTP GET，不开浏览器，100-200ms 一次调用。
OpenAlex 无需 API Key，无限速，覆盖全学科。

管道位置（新增）：
    search_concept.json → query_builder.py → free_precheck.py → 按信号分流
                                                   ↓
                                     ┌──────┬──────┼──────┐
                                  太窄     合理    太宽     API 挂了
                                    ↓       ↓       ↓        ↓
                                 反馈 AI   继续    反馈 AI   跳过预检
                                放宽概念  管道    收紧概念  继续管道

用法：
    # 标准预检（从 search_concept.json 读取）
    python free_precheck.py -c memory/search_concept.json

    # 管道模式（输出 JSON，供 AI 解析）
    python free_precheck.py -c memory/search_concept.json --json

    # 只检查不输出建议
    python free_precheck.py -c memory/search_concept.json --quiet

输出信号：
    { "signal": "narrow|good|broad|skip", "count": N, "suggestion": "..." }

阈值（可调）：
    TOO_NARROW  = 3     # ≤3 条 → 查询太窄
    TOO_BROAD   = 2000  # >2000 条 → 查询太宽（付费库 25/page 的话是 80+ 页）
"""

import argparse
import json
import sys

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import urllib.request
import urllib.parse
import urllib.error
import re
import time
from pathlib import Path


# ---------------------------------------------------------------------------
# 阈值
# ---------------------------------------------------------------------------
TOO_NARROW = 3       # ≤ 此值 → 太窄
TOO_BROAD = 2000     # > 此值 → 太宽（IE 约 25/page = 80 页+）
MAX_RETRIES = 2
RETRY_DELAY = 1.5    # 秒


# ---------------------------------------------------------------------------
# OpenAlex 查询构建
# ---------------------------------------------------------------------------

def build_openalex_query(concept: dict) -> str:
    """
    将 search_concept.json 翻译成 OpenAlex 搜索字符串。

    OpenAlex 搜索语法：
      - "exact phrase" → 引号短语
      - AND / OR / NOT → 布尔运算，AND 优先级高于 OR
      - 不支持嵌套括号 → 扁平化处理

    策略：核心概念 AND 连接，子主题 OR 插入，排除词 NOT。
    """
    clauses = []

    # 1. 核心概念（AND 连接）
    for c in concept.get("core_concepts", []):
        clauses.append(f'"{c}"')

    # 2. 子主题（OR 组）
    sub_parts = []
    for st in concept.get("sub_topics", []):
        sub_parts.append(f'"{st}"')
    if sub_parts:
        clauses.append("(" + " OR ".join(sub_parts) + ")")

    # 3. 同义词扩展（每个 term 展开为 OR 组）
    for term, syns in concept.get("synonyms", {}).items():
        all_terms = [f'"{s}"' for s in [term] + syns]
        clauses.append("(" + " OR ".join(all_terms) + ")")

    query = " AND ".join(clauses)

    # 4. 排除词
    for ex in concept.get("exclude", []):
        query += f' NOT "{ex}"'

    return query.strip()


def build_openalex_url(query: str, concept: dict) -> str:
    """构建 OpenAlex API URL，附带年份过滤。"""
    encoded = urllib.parse.quote(query, safe='')
    url = f"https://api.openalex.org/works?search={encoded}&per_page=1"

    # 年份过滤
    year = concept.get("year_range", "")
    if year and "-" in year:
        try:
            start, end = year.split("-")[:2]
            url += f"&filter=from_publication_date:{start}-01-01,to_publication_date:{end}-12-31"
        except (ValueError, IndexError):
            pass

    return url


# ---------------------------------------------------------------------------
# API 调用
# ---------------------------------------------------------------------------

def call_openalex(url: str, timeout: int = 15) -> dict:
    """调用 OpenAlex API，带重试和错误处理。"""
    last_error = None

    for attempt in range(MAX_RETRIES + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "paid-db-access/1.0 (mailto:researcher@example.com)"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return {"ok": True, "data": data, "error": None}

        except urllib.error.HTTPError as e:
            last_error = f"HTTP {e.code}"
            if e.code == 429:
                time.sleep(RETRY_DELAY * 2)
                continue
            break
        except urllib.error.URLError as e:
            last_error = f"Network: {e.reason}"
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
                continue
            break
        except json.JSONDecodeError:
            last_error = "Invalid JSON response"
            break
        except Exception as e:
            last_error = str(e)
            break

    return {"ok": False, "data": None, "error": last_error}


# ---------------------------------------------------------------------------
# 信号判断
# ---------------------------------------------------------------------------

def classify_count(count: int) -> tuple[str, str]:
    """
    根据命中数返回 (信号, 建议)。

    信号：
      "narrow" — 太窄，可能是 AND 条件冲突
      "good"   — 合理范围
      "broad"  — 太宽，需要加约束

    建议是给 AI 的自然语言提示，比如：
      "core_concepts 中 3 个词 AND 连接导致零结果，
       建议将 1-2 个移到 sub_topics 或拆成多轮搜索"
    """
    if count <= TOO_NARROW:
        return ("narrow", _narrow_suggestion(count))
    elif count > TOO_BROAD:
        return ("broad", _broad_suggestion(count))
    else:
        return ("good", f"命中 {count} 篇，查询范围合理，可以上付费库")


def _narrow_suggestion(count: int) -> str:
    """生成'查询太窄'的具体建议。"""
    if count == 0:
        return (
            "查询命中 0 篇。可能原因：\n"
            "  1. core_concepts 中多个短语 AND 连接过于严格\n"
            "  2. exclude 词误伤了相关论文\n"
            "  3. 年份范围太窄\n"
            "  建议：减少 core_concepts 数量（≤2 个），或将部分核心概念移到 sub_topics"
        )
    else:
        return (
            f"查询仅命中 {count} 篇，过于狭窄。\n"
            "  建议：放宽 core_concepts、增加 synonym 扩展、或去掉部分 AND 条件"
        )


def _broad_suggestion(count: int) -> str:
    """生成'查询太宽'的具体建议。"""
    return (
        f"查询命中 {count} 篇，范围过宽（> {TOO_BROAD}）。\n"
        "  建议：添加 core_concepts 收紧主题、增加 exclude 排除无关领域、\n"
        "  或添加子主题 sub_topics 聚焦具体方向"
    )


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------

def precheck(concept_path: str, quiet: bool = False) -> dict:
    """
    执行预检，返回结果字典。

    Returns:
        {
            "signal": "narrow|good|broad|skip",
            "count": int,
            "query": str,
            "suggestion": str,
            "error": str | None
        }
    """
    # 加载概念
    try:
        p = Path(concept_path)
        if not p.exists():
            return {
                "signal": "skip", "count": 0,
                "query": "", "suggestion": "search_concept.json 不存在，跳过预检",
                "error": "file_not_found"
            }
        with open(p, "r", encoding="utf-8") as f:
            concept = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        return {
            "signal": "skip", "count": 0,
            "query": "", "suggestion": f"概念文件读取失败: {e}",
            "error": str(e)
        }

    # 构建查询
    query = build_openalex_query(concept)
    url = build_openalex_url(query, concept)

    if not quiet:
        print(f"[Precheck] 查询: {query[:120]}{'...' if len(query) > 120 else ''}")
        print(f"[Precheck] URL: {url[:150]}{'...' if len(url) > 150 else ''}")

    # 调用 API
    result = call_openalex(url)
    if not result["ok"]:
        return {
            "signal": "skip", "count": 0,
            "query": query,
            "suggestion": f"OpenAlex API 不可用 ({result['error']})，跳过预检，直接上付费库",
            "error": result["error"]
        }

    # 提取计数
    data = result["data"]
    count = data.get("meta", {}).get("count", 0)
    signal, suggestion = classify_count(count)

    if not quiet:
        print(f"[Precheck] 命中: {count} → 信号: {signal}")
        if signal != "good":
            print(f"[Precheck] 建议:\n{suggestion}")

    return {
        "signal": signal,
        "count": count,
        "query": query,
        "suggestion": suggestion,
        "error": None,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Free Pre-check — 用 OpenAlex 预检查询范围，避免付费库白跑",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python free_precheck.py -c memory/search_concept.json
  python free_precheck.py -c memory/search_concept.json --json
  python free_precheck.py -c memory/search_concept.json --quiet

Signals:
  narrow  — 查询 < 3 篇，需放宽概念
  good    — 3-2000 篇，可以上付费库
  broad   — > 2000 篇，需收紧概念
  skip    — API 不可用，跳过预检继续管道
        """,
    )
    parser.add_argument("-c", "--concept", required=True,
                        help="搜索概念 JSON 文件路径")
    parser.add_argument("--json", action="store_true",
                        help="输出 JSON 格式（供 AI/管道解析）")
    parser.add_argument("--quiet", action="store_true",
                        help="静默模式，仅输出 JSON（需同时传 --json）")
    args = parser.parse_args()

    result = precheck(args.concept, quiet=args.quiet or args.json)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        # 返回退出码供脚本判断
        signal = result.get("signal", "skip")
        if signal == "narrow":
            sys.exit(2)   # 需要 AI 介入
        elif signal == "broad":
            sys.exit(3)   # 需要 AI 紧缩
        elif signal == "skip":
            sys.exit(4)   # API 不可用，继续管道

    # 非 JSON 模式下返回 exit code 供 shell pipeline 判断
    signal = result.get("signal", "skip")
    if signal == "narrow":
        sys.exit(2)
    elif signal == "broad":
        sys.exit(3)


if __name__ == "__main__":
    main()
