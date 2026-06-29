#!/usr/bin/env python3

"""

论文统一评分与分类 · Paper Ranker

================================



替代 merge_results.py 中的评分模块。独立于去重逻辑——去重仍由 merge_results.py 处理。



核心理念：从「打一个总分」变成「画一个多维画像」。

每个维度 0-100，彼此独立。输出带标签的结构化数据供 AI 做最终判断。



管道位置：

    merge_results.py (去重) → paper_ranker.py (评分+分类) → AI 输出推荐



用法：

    python paper_ranker.py -i merged.json -o ranked.json --keywords "machine learning, transformer"

    python paper_ranker.py -i merged.json -o ranked.json --keywords "NLP" --mode seminal

    python paper_ranker.py -i merged.json -o ranked.json                # 无关键词，跳过相关性



评分维度：

    relevance     0-100   搜索关键词匹配度（无关键词时标记 null）

    impact        0-100   学术影响力（引用百分位 + venue）

    recency       0-100   时效性（指数衰减）

    accessibility 0-100   可获得性（OA / DOI / 链接）



分类标签：

    landmark      影响力 ≥80                                领域基石

    core          相关性 ≥70 AND 影响力 ≥50                 本次核心

    frontier      时效性 ≥85 AND 相关性 ≥50                 最新前沿

    solid         影响力 ≥40 OR 相关性 ≥50                  值得浏览

    quick_read    OA AND 相关性 ≥50                         可直接下载

    background    default                                   背景参考



搜索模式：

    balanced      相关性 ↓, 影响力 tiebreak                 常规调研

    seminal       影响力 ↓, 相关性 ≥30                      找经典/写综述

    frontier      时效性 ↓, 相关性 ≥40                      追前沿

    quick         可获得性 ↓, 相关性 ≥50                    找能下载的

"""



import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse

import json

import re

import sys

from datetime import datetime

from pathlib import Path

from typing import Optional



from utils.pipeline_schema import validate, report, stamp, check_version, PIPELINE_VERSION





import sys, os




# ---------------------------------------------------------------------------

# 1. 字段规范化

# ---------------------------------------------------------------------------



# 引用数跨库归一化系数（Scopus 覆盖面最广，以它为基准 ≈1.0）

# 调整原则：使同一篇论文从不同库查到的引用数在合理误差内

CITATION_SCALE = {

    "scopus": 1.0,

    "ieee": 0.7,               # IEEE 只统计 IEEE 内部的引用，偏低

    "engineering_village": 1.0, # EV 用的就是 Scopus 数据

    "acm": 0.75,               # ACM 引用覆盖偏窄

    "wos": 0.85,               # WoS 比 Scopus 略保守

}



# Venue 质量分层

# 规则：精确名（白名单）→ 关键词规则（transactions/journal/conference/workshop）→ 兜底

TOP_VENUES: dict[str, int] = {

    # === Tier 0: 三大顶刊 ===

    "nature": 10, "science": 10, "cell": 10, "pnas": 9,

    "nature communications": 8, "science advances": 8,



    # === Tier 1: 顶级会议 (9-10) ===

    "neurips": 9, "icml": 9, "iclr": 9,

    "cvpr": 9, "iccv": 9, "eccv": 8,

    "acl": 9, "emnlp": 9, "naacl": 8,

    "aaai": 8, "ijcai": 8,

    "sigmod": 9, "vldb": 9, "sigcomm": 9, "sosp": 10, "osdi": 10,

    "chi": 9, "cscw": 8, "uist": 8,

    "isca": 9, "micro": 9, "hpc": 9, "asplos": 9,

    "www": 8, "sigir": 8, "wsdm": 8, "kdd": 9,

    "icse": 9, "fse": 9, "ase": 8,

    "mobicom": 9, "sensys": 8, "nsdi": 9,



    # === Tier 1: 顶级期刊 (9) ===

    "ieee transactions on pattern analysis and machine intelligence": 10,

    "ieee transactions on neural networks and learning systems": 9,

    "ieee transactions on information forensics and security": 8,

    "acm computing surveys": 10,

    "acm transactions on": 8,                            # ACM Trans. 通用

    "communications of the acm": 9,                      # CACM

    "journal of machine learning research": 9,

    "artificial intelligence": 9,

    "international journal of computer vision": 9,



    # === Tier 1: 顶级会议全名（数据库可能返回全名而非缩写） ===

    "advances in neural information processing systems": 9,  # NeurIPS full name

    "international conference on machine learning": 9,

    "conference on computer vision and pattern recognition": 9,

    "international conference on computer vision": 9,

    "international conference on learning representations": 9,

    "annual meeting of the association for computational linguistics": 9,

    "conference on empirical methods in natural language processing": 9,

    "north american chapter of the association for computational linguistics": 8,  # NAACL

}



