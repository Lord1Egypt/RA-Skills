#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 文件：main.py
import sys, json, argparse, re, time
from typing import List, Dict, Any
import requests

# 设置Windows控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 尝试导入机器学习依赖
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False

# ------------------- 配置 -------------------
DEFAULT_CONFIG = {
    "default_years": 5,
    "max_papers": 50,
    "use_llm_for_writing": False,
    "llm_model": "deepseek-chat",
    "llm_api_base": "https://api.deepseek.com/v1",
    "output_format": "markdown",
    "human_review_papers": False
}

# ------------------- 检索模块 -------------------
def search_semantic_scholar(query: str, year_start: int, year_end: int, limit: int = 100) -> List[Dict]:
    """调用Semantic Scholar API"""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "year": f"{year_start}-{year_end}",
        "limit": min(limit, 100),
        "fields": "title,authors,year,abstract,referenceCount,citationCount,doi,openAccessPdf"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        papers = []
        for p in data.get("data", []):
            papers.append({
                "title": p.get("title"),
                "authors": [a.get("name") for a in p.get("authors", [])],
                "year": p.get("year"),
                "abstract": p.get("abstract"),
                "citations": p.get("citationCount"),
                "doi": p.get("doi"),
                "url": p.get("openAccessPdf", {}).get("url") if p.get("openAccessPdf") else None,
                "source": "semantic_scholar"
            })
        return papers
    except Exception as e:
        print(f"Semantic Scholar检索失败: {e}", file=sys.stderr)
        return []

def search_arxiv(query: str, year_start: int, year_end: int, limit: int = 50) -> List[Dict]:
    """调用arXiv API（按年份过滤需自行处理）"""
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": limit,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        # 解析XML（简化，实际需用xml.etree）
        # 为简化示例，返回空列表，真实实现需解析Atom feed
        return []
    except Exception as e:
        print(f"arXiv检索失败: {e}", file=sys.stderr)
        return []

def search_crossref(query: str, year_start: int, year_end: int, limit: int = 50) -> List[Dict]:
    """调用CrossRef API"""
    url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "filter": f"from-pub-date:{year_start},until-pub-date:{year_end}",
        "rows": limit,
        "sort": "relevance"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        papers = []
        for item in data.get("message", {}).get("items", []):
            papers.append({
                "title": item.get("title", [None])[0],
                "authors": [f"{a.get('given','')} {a.get('family','')}" for a in item.get("author", [])],
                "year": item.get("published-print", {}).get("date-parts", [[None]])[0][0],
                "abstract": item.get("abstract"),
                "citations": None,
                "doi": item.get("DOI"),
                "url": item.get("URL"),
                "source": "crossref"
            })
        return papers
    except Exception as e:
        print(f"CrossRef检索失败: {e}", file=sys.stderr)
        return []

def merge_and_deduplicate(papers_list: List[List[Dict]]) -> List[Dict]:
    """合并多个来源，按DOI和标题去重"""
    seen_dois = set()
    seen_titles = set()
    merged = []
    for papers in papers_list:
        for p in papers:
            doi = p.get("doi")
            title = p.get("title", "").lower().strip()
            if doi and doi in seen_dois:
                continue
            if title and title in seen_titles:
                continue
            if doi:
                seen_dois.add(doi)
            if title:
                seen_titles.add(title)
            merged.append(p)
    return merged

# ------------------- 相关性筛选 -------------------
def rank_by_relevance(papers: List[Dict], query: str, top_k: int) -> List[Dict]:
    """计算摘要与查询的相似度（优先TF-IDF，回退到关键词匹配）"""
    texts = [p.get("abstract", "") or p.get("title", "") for p in papers]
    if not texts:
        return papers[:top_k]
    
    if ML_AVAILABLE:
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(texts)
            query_vec = vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            indexed = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
            ranked = [papers[i] for i, _ in indexed[:top_k]]
            return ranked
        except Exception:
            pass
    
    # 回退：简单关键词匹配
    query_words = set(query.lower().split())
    scores = []
    for i, text in enumerate(texts):
        text_words = set(text.lower().split())
        score = len(query_words & text_words)
        scores.append((-score, i))  # 负号用于升序排列
    
    scores.sort()
    ranked = [papers[i] for _, i in scores[:top_k]]
    return ranked

