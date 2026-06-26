#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
论文检阅主程序（重写版）

关键特性：
1. keep_topk 仅来自原始检索
2. 扩展检索独立，不参与排序
3. 扩展词固定保留 expand_query_number 条
4. 所有结果均保存并写入 index

新增功能（2026-03-29）：
- 自动导出 BibTeX 文件，方便导入 Zotero
- 获取论文发表状态与 CCF 评级
- 综合评分（相关度 + 权威度）优化 Top-K 排序
- 10 分钟卡死脱离保护（无输出自动终止）
"""

import argparse
import json
import os
import sys
import signal
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HUB_ENDPOINT"] = "https://hf-mirror.com"

from search.arxiv import search_arxiv
from search.semantic import search_semantic
from core.similarity import SimilarityModel
from core.expansion import expand_query
from core.dedup import deduplicate
from core.summarizer import summarize
from core.storage import save_paper
from core.publication_status import enrich_papers_with_publication_status
from core.bibtex import export_bibtex, generate_bibtex_path
from core.report import generate_report, save_report


# =========================
# 卡死脱离保护 - 10 分钟无输出自动终止
# =========================

class TimeoutMonitor:
    """监控程序输出，超时自动终止"""
    
    def __init__(self, timeout_seconds=600):
        self.timeout = timeout_seconds
        self.last_activity = None
        self.alive = True
        
    def touch(self):
        """记录活动"""
        import time
        self.last_activity = time.time()
        
    def check(self):
        """检查是否超时"""
        import time
        if self.last_activity is None:
            return
        elapsed = time.time() - self.last_activity
        if elapsed > self.timeout:
            print(f"\n\n⚠️  卡死检测：超过 {self.timeout} 秒无输出，强制终止程序")
            sys.exit(1)
    
    def start_monitoring(self):
        """启动监控"""
        import time
        import threading
        
        self.last_activity = time.time()
        
        def monitor_loop():
            while self.alive:
                time.sleep(30)  # 每 30 秒检查一次
                self.check()
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
    
    def stop(self):
        """停止监控"""
        self.alive = False


# 全局监控器
timeout_monitor = TimeoutMonitor(timeout_seconds=600)  # 10 分钟


def activity_hook():
    """在关键操作前后调用，记录活动"""
    timeout_monitor.touch()


CONFIG_PATH = os.path.expanduser("~/.openclaw/paper-review-pro/config.json")


# =========================
# 工具函数
# =========================

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def load_index(path):
    if not os.path.exists(path):
        return {"papers": []}
    return json.load(open(path))


def save_index(path, index):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(index, open(path, "w"), indent=2)


# =========================
# 主流程
# =========================

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--query", required=True)
    parser.add_argument("--retrieve_number", type=int)
    parser.add_argument("--keep_topk", type=int)
    parser.add_argument("--year", type=int)
    parser.add_argument("--expand_query_number", type=int, default=1, help="每个扩展词保留数量")
    parser.add_argument("--no-llm", action="store_true", help="禁用 LLM 功能（使用规则 fallback）")
    
    # 新功能参数
    parser.add_argument("--no-bibtex", action="store_true", help="禁用 BibTeX 导出")
    parser.add_argument("--no-authority", action="store_true", help="禁用权威度评分（仅使用相关度）")
    parser.add_argument("--authority-weight", type=float, default=0.3, help="权威度分数权重（0.0-1.0，默认 0.3）")
    parser.add_argument("--use-api", action="store_true", default=True, help="使用在线 API 查询发表状态（较慢但更准确，默认启用）")
    parser.add_argument("--no-use-api", dest="use_api", action="store_false", help="禁用在线 API 查询（仅使用本地数据库）")

    args = parser.parse_args()

    config = load_config()
    
    # 设置 LLM 相关环境变量（供子模块使用）
    llm_config = config.get("llm", {})
    if llm_config.get("enabled", True):
        os.environ.setdefault("OPENCLAW_GATEWAY_URL", llm_config.get("gateway_url", "http://localhost:14940"))
        os.environ.setdefault("DASHSCOPE_MODEL", llm_config.get("dashscope_model", "qwen3.5-plus"))

    n = args.retrieve_number or config["default_n"]
    k = args.keep_topk or config["default_k"]
    year = args.year or config["min_year"]
    p = args.expand_query_number if args.expand_query_number else config.get("default_p", 2)

    index = load_index(config["storage"]["index_file"])

    # 启动卡死脱离监控
    timeout_monitor.start_monitoring()
    activity_hook()

    print("=" * 60)
    print("论文检阅系统")
    print("=" * 60)
    print(f"Query: {args.query}")
    print(f"retrieve_number={n}, keep_topk={k}, year>={year}, expand_query_number={p}")
    print(f"卡死保护：{timeout_monitor.timeout}秒无输出自动终止")
    activity_hook()

    # =========================
    # 1️⃣ 原始检索
    # =========================
    print("\n=== 开始检索 ===")
    activity_hook()
    
    papers = []
    
    # 尝试 arXiv 检索
    try:
        arxiv_papers = search_arxiv(args.query, n)
        activity_hook()
        if arxiv_papers:
            papers.extend(arxiv_papers)
            print(f"  [arXiv] 检索到 {len(arxiv_papers)} 篇")
    except Exception as e:
        print(f"  [arXiv 检索失败]: {e}")
    
    # 尝试 Semantic Scholar 检索
    try:
        semantic_papers = search_semantic(args.query, n)
        activity_hook()
        if semantic_papers:
            papers.extend(semantic_papers)
            print(f"  [Semantic Scholar] 检索到 {len(semantic_papers)} 篇")
    except Exception as e:
        print(f"  [Semantic Scholar 检索失败]: {e}")
    
    if not papers:
        print("⚠️ 无检索结果，请检查网络连接")
        timeout_monitor.stop()
        return

    # 年份过滤
    papers = [paper for paper in papers if paper.get("year", 0) >= year]
    activity_hook()

    # 去重
    papers = deduplicate(papers, index)
    activity_hook()

    # =========================
    # 🔹 相关性过滤（新增）
    # =========================
    activity_hook()
    # 提取查询关键词，过滤完全不相关的论文
    query_keywords = set(args.query.lower().split())
    # 移除停用词
    stop_words = {"the", "a", "an", "for", "with", "based", "using", "and", "or", "of", "in", "on", "to"}
    query_keywords = query_keywords - stop_words
    
    filtered_papers = []
    for paper in papers:
        title = paper.get("title") or ""
        abstract = paper.get("abstract") or ""
        title_lower = title.lower()
        abstract_lower = abstract.lower()
        
        # 至少有一个关键词出现在标题或摘要中
        has_keyword = any(kw in title_lower or kw in abstract_lower for kw in query_keywords)
        
        if has_keyword:
            filtered_papers.append(paper)
    
    if filtered_papers:
        papers = filtered_papers
        print(f"  [相关性过滤] 保留 {len(papers)} 篇相关论文")
    elif papers:
        print(f"  [相关性过滤] 警告：无完全匹配论文，使用全部 {len(papers)} 篇")

    if not papers:
        print("⚠️ 无检索结果")
        timeout_monitor.stop()
        return

    # =========================
    # 🔹 新增：获取发表状态与 CCF 评级
    # =========================
    activity_hook()
    use_authority = not args.no_authority
    if use_authority:
        papers = enrich_papers_with_publication_status(papers, use_api=args.use_api)
        activity_hook()
    else:
        # 即使不使用权威度，也标记预印本状态
        for paper in papers:
            paper["is_preprint"] = "arxiv" in paper.get("url", "").lower() or paper.get("source", "") == "arxiv"
            paper["publication"] = ""
            paper["ccf_rank"] = ""
            paper["authority_score"] = 0.3

    # =========================
    # 2️⃣ 相似度排序（仅用于 Top-K）
    # =========================
    activity_hook()
    sim_model = SimilarityModel()
    
    if use_authority:
        # 使用综合评分（相关度 + 权威度）
        print(f"\n=== 综合评分（权威度权重={args.authority_weight}）===")
        papers = sim_model.compute_with_authority(args.query, papers, authority_weight=args.authority_weight)
        # 使用综合分数排序
        papers.sort(key=lambda x: x.get("sim_combined", x["sim"]), reverse=True)
    else:
        # 仅使用相关度评分
        papers = sim_model.compute(args.query, papers)
        papers.sort(key=lambda x: x["sim"], reverse=True)

    topk = papers[:k]

    # =========================
    # 3️⃣ 扩展词生成
    # =========================
    activity_hook()
    reference_paper = papers[:3]  # 取前 3 篇作为扩展参考
    use_llm = not args.no_llm and config.get("llm", {}).get("enabled", True)
    expansions = expand_query(reference_paper, args.query, max_terms=p, use_llm=use_llm)
    activity_hook()

    # =========================
    # 4️⃣ 扩展检索（独立分支）
    # =========================
    expanded_results = []

    print("\n=== 扩展检索 ===")
    activity_hook()

    for e in expansions:
        term = e["term"]
        score = e["score"]

        print(f"\n扩展词：{term} (score={score:.2f})")
        activity_hook()

        results = search_arxiv(term, 5)
        activity_hook()

        # 年份过滤
        results = [r for r in results if r.get("year", 0) >= year]

        # 仅取前 p 条（确保 p 是整数）
        p_int = int(p) if isinstance(p, int) else 2
        results = results[:p_int]

        for r in results:
            r["expansion_term"] = term

        expanded_results.extend(results)

        print(f"  保留 {len(results)} 条")
        activity_hook()

    # =========================
    # 5️⃣ 保存 Top-K
    # =========================
    saved_topk = []

    print("\n=== Top-K 核心论文 ===")
    activity_hook()

    for i, paper in enumerate(topk, 1):
        summary = summarize(paper, use_llm=use_llm)
        activity_hook()
        path = save_paper(paper, summary, config)
        activity_hook()

        # 构建更完整的索引信息
        index_entry = {
            "query": args.query,
            "title": paper["title"],
            "similarity": paper.get("sim_combined", paper["sim"]),
            "similarity_base": paper["sim"],
            "year": paper.get("year"),
            "url": paper.get("url"),
            "authors": paper.get("authors", []),
            "type": "core",
            "path": path,
            # 新增字段
            "is_preprint": paper.get("is_preprint", False),
            "publication": paper.get("publication", ""),
            "ccf_rank": paper.get("ccf_rank", ""),
            "authority_score": paper.get("authority_score", 0.3)
        }
        index["papers"].append(index_entry)

        saved_topk.append(paper)

        # 显示论文信息（包含发表状态）
        pub_info = ""
        if paper.get("ccf_rank"):
            pub_info = f" [CCF-{paper['ccf_rank']}]"
        elif paper.get("publication"):
            pub_info = f" [{paper['publication']}]"
        elif paper.get("is_preprint"):
            pub_info = " [preprint]"
        
        sim_score = paper.get("sim_combined", paper["sim"])
        print(f"{i}. {paper['title']}{pub_info} (score={sim_score:.3f})")
        print(f"--Main focus: {summary.get('研究问题', 'N/A')}")

    # =========================
    # 6️⃣ 保存扩展论文（不参与排序）
    # =========================
    saved_expanded = []

    print("\n=== 扩展检索论文 ===")
    activity_hook()

    for paper in expanded_results:
        summary = summarize(paper, use_llm=use_llm)
        activity_hook()
        path = save_paper(paper, summary, config)
        activity_hook()

        index["papers"].append({
            "query": args.query,
            "title": paper["title"],
            "similarity": None,
            "year": paper.get("year"),
            "url": paper.get("url"),
            "authors": paper.get("authors", []),
            "type": "expansion",
            "expansion_term": paper.get("expansion_term"),
            "path": path
        })

        saved_expanded.append(paper)

        print(f"- [{paper.get('expansion_term')}] {paper['title']}")
        print(f"--Main focus: {summary.get('研究问题', 'N/A')}")

    # =========================
    # 7️⃣ 保存索引
    # =========================
    save_index(config["storage"]["index_file"], index)
    activity_hook()

    # =========================
    # 8️⃣ 新增：导出 BibTeX 文件
    # =========================
    if not args.no_bibtex and saved_topk:
        print("\n=== 导出 BibTeX ===")
        activity_hook()
        try:
            bibtex_path = generate_bibtex_path(args.query, config)
            export_bibtex(saved_topk, bibtex_path)
            activity_hook()
            print(f"✓ BibTeX 文件已生成：{bibtex_path}")
            print("  导入 Zotero: File → Import → From File → 选择上述.bib 文件")
        except Exception as e:
            print(f"⚠️ BibTeX 导出失败：{e}")

    # =========================
    # 9️⃣ 最终报告
    # =========================
    print("\n" + "=" * 60)
    print("检阅完成")
    print("=" * 60)
    activity_hook()

    print(f"Top-K: {len(saved_topk)} 篇")
    print(f"扩展论文：{len(saved_expanded)} 篇")
    print(f"总检索：{len(saved_topk) + len(saved_expanded)} 篇")
    
    # 统计发表情况
    if use_authority:
        ccf_a = sum(1 for p in saved_topk if p.get("ccf_rank") == "A")
        ccf_b = sum(1 for p in saved_topk if p.get("ccf_rank") == "B")
        ccf_c = sum(1 for p in saved_topk if p.get("ccf_rank") == "C")
        preprint = sum(1 for p in saved_topk if p.get("is_preprint", False))
        print(f"\n发表统计:")
        print(f"  CCF-A: {ccf_a} 篇 | CCF-B: {ccf_b} 篇 | CCF-C: {ccf_c} 篇 | 预印本：{preprint} 篇")
    
    # =========================
    # 🔟 生成详细总结报告
    # =========================
    print("\n=== 生成总结报告 ===")
    activity_hook()
    try:
        report = generate_report(args.query, saved_topk, saved_expanded, expansions, config, use_authority)
        report_path = save_report(report, args.query, config)
        activity_hook()
        print(f"✓ 报告已生成：{report_path}")
    except Exception as e:
        print(f"⚠️ 报告生成失败：{e}")
        import traceback
        traceback.print_exc()
    
    # 停止监控
    timeout_monitor.stop()


if __name__ == "__main__":
    main()