# Venue 类别关键词（精确匹配失败后使用）

VENUE_RULES = [

    (["ieee transactions on", "acm transactions on"], 8),     # 顶刊

    (["ieee journal of", "acm journal of"], 7),               # 好刊

    (["journal of", "international journal of"], 6),          # 普通期刊

    (["ieee transactions", "ieee trans", "acm transactions"], 7),  # IEEE/ACM 汇刊简写

    (["conference on", "international conference on"], 6),    # 会议

    (["symposium on", "ieee symposium"], 6),                  # 研讨会

    (["workshop on", "ieee workshop"], 4),                    # 工作坊

    (["ieee access"], 5),                                     # IEEE Access

    (["arxiv"], 3),                                           # 预印本

]



CURRENT_YEAR = datetime.now().year





def normalize_year(year) -> Optional[int]:

    """规范化年份。无效/缺失返回 None，不猜测。"""

    if year is None:

        return None

    try:

        y = int(year)

    except (ValueError, TypeError):

        return None

    if y < 1900 or y > CURRENT_YEAR + 2:

        return None

    return y





def normalize_citations(citations, source_dbs: list[str]) -> float:

    """归一化引用数：取各库引用数乘系数后的最大值。"""

    try:

        c = int(citations)

    except (ValueError, TypeError):

        c = 0



    if not source_dbs:

        return float(c)



    # 取第一个有系数的库，如果没有就用 1.0

    scale = next((CITATION_SCALE.get(db, 1.0) for db in source_dbs), 1.0)

    return round(c * scale, 1)





def classify_venue(venue: str) -> int:

    """

    venue 质量打分 (0-10)。



    匹配优先级：

      1. 精确全名匹配白名单

      2. 标准化后精确匹配

      3. 关键词规则（按 VENUE_RULES 顺序）

      4. 白名单多词 key 子串匹配（仅 2+ 词的 key）

      5. 兜底 3

    """

    if not venue:

        return 3



    v = venue.strip()

    v_norm = re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', v.lower())).strip()



    # 1-2. 精确匹配（原始 + 标准化后）

    if v.lower() in TOP_VENUES:

        return TOP_VENUES[v.lower()]

    if v_norm in TOP_VENUES:

        return TOP_VENUES[v_norm]



    # 3. 关键词规则（先于白名单子串，避免宽泛规则覆盖精确匹配）

    for patterns, score in VENUE_RULES:

        for pat in patterns:

            if pat in v_norm:

                return score



    # 4. 白名单子串匹配

    best_len = 0

    best_score = 3



    # 4a. 多词 key（2+ 词）：直接子串匹配（如 "nature communications" in venue）

    for key, score in TOP_VENUES.items():

        if ' ' in key and key in v_norm and len(key) > best_len:

            best_len = len(key)

            best_score = score



    # 4b. 单词 key：词边界匹配（如 "naacl" matches "naacl hlt 2019" 但不匹配 "naaclv2"）

    if best_len == 0:

        v_words = set(v_norm.split())

        for key, score in TOP_VENUES.items():

            if ' ' not in key and key in v_words and score > best_score:

                best_score = score



    if best_score > 3 or best_len > 0:

        return best_score



    # 5. 兜底

    if "journal" in v_norm:

        return 4

    return 3





