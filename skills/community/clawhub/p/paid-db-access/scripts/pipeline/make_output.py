#!/usr/bin/env python3

"""

make_output.py — themed.json → 最终 Markdown 输出

===============================================



两层结构：

  第一层：按 AI 分数分档 → 🟢 核心文献 / 🟡 高质量参考 / 🟠 前沿探索

  第二层：档内按 _theme 主题细分 → 一、二、三……



用法：

  python scripts/make_output.py -i memory/themed.json -o memory/final_results.md

  python scripts/make_output.py -i memory/themed.json -o memory/final_results.md --top 15



分档规则（可配置 --tier-mode）：

  percentile  — 按分位线 (top 30%/mid 40%/bot 30%)

  equal       — 均分三等份

  threshold   — 按固定阈值 (>=75/>=60/<60)

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse, json, os, sys



from utils.pipeline_schema import validate, report, check_version



import sys, os




# Windows GBK → UTF-8

if sys.platform == "win32":

    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    sys.stderr.reconfigure(encoding="utf-8", errors="replace")



from pathlib import Path

from collections import Counter, OrderedDict



# ---------------------------------------------------------------------------

# 中文数字

# ---------------------------------------------------------------------------

CN_NUM = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]



def cn_num(n: int) -> str:

    if 0 <= n < len(CN_NUM):

        return CN_NUM[n]

    return str(n + 1)



# ---------------------------------------------------------------------------

# Tier 定义

# ---------------------------------------------------------------------------

TIERS = [

    {

        "key": "core",

        "emoji": "\U0001f7e2",  # 🟢

        "label": "核心文献",

    },

    {

        "key": "solid",

        "emoji": "\U0001f7e1",  # 🟡

        "label": "高质量参考",

    },

    {

        "key": "frontier",

        "emoji": "\U0001f7e0",  # 🟠

        "label": "前沿探索",

    },

]



# ---------------------------------------------------------------------------

# 分档逻辑

# ---------------------------------------------------------------------------



def composite_score(paper: dict, weights=(0.4, 0.3, 0.3)) -> float:

    """综合三维 AI 评分。默认权重：relevance 40%, quality 30%, novelty 30%"""

    ai = paper.get("_ai_scores", {})

    r = ai.get("relevance", 0)

    q = ai.get("quality", 0)

    n = ai.get("novelty", 0)

    return r * weights[0] + q * weights[1] + n * weights[2]





def assign_tiers(papers: list[dict], mode: str = "percentile") -> list[dict]:

    """

    为论文分配 tier，返回带 _tier 字段的排序列表。



    mode:

      percentile — top 30% 🟢, mid 40% 🟡, bot 30% 🟠

      equal      — 均分三等份

      threshold   — >=75 🟢, >=60 🟡, <60 🟠

    """

    # 计算综合分并排序

    scored = [(composite_score(p), p) for p in papers]

    scored.sort(key=lambda x: x[0], reverse=True)



    n = len(scored)



    if mode == "threshold":

        for score, p in scored:

            if score >= 75:

                p["_tier"] = "core"

            elif score >= 60:

                p["_tier"] = "solid"

            else:

                p["_tier"] = "frontier"

    elif mode == "equal":

        chunk = max(1, n // 3)

        for idx, (score, p) in enumerate(scored):

            if idx < chunk:

                p["_tier"] = "core"

            elif idx < chunk * 2:

                p["_tier"] = "solid"

            else:

                p["_tier"] = "frontier"

    else:  # percentile (default)

        top_n = max(1, int(n * 0.3))

        mid_n = max(1, int(n * 0.4))

        for idx, (score, p) in enumerate(scored):

            if idx < top_n:

                p["_tier"] = "core"

            elif idx < top_n + mid_n:

                p["_tier"] = "solid"

            else:

                p["_tier"] = "frontier"



    # 按 tier → score 降序排列

    tier_order = {"core": 0, "solid": 1, "frontier": 2}

    scored.sort(key=lambda x: (tier_order.get(x[1].get("_tier", "frontier"), 9),

                                -x[0]))

    return [p for _, p in scored]





# ---------------------------------------------------------------------------

# 渲染

# ---------------------------------------------------------------------------



def _read_abstract_fallback(paper: dict) -> str:

    """缺中文摘要时的兜底：从 _abstract_file 读英文摘要前 300 字符。"""

    import os as _os

    af = paper.get("_abstract_file", "")

    if af and _os.path.exists(af):

        try:

            content = open(af, "r", encoding="utf-8").read()

            idx = content.find("\nAbstract:\n")

            if idx >= 0:

                text = content[idx + len("\nAbstract:\n"):].strip()

                return text[:300] + ("..." if len(text) > 300 else "")

        except Exception:

            pass

    return ""





def render_markdown(papers: list[dict], bibtex_path: str = "memory/results.bib") -> str:

    """渲染最终 Markdown 输出。"""

    lines = []



    # ── 头部 ──

    lines.append(f"# \U0001f52c 文献检索结果 · 精选 {len(papers)} 篇\n")

    dbs = set()

    for p in papers:

        src = p.get("_source_db", [])

        if isinstance(src, list):

            dbs.update(src)

        else:

            dbs.add(str(src))

    db_str = "/".join(sorted(dbs))

    lines.append(f"> 来源: {db_str} | BibTeX: `{bibtex_path}`\n")



    # ── 按 tier 分组 ──

    tier_groups = OrderedDict()

    for t in TIERS:

        tier_groups[t["key"]] = []



    for p in papers:

        tier_key = p.get("_tier", "frontier")

        if tier_key not in tier_groups:

            tier_key = "frontier"

        tier_groups[tier_key].append(p)



    # 移除空 tier

    tier_groups = OrderedDict((k, v) for k, v in tier_groups.items() if v)



    # ── 渲染每个 tier ──

    for tier_key, tier_papers in tier_groups.items():

        tier = next(t for t in TIERS if t["key"] == tier_key)

        emoji = tier["emoji"]

        label = tier["label"]



        lines.append(f"## {emoji} {label}\n")



        # ── tier 内按 _theme 分组 ──

        theme_groups = OrderedDict()

        for p in tier_papers:

            theme = p.get("_theme", "其他")

            theme_groups.setdefault(theme, []).append(p)



        # 主题排序：论文数多的在前

        theme_groups = OrderedDict(

            sorted(theme_groups.items(), key=lambda x: len(x[1]), reverse=True)

        )



        theme_idx = 0

        for theme_name, theme_papers in theme_groups.items():

            n = len(theme_papers)

            cn_idx = cn_num(theme_idx)

            lines.append(f"### {emoji} {cn_idx}\u3001{theme_name}\uff08{label} \u00b7 {n}\u7bc7\uff09\n")



            for i, p in enumerate(theme_papers, 1):

                title = p.get("title", "?")

                src_db = "+".join(p.get("_source_db", ["?"])) if isinstance(p.get("_source_db"), list) else str(p.get("_source_db", "?"))



                # AI scores intentionally excluded from output per USER.md requirement



                authors = p.get("authors", "?")

                year = p.get("year", "?")

                venue = p.get("venue", "?")

                citations = p.get("citations", "?")

                link = p.get("link", "")

                doi = p.get("doi", "")

                cn_summary = (p.get("_cn_summary") or "").strip()



                # 标题行

                lines.append(f"**{i}. {title}** [{src_db}]")

                # 元数据行

                meta = f"\U0001f464 {authors} \u00b7 \U0001f4c5 {year} \u00b7 \U0001f4ca \u5f15\u7528 {citations}"

                if venue:

                    meta += f" \u00b7 \U0001f3db\ufe0f {venue}"

                lines.append(meta)

                # 链接

                url = link or (f"https://doi.org/{doi}" if doi else "")

                if url:

                    lines.append(f"\U0001f517 {url}")

                # DOI（有 link 时补充）

                if doi and link:

                    lines.append(f"\U0001f4c4 DOI: {doi}")

                # 中文摘要（缺失时用英文摘要前 300 字兜底）

                if cn_summary and len(cn_summary) > 20:

                    cn_clean = cn_summary.replace("\n", " ").strip()

                    lines.append(f"\U0001f4a1 {cn_clean}")

                else:

                    # 兜底：从 _abstract_file 读英文摘要

                    fallback = _read_abstract_fallback(p)

                    if fallback:

                        lines.append(f"\U0001f4a1 [EN] {fallback}")

                    else:

                        lines.append(f"\U0001f4a1 [\u6458\u8981\u7f3a\u5931]")



                lines.append("")



            theme_idx += 1



    # ── 统计 ──

    lines.append("---\n")

    lines.append("\U0001f4ca \u7edf\u8ba1\n")

    lines.append(f"- \u6700\u7ec8\u8f93\u51fa: {len(papers)} \u7bc7")



    db_counts = Counter()

    for p in papers:

        src = p.get("_source_db", [])

        if isinstance(src, list):

            for db in src:

                db_counts[db] += 1

        else:

            db_counts[str(src)] += 1

    lines.append(f"- \u6570\u636e\u5e93\u5206\u5e03: " + ", ".join(f"{k}: {v}" for k, v in db_counts.items()))



    # Tier 分布

    tier_counts = Counter(p.get("_tier", "?") for p in papers)

    tier_labels = {t["key"]: f"{t['emoji']} {t['label']}" for t in TIERS}

    lines.append(f"- \u6863\u6b21\u5206\u5e03: " + ", ".join(

        f"{tier_labels.get(k, k)}: {v}" for k, v in tier_counts.items()))



    lines.append(f"- BibTeX: `{bibtex_path}`")



    return "\n".join(lines)





# ---------------------------------------------------------------------------

# CLI

# ---------------------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(

        description="themed.json → 最终分层主题 Markdown",

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog="""