# ------------------- 聚类分析 -------------------
def simple_cluster_by_keywords(papers: List[Dict], n_clusters=4) -> Dict:
    """
    简易聚类：基于标题和摘要的关键词共现，使用KMeans（需降维）。
    这里仅演示返回伪代码，实际可使用BERTopic或LDA。
    """
    # 文本预处理略
    # 返回聚类结果结构
    clusters = {
        "clusters": [
            {"topic": "研究方法", "papers": papers[:len(papers)//4]},
            {"topic": "应用场景", "papers": papers[len(papers)//4:2*len(papers)//4]},
        ],
        "year_trend": {}
    }
    # 统计每年发文
    year_counts = {}
    for p in papers:
        y = p.get("year")
        if y:
            year_counts[y] = year_counts.get(y, 0) + 1
    clusters["year_trend"] = year_counts
    return clusters

# ------------------- 综述生成 -------------------
def generate_review_local(topic: str, papers: List[Dict], clusters: Dict) -> str:
    """纯本地模板生成综述"""
    lines = []
    lines.append(f"# 关于“{topic}”的文献综述（自动生成）")
    lines.append("")
    lines.append("## 摘要")
    lines.append(f"本综述检索了{len(papers)}篇相关文献，归纳出{len(clusters['clusters'])}个主要研究方向。")
    lines.append("")
    lines.append("## 主要研究方向")
    for idx, c in enumerate(clusters["clusters"], 1):
        lines.append(f"### {idx}. {c['topic']}")
        for p in c["papers"][:5]:  # 每个方向最多展示5篇
            title = p.get("title", "无标题")
            authors = ", ".join(p.get("authors", [])[:3])
            year = p.get("year", "未知")
            lines.append(f"- **{title}** ({authors}, {year})")
        lines.append("")
    lines.append("## 年度发文趋势")
    year_trend = clusters["year_trend"]
    if year_trend:
        years_sorted = sorted(year_trend.items())
        lines.append(", ".join([f"{y}: {c}" for y, c in years_sorted]))
    else:
        lines.append("无年度数据")
    lines.append("")
    lines.append("## 参考文献")
    for i, p in enumerate(papers, 1):
        lines.append(f"{i}. {p.get('title', '')} {p.get('doi', '')}")
    lines.append("")
    lines.append("*(注：本综述基于自动检索与模板生成，内容仅供参考。)*")
    return "\n".join(lines)

def generate_review_with_llm(topic: str, papers: List[Dict], clusters: Dict, config: Dict) -> str:
    """调用大模型生成综述（需配置API密钥）"""
    api_key = config.get("llm_api_key")
    if not api_key:
        return generate_review_local(topic, papers, clusters) + "\n\n> 警告：未配置大模型API密钥，降级为本地模板。"
    # 组装prompt
    paper_summaries = "\n".join([f"- {p['title']} ({p.get('year','')}): {p.get('abstract','无摘要')[:200]}..." for p in papers[:15]])
    prompt = f"""请根据以下文献信息，撰写一篇关于“{topic}”的学术文献综述。要求包含摘要、引言、按主题分类的讨论（至少2个主题）、研究趋势与挑战、结论与展望。字数800-1200字。

检索到{len(papers)}篇相关论文，主要聚类主题有：{', '.join([c['topic'] for c in clusters['clusters']])}。

代表性论文摘要：
{paper_summaries}

请输出Markdown格式。"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": config.get("llm_model"),
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }
    api_base = config.get("llm_api_base")
    try:
        resp = requests.post(f"{api_base}/chat/completions", headers=headers, json=data, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        content = result["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        print(f"大模型调用失败: {e}", file=sys.stderr)
        return generate_review_local(topic, papers, clusters) + "\n\n> 大模型生成失败，回退至本地模板。"

# ------------------- 主函数 -------------------
def main():
    parser = argparse.ArgumentParser(description="文献检索与综述生成")
    parser.add_argument("--topic", type=str, required=True, help="研究主题")
    parser.add_argument("--years", type=int, help="检索年数", default=None)
    parser.add_argument("--max_papers", type=int, help="最大保留文献数", default=None)
    parser.add_argument("--output", type=str, help="输出文件路径（不含后缀）", default="literature_review")
    parser.add_argument("--config", type=str, help="JSON配置", default="{}")
    args = parser.parse_args()
    
    # 加载配置
    config = DEFAULT_CONFIG.copy()
    if args.config:
        try:
            user_config = json.loads(args.config)
            config.update(user_config)
        except:
            pass
    if args.years is not None:
        config["default_years"] = args.years
    if args.max_papers is not None:
        config["max_papers"] = args.max_papers
    
    topic = args.topic
    year_end = 2026  # 动态获取当前年份？可以调用time
    year_start = year_end - config["default_years"]
    
    print(f"开始检索主题: {topic} ({year_start}-{year_end})")
    # 并发检索（简化示例顺序执行）
    ss_papers = search_semantic_scholar(topic, year_start, year_end, 100)
    arxiv_papers = search_arxiv(topic, year_start, year_end, 50)
    cross_papers = search_crossref(topic, year_start, year_end, 50)
    all_papers = merge_and_deduplicate([ss_papers, arxiv_papers, cross_papers])
    print(f"去重后共获取 {len(all_papers)} 篇候选文献")
    
    # 筛选
    if len(all_papers) > config["max_papers"]:
        all_papers = rank_by_relevance(all_papers, topic, config["max_papers"])
        print(f"相关性筛选后保留 {len(all_papers)} 篇")
    
    # 聚类
    clusters = simple_cluster_by_keywords(all_papers)
    
    # 生成综述
    if config.get("use_llm_for_writing"):
        review = generate_review_with_llm(topic, all_papers, clusters, config)
    else:
        review = generate_review_local(topic, all_papers, clusters)
    
    # 输出文件
    output_path = f"{args.output}.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(review)
    
    # 输出BibTeX
    bib_path = f"{args.output}.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        for p in all_papers:
            if p.get("doi"):
                f.write(f"@article{{,\n  doi = {{{p['doi']}}},\n  title = {{{p['title']}}},\n  year = {{{p.get('year')}}},\n}}\n\n")
    
    # 打印结果摘要（供OpenClaw捕获）
    print(json.dumps({
        "status": "success",
        "num_papers": len(all_papers),
        "num_clusters": len(clusters.get("clusters", [])),
        "output_file": output_path,
        "bib_file": bib_path
    }))
    print(f"综述已生成: {output_path}")

if __name__ == "__main__":
    main()