def normalize_field(paper: dict):

    """原地规范化 paper 的关键字段，添加 _norm_* 内部字段。"""

    raw_year = paper.get("year")

    paper["_norm_year"] = normalize_year(raw_year)



    sources = paper.get("_source_db", [])

    if not isinstance(sources, list):

        sources = [sources] if sources else []



    raw_cit = paper.get("citations")

    paper["_norm_citations"] = normalize_citations(raw_cit, sources)



    paper["_venue_tier"] = classify_venue(paper.get("venue", ""))





# ---------------------------------------------------------------------------

# 2. 多维评分

# ---------------------------------------------------------------------------



def tokenize(text: str) -> set[str]:

    """提取有意义的词（>2 字符），支持中英文。"""

    t = re.sub(r'[^\w\s]', ' ', str(text).lower())

    return set(w for w in t.split() if len(w) > 2)





def compute_relevance(paper: dict, keywords: Optional[list[str]]) -> Optional[int]:

    """

    相关性评分 (0-100)。



    算法：关键词 token 在标题和摘要中的加权命中密度。

    标题权重 60%，摘要权重 40%。



    返回 None 表示无关键词，跳过此维度。

    """

    if not keywords:

        return None



    kw_tokens = set()

    for kw in keywords:

        kw_tokens.update(tokenize(kw))



    if not kw_tokens:

        return None



    title = paper.get("title", "")

    abstract = paper.get("abstract", "")



    title_tokens = tokenize(title)

    abs_tokens = tokenize(abstract)



    title_hit = len(kw_tokens & title_tokens) / max(len(kw_tokens), 1)

    abs_hit = len(kw_tokens & abs_tokens) / max(len(kw_tokens), 1)



    score = title_hit * 60 + abs_hit * 40

    return min(round(score), 100)





def compute_impact(paper: dict, all_citations: list[float]) -> int:

    """

    影响力评分 (0-100)。



    引用分 (70%)：在结果集内的百分位排名。

    Venue分 (30%)：来自 classify_venue。



    百分位自适应当前结果集——冷门领域 5 次引用可能前 10%，

    热门领域 50 次引用可能只在中游。不依赖硬编码阈值。

    """

    cit = paper.get("_norm_citations", 0)

    venue_tier = paper.get("_venue_tier", 3)



    # 引用百分位

    if all_citations and max(all_citations) > 0:

        # 百分位 = 比多少比例的论文引用高

        lower = sum(1 for c in all_citations if c < cit)

        equal = sum(1 for c in all_citations if c == cit)

        # 使用 "lower + equal/2" 避免平局全部判高分

        cit_pct = ((lower + equal * 0.5) / len(all_citations)) * 100

    else:

        cit_pct = 50



    impact = cit_pct * 0.7 + (venue_tier * 10) * 0.3

    return min(round(impact), 100)





def compute_recency(paper: dict) -> Optional[int]:

    """

    时效性评分 (0-100)。



    指数衰减：半衰期 5 年。今年 100 → 5 年后 50 → 10 年后 25。

    比台阶函数更平滑——3 年前和 4 年前不会有断崖差距。



    返回 None 表示年份缺失。

    """

    year = paper.get("_norm_year")

    if year is None:

        return None



    age = CURRENT_YEAR - year

    if age < 0:

        return 100

    return round(100 * (0.5 ** (age / 5)))





def compute_accessibility(paper: dict) -> int:

    """

    可获得性评分 (0-100)。



    简单三级：

      OA → 100

      有 DOI 或 link → 50

      都没有 → 0

    """

    is_oa = paper.get("isOA") or paper.get("openaccess")

    doi = paper.get("doi")

    link = paper.get("link")



    if is_oa:

        return 100

    if doi or link:

        return 50

    return 0





# ---------------------------------------------------------------------------

# 3. 分类标签

# ---------------------------------------------------------------------------



def classify(paper: dict) -> list[str]:

    """根据画像打标签。一篇论文可以有多个标签。"""

    scores = paper.get("_scores", {})

    rel = scores.get("relevance")

    imp = scores.get("impact", 0)

    rec = scores.get("recency")

    acc = scores.get("accessibility", 0)



    tags = []



    # landmark: 领域基石

    if imp >= 80:

        tags.append("landmark")



    # core: 本次搜索的核心文献（需要相关性打分）

    if rel is not None and rel >= 70 and imp >= 50:

        tags.append("core")



    # frontier: 最新前沿

    if rec is not None and rec >= 85 and (rel is not None and rel >= 50):

        tags.append("frontier")



    # solid: 值得浏览

    if imp >= 40 or (rel is not None and rel >= 50):

        tags.append("solid")



    # quick_read: 直接可读

    if acc == 100 and (rel is not None and rel >= 50):

        tags.append("quick_read")



    # background: 兜底

    if not tags:

        tags.append("background")



    return tags