Examples:

  python make_output.py -i memory/themed.json -o memory/final_results.md

  python make_output.py -i memory/themed.json -o memory/final_results.md --top 15 --tier-mode threshold

  python make_output.py -i memory/themed.json -o memory/final_results.md --bibtex memory/results.bib

        """,

    )

    parser.add_argument("-i", "--input", required=True, help="themed.json 路径")

    parser.add_argument("-o", "--output", help="输出 Markdown 文件路径")

    parser.add_argument("--top", type=int, default=0, help="Top N 篇 (0=全部)")

    parser.add_argument("--tier-mode", choices=["percentile", "equal", "threshold"],

                        default="percentile", help="分档模式 (default: percentile)")

    parser.add_argument("--bibtex", default="memory/results.bib", help="BibTeX 文件路径引用")

    parser.add_argument("--stdout", action="store_true", help="同时打印到 stdout")

    args = parser.parse_args()



    with open(args.input, "r", encoding="utf-8") as f:

        data = json.load(f)



    papers = data.get("papers", data if isinstance(data, list) else [])

    if args.top > 0:

        papers = papers[:args.top]



    # --- 入口校验 ---

    ver_issues = check_version(data, stage="themed")

    if ver_issues:

        report(ver_issues, stage="make_output")

    ok, issues = validate(papers, stage="themed")

    if issues:

        report(issues, stage="make_output")



    # 确保有 _theme 字段

    for p in papers:

        if "_theme" not in p:

            p["_theme"] = "\u672a\u5206\u7c7b"



    print(f"[make_output] {len(papers)} papers, tier-mode={args.tier_mode}")



    # 分档

    papers = assign_tiers(papers, mode=args.tier_mode)

    for t in TIERS:

        count = sum(1 for p in papers if p.get("_tier") == t["key"])

        if count:

            print(f"  {t['emoji']} {t['label']}: {count} \u7bc7")



    # 渲染

    md = render_markdown(papers, bibtex_path=args.bibtex)



    if args.output:

        out_path = Path(args.output)

        out_path.parent.mkdir(parents=True, exist_ok=True)

        out_path.write_text(md, encoding="utf-8")

        print(f"\n\u2705 Saved to {out_path}")



    if args.stdout or not args.output:

        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

        print(md)





if __name__ == "__main__":

    main()