# ---------------------------------------------------------------------------

# 4. 搜索模式 & 排序

# ---------------------------------------------------------------------------



# 模式 → (主排序键, 降序, 过滤条件)

SEARCH_MODES = {

    "balanced": {

        "sort_key": lambda p: (

            p["_scores"].get("relevance") or 0,

        ),

        "description": "相关性优先，影响力作为 tiebreaker",

    },

    "seminal": {

        "sort_key": lambda p: (

            p["_scores"].get("impact", 0),

        ),

        "filter": lambda p: (p["_scores"].get("relevance") or 0) >= 30,

        "description": "高影响力优先，找经典/写综述",

    },

    "frontier": {

        "sort_key": lambda p: (

            p["_scores"].get("recency") or 0,

        ),

        "filter": lambda p: (p["_scores"].get("relevance") or 0) >= 40,

        "description": "最新优先，追前沿/找 gap",

    },

    "quick": {

        "sort_key": lambda p: (

            p["_scores"].get("accessibility", 0),

        ),

        "filter": lambda p: (p["_scores"].get("relevance") or 0) >= 50,

        "description": "可获取性优先，找能直接下载的",

    },

}





def sort_papers(papers: list[dict], mode: str = "balanced") -> list[dict]:

    """按模式排序。过滤 + 主排序 + 引用数 tiebreak。"""

    config = SEARCH_MODES.get(mode, SEARCH_MODES["balanced"])

    sort_key = config["sort_key"]

    filter_fn = config.get("filter")



    if filter_fn:

        papers = [p for p in papers if filter_fn(p)]



    # 排序：主键（模式决定）+ 引用数作为二级 tiebreak

    papers.sort(key=lambda p: (

        sort_key(p),

        p.get("_norm_citations", 0),

    ), reverse=True)



    return papers





# ---------------------------------------------------------------------------

# 5. 主流程

# ---------------------------------------------------------------------------



def rank_papers(input_path: str, output_path: Optional[str] = None,

                keywords: Optional[str] = None,

                mode: str = "balanced",

                min_score: float = 0):

    """

    完整评分管道：规范化 → 评分 → 分类 → 排序 → 输出。

    """

    with open(input_path, "r", encoding="utf-8") as f:

        data = json.load(f)



    if isinstance(data, dict) and "papers" in data:

        papers = data["papers"]

        wrapper = data

    elif isinstance(data, list):

        papers = data

        wrapper = {"papers": data}

    else:

        print(f"[ERROR] Unrecognized input format", file=sys.stderr)

        sys.exit(1)



    total = len(papers)

    if total == 0:

        print("[WARN] No papers to score", file=sys.stderr)

        output = wrapper if isinstance(data, dict) and "papers" in data else {"papers": []}

        if output_path:

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            stamp(output, stage="ranked")

            with open(output_path, "w", encoding="utf-8") as f:

                json.dump(output, f, ensure_ascii=False, indent=2)

        return



    kw_list = None

    if keywords:

        kw_list = [kw.strip() for kw in keywords.split(",") if kw.strip()]



    # --- Step 1: 字段规范化 ---

    for paper in papers:

        normalize_field(paper)



    all_citations = [p.get("_norm_citations", 0) for p in papers]

    has_keywords = bool(kw_list)



    # --- Step 2: 多维评分 ---

    for paper in papers:

        scores = {

            "relevance": compute_relevance(paper, kw_list),

            "impact": compute_impact(paper, all_citations),

            "recency": compute_recency(paper),

            "accessibility": compute_accessibility(paper),

        }

        paper["_scores"] = scores



    # --- Step 3: 分类 ---

    for paper in papers:

        paper["_tags"] = classify(paper)



    # --- Step 4: 排序 ---

    ranked = sort_papers(papers, mode)



    # --- 统计摘要 ---

    tag_counts = {}

    for p in ranked:

        for tag in p["_tags"]:

            tag_counts[tag] = tag_counts.get(tag, 0) + 1



    with_rel = sum(1 for p in ranked if p["_scores"]["relevance"] is not None)

    with_abs = sum(1 for p in ranked if p.get("abstract") and len(p["abstract"]) > 50)

    avg_impact = round(sum(p["_scores"]["impact"] for p in ranked) / max(len(ranked), 1), 1)



    # --- 日志 ---

    print(f"[Ranker] {total} → {len(ranked)} papers (mode: {mode})")

    if has_keywords:

        print(f"[Ranker] Keywords: {', '.join(kw_list[:5])}"

              f"{'...' if len(kw_list) > 5 else ''}")

    print(f"[Ranker] Relevance scored: {with_rel}/{len(ranked)}")

    print(f"[Ranker] With abstracts: {with_abs}/{len(ranked)}")

    print(f"[Ranker] Avg impact: {avg_impact}")

    print(f"[Ranker] Tags: {', '.join(f'{k}:{v}' for k, v in sorted(tag_counts.items()))}")



    # --- 校验 + 报告 ---

    ok, issues = validate(ranked, stage="ranked")

    if issues:

        report(issues, stage="ranked")



    # --- 输出 ---

    if isinstance(data, dict) and "papers" in data:

        data["papers"] = ranked

        data["_scoring"] = {

            "mode": mode,

            "keywords": kw_list,

            "total_scored": len(ranked),

            "avg_impact": avg_impact,

            "tag_distribution": tag_counts,

        }

        output_data = data

    else:

        output_data = {"papers": ranked}



    if output_path:

        out = Path(output_path)

        out.parent.mkdir(parents=True, exist_ok=True)

        stamp(output_data, stage="ranked")

        with open(out, "w", encoding="utf-8") as f:

            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Saved to {out}")

    else:

        # NEVER print full paper data to stdout — that enters AI context.

        # Print summary only. Use -o for file output.

        print(f"\n[Ranker] Use -o to write ranked results to file.")

        print(f"[Ranker] Summary only (no paper data in stdout):")

        print(f"  Papers: {len(ranked)}")

        print(f"  Tags: {', '.join(f'{k}:{v}' for k, v in sorted(tag_counts.items()))}")

        print(f"  Top 3: {', '.join(p['title'][:40]+'...' for p in ranked[:3])}")





# ---------------------------------------------------------------------------

# CLI

# ---------------------------------------------------------------------------



def main():

    parser = argparse.ArgumentParser(

        description="Paper Ranker — multi-dimensional scoring & classification",

        formatter_class=argparse.RawDescriptionHelpFormatter,

        epilog="""

Examples:

  python paper_ranker.py -i merged.json -o ranked.json --keywords "transformer, attention"

  python paper_ranker.py -i merged.json -o ranked.json --mode seminal

  python paper_ranker.py -i merged.json --keywords "GAN" --mode frontier



Modes:

  balanced   Relevance-first, balanced weighting (default)

  seminal    Impact-first, find classic/seminal works

  frontier   Recency-first, track latest research

  quick      Accessibility-first, find immediately readable papers

        """,

    )

    parser.add_argument("--input", "-i", required=True, help="Input JSON (merged results)")

    parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    parser.add_argument("--keywords", "-k", help="Search keywords, comma-separated")

    parser.add_argument(

        "--mode", "-m", default="balanced",

        choices=list(SEARCH_MODES.keys()),

        help="Sorting mode (default: balanced)"

    )

    parser.add_argument("--min-score", type=float, default=0,

                        help="Minimum average score to include (default: 0)")

    args = parser.parse_args()



    if not Path(args.input).exists():

        print(f"[ERROR] File not found: {args.input}", file=sys.stderr)

        sys.exit(1)



    rank_papers(

        args.input, args.output,

        keywords=args.keywords,

        mode=args.mode,

        min_score=args.min_score,

    )





if __name__ == "__main__":

    main()

