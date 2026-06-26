# -*- coding: utf-8 -*-
"""
文献智能检索与综述生成器
自动检索学术文献，进行相关性筛选、主题聚类分析，并生成综述草稿
"""
import sys
import os
import re
import json
import requests
import time
import argparse
from datetime import datetime
from typing import List, Dict, Set, Optional, Tuple
from collections import defaultdict, Counter

# 设置Windows控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 尝试导入机器学习依赖
ML_AVAILABLE = False
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    ML_AVAILABLE = True
except Exception:
    ML_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    from bertopic import BERTopic
    BERTOPIC_AVAILABLE = True
except ImportError:
    BERTOPIC_AVAILABLE = False

# 配置默认值
DEFAULT_CONFIG = {
    "default_years": 5,
    "max_papers": 50,
    "use_llm_for_writing": False,
    "llm_model": "deepseek-chat",
    "llm_api_base": "https://api.deepseek.com/v1",
    "output_format": "markdown",
    "human_review_papers": False
}


class LiteratureReviewer:
    def __init__(self, config: Dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.papers = []
        self.clusters = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def parse_request(self, user_input: str) -> Dict:
        """解析用户请求，提取关键词和参数"""
        print("🔍 正在解析请求...")
        
        # 提取时间范围
        year_match = re.search(r'近(\d+)年|(\d+)\s*年', user_input)
        years = int(year_match.group(1) or year_match.group(2)) if year_match else self.config["default_years"]
        
        # 提取最大文献数
        max_match = re.search(r'最多(\d+)篇|前(\d+)篇', user_input)
        max_papers = int(max_match.group(1) or max_match.group(2)) if max_match else self.config["max_papers"]
        
        # 提取核心关键词（移除指令性词汇）
        stop_words = ['帮我', '检索', '文献', '综述', '写一篇', '研究热点', '论文', '关于', 
                      '的', '最新进展', '给我', '一份', '概览', '了解', '领域', '趋势']
        
        keywords = user_input
        for word in stop_words:
            keywords = re.sub(word, '', keywords)
        keywords = keywords.strip()
        
        # 生成英文关键词（简单映射）
        en_keywords = self._translate_to_english(keywords)
        
        print(f"   关键词: {keywords}")
        print(f"   英文关键词: {en_keywords}")
        print(f"   时间范围: 近{years}年")
        print(f"   最大文献数: {max_papers}篇")
        
        return {
            "keywords": keywords,
            "en_keywords": en_keywords,
            "years": years,
            "max_papers": max_papers
        }

    def _translate_to_english(self, text: str) -> str:
        """简单的中译英关键词映射"""
        translations = {
            '联邦学习': 'federated learning',
            '工业视觉': 'industrial vision',
            '大模型': 'large language model LLM',
            '微调': 'fine-tuning fine tuning',
            '柔性机器人': 'soft robotics flexible robot',
            '深度学习': 'deep learning',
            '强化学习': 'reinforcement learning',
            '计算机视觉': 'computer vision',
            '自然语言处理': 'NLP natural language processing',
            '目标检测': 'object detection',
            '图像分割': 'image segmentation',
            '生成对抗网络': 'GAN generative adversarial network',
            'Transformer': 'Transformer attention mechanism',
            '多模态': 'multimodal multi-modal',
            '知识图谱': 'knowledge graph',
            '推荐系统': 'recommender system recommendation',
            '自动驾驶': 'autonomous driving self-driving',
            '机器人': 'robot robotics',
            '边缘计算': 'edge computing',
            '物联网': 'IoT Internet of Things',
            '人工智能': 'AI artificial intelligence',
            '机器学习': 'machine learning ML'
        }
        
        result = text
        for cn, en in translations.items():
            if cn in text:
                result += ' ' + en
        
        return result.strip() if result != text else text

    def search_semantic_scholar(self, keywords: str, years: int, limit: int = 50) -> List[Dict]:
        """从Semantic Scholar检索文献"""
        print("\n📚 正在检索 Semantic Scholar...")
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        current_year = datetime.now().year
        
        params = {
            "query": keywords,
            "limit": min(limit, 100),
            "year": f"{current_year - years}-{current_year}",
            "fields": "title,authors,year,abstract,citationCount,externalIds,url,journal"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for paper in data.get('data', []):
                papers.append({
                    'title': paper.get('title', ''),
                    'authors': [a.get('name', '') for a in paper.get('authors', [])[:3]],
                    'year': paper.get('year', current_year),
                    'abstract': paper.get('abstract', ''),
                    'citations': paper.get('citationCount', 0),
                    'doi': paper.get('externalIds', {}).get('DOI', ''),
                    'url': paper.get('url', ''),
                    'source': 'Semantic Scholar',
                    'journal': paper.get('journal', {}).get('name', '') if paper.get('journal') else ''
                })
            
            print(f"   找到 {len(papers)} 篇文献")
            return papers
        except Exception as e:
            print(f"   Semantic Scholar 检索失败: {e}")
            return []

    def search_arxiv(self, keywords: str, years: int, limit: int = 30) -> List[Dict]:
        """从arXiv检索文献"""
        print("\n📘 正在检索 arXiv...")
        url = "http://export.arxiv.org/api/query"
        
        params = {
            "search_query": f"all:{keywords}",
            "start": 0,
            "max_results": min(limit, 50),
            "sortBy": "relevance",
            "sortOrder": "descending"
        }
        
        try:
            import xml.etree.ElementTree as ET
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            papers = []
            current_year = datetime.now().year
            
            for entry in root.findall('atom:entry', ns):
                year_elem = entry.find('atom:published', ns)
                paper_year = int(year_elem.text[:4]) if year_elem is not None else current_year
                
                if paper_year < current_year - years:
                    continue
                
                authors = []
                for author in entry.findall('atom:author', ns):
                    name = author.find('atom:name', ns)
                    if name is not None:
                        authors.append(name.text)
                
                title = entry.find('atom:title', ns)
                summary = entry.find('atom:summary', ns)
                id_elem = entry.find('atom:id', ns)
                
                doi = ''
                url = id_elem.text if id_elem is not None else ''
                if url and 'arxiv.org' in url:
                    arxiv_id = url.split('/')[-1]
                    doi = f"10.48550/arXiv.{arxiv_id}"
                
                papers.append({
                    'title': title.text if title is not None else '',
                    'authors': authors[:3],
                    'year': paper_year,
                    'abstract': summary.text if summary is not None else '',
                    'citations': 0,
                    'doi': doi,
                    'url': url,
                    'source': 'arXiv',
                    'journal': 'arXiv preprint'
                })
            
            print(f"   找到 {len(papers)} 篇文献")
            return papers
        except Exception as e:
            print(f"   arXiv 检索失败: {e}")
            return []

    def search_crossref(self, keywords: str, years: int, limit: int = 30) -> List[Dict]:
        """从CrossRef检索文献"""
        print("\n📑 正在检索 CrossRef...")
        url = "https://api.crossref.org/works"
        current_year = datetime.now().year
        
        params = {
            "query": keywords,
            "rows": min(limit, 50),
            "filter": f"from-pub-date:{current_year - years}-01-01",
            "sort": "relevance"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            papers = []
            for item in data.get('message', {}).get('items', []):
                date_parts = item.get('published-print', item.get('published-online', {})).get('date-parts', [[current_year]])
                paper_year = date_parts[0][0] if date_parts else current_year
                
                authors = []
                for author in item.get('author', [])[:3]:
                    given = author.get('given', '')
                    family = author.get('family', '')
                    if given or family:
                        authors.append(f"{given} {family}".strip())
                
                papers.append({
                    'title': item.get('title', [''])[0] if item.get('title') else '',
                    'authors': authors,
                    'year': paper_year,
                    'abstract': item.get('abstract', ''),
                    'citations': item.get('is-referenced-by-count', 0),
                    'doi': item.get('DOI', ''),
                    'url': f"https://doi.org/{item.get('DOI', '')}",
                    'source': 'CrossRef',
                    'journal': item.get('container-title', [''])[0] if item.get('container-title') else ''
                })
            
            print(f"   找到 {len(papers)} 篇文献")
            return papers
        except Exception as e:
            print(f"   CrossRef 检索失败: {e}")
            return []

    def search_all(self, keywords: str, en_keywords: str, years: int, max_papers: int) -> List[Dict]:
        """并发检索所有数据源"""
        all_papers = []
        
        # 优先使用英文关键词检索
        search_terms = en_keywords if en_keywords != keywords else keywords
        
        # 检索各个数据源
        all_papers.extend(self.search_semantic_scholar(search_terms, years, max_papers))
        time.sleep(1)  # 避免请求过快
        all_papers.extend(self.search_arxiv(search_terms, years, max_papers // 2))
        time.sleep(1)
        all_papers.extend(self.search_crossref(search_terms, years, max_papers // 2))
        
        print(f"\n📊 共检索到 {len(all_papers)} 篇文献")
        return all_papers

    def deduplicate_papers(self, papers: List[Dict]) -> List[Dict]:
        """去除重复文献"""
        seen_dois: Set[str] = set()
        seen_titles: Set[str] = set()
        unique_papers = []
        
        for paper in papers:
            # 基于DOI去重
            doi = paper.get('doi', '').lower().strip()
            if doi and doi in seen_dois:
                continue
            
            # 基于标题相似度去重
            title = paper.get('title', '').lower().strip()
            title_normalized = re.sub(r'[^\w\s]', '', title)
            
            if not title:
                continue
                
            is_duplicate = False
            for seen_title in seen_titles:
                if len(title_normalized) > 10 and title_normalized in seen_title or seen_title in title_normalized:
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                if doi:
                    seen_dois.add(doi)
                seen_titles.add(title_normalized)
                unique_papers.append(paper)
        
        print(f"   去重后剩余 {len(unique_papers)} 篇文献")
        return unique_papers

    def filter_by_relevance(self, papers: List[Dict], keywords: str, max_papers: int) -> List[Dict]:
        """基于相关性筛选文献"""
        print(f"\n🎯 正在进行相关性筛选...")
        
        if not ML_AVAILABLE:
            print("   scikit-learn不可用，基于简单关键词匹配筛选")
            # 简单关键词匹配
            keyword_list = keywords.lower().split()
            scored_papers = []
            
            for paper in papers:
                text = (paper.get('title', '') + ' ' + paper.get('abstract', '')).lower()
                score = sum(1 for kw in keyword_list if kw in text)
                scored_papers.append((score, paper))
            
            scored_papers.sort(key=lambda x: (-x[0], -x[1].get('citations', 0)))
            filtered = [p for s, p in scored_papers if s > 0][:max_papers]
        else:
            # 使用TF-IDF计算相似度
            texts = []
            valid_papers = []
            
            for paper in papers:
                text = (paper.get('title', '') + ' ' + paper.get('abstract', '')).strip()
                if len(text) > 20:  # 过滤太短的文本
                    texts.append(text)
                    valid_papers.append(paper)
            
            if texts:
                vectorizer = TfidfVectorizer(stop_words='english')
                tfidf_matrix = vectorizer.fit_transform(texts + [keywords])
                
                # 计算与关键词的相似度
                similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])[0]
                
                # 结合引用数加权
                max_citations = max(p.get('citations', 1) for p in valid_papers) if valid_papers else 1
                scored = []
                for i, (sim, paper) in enumerate(zip(similarities, valid_papers)):
                    citation_score = np.log(paper.get('citations', 0) + 1) / np.log(max_citations + 1)
                    final_score = sim * 0.7 + citation_score * 0.3  # 70%相关性 + 30%引用数
                    scored.append((final_score, paper))
                
                scored.sort(key=lambda x: -x[0])
                filtered = [p for s, p in scored if s > 0.05][:max_papers]
            else:
                filtered = papers[:max_papers]
        
        print(f"   筛选后保留 {len(filtered)} 篇最相关文献")
        return filtered

    def cluster_papers(self, papers: List[Dict]) -> List[Dict]:
        """对文献进行主题聚类"""
        print(f"\n🧩 正在进行主题聚类...")
        
        if not papers:
            return []
        
        abstracts = [p.get('abstract', p.get('title', '')) for p in papers]
        
        if BERTOPIC_AVAILABLE and len(papers) >= 5:
            print("   使用BERTopic进行深度聚类")
            try:
                model = BERTopic(verbose=False, min_topic_size=2)
                topics, probs = model.fit_transform(abstracts)
                
                topic_info = model.get_topic_info()
                clusters = defaultdict(list)
                
                for i, topic_id in enumerate(topics):
                    if topic_id != -1:  # -1是噪声
                        topic_words = model.get_topic(topic_id)
                        topic_name = ' '.join([w for w, s in topic_words[:3]])
                        clusters[topic_name].append(papers[i])
                
                self.clusters = [
                    {"name": name, "papers": papers, "count": len(papers)}
                    for name, papers in clusters.items()
                ]
                self.clusters.sort(key=lambda x: -x["count"])
                
                print(f"   识别到 {len(self.clusters)} 个研究主题")
                return self.clusters
            except Exception as e:
                print(f"   BERTopic聚类失败: {e}，使用简单关键词聚类")
        
        # 简单的关键词聚类（回退方案）
        print("   使用关键词聚类")
        key_phrases = []
        for paper in papers:
            text = paper.get('title', '') + ' ' + paper.get('abstract', '')
            words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
            key_phrases.extend(words)
        
        common_words = [w for w, c in Counter(key_phrases).most_common() if c >= 2][:10]
        
        clusters = defaultdict(list)
        unassigned = []
        
        for paper in papers:
            text = paper.get('title', '') + ' ' + paper.get('abstract', '')
            assigned = False
            
            for word in common_words[:6]:
                if word.lower() in text.lower():
                    clusters[word].append(paper)
                    assigned = True
                    break
            
            if not assigned:
                unassigned.append(paper)
        
        if unassigned:
            clusters["其他主题"] = unassigned
        
        self.clusters = [
            {"name": name, "papers": papers, "count": len(papers)}
            for name, papers in clusters.items()
        ]
        self.clusters.sort(key=lambda x: -x["count"])
        
        print(f"   识别到 {len(self.clusters)} 个研究主题")
        return self.clusters

    def analyze_trends(self, papers: List[Dict]) -> Dict:
        """分析研究趋势"""
        # 年度发文趋势
        year_counts = Counter(p.get('year', 0) for p in papers)
        sorted_years = sorted(year_counts.items())
        
        trend_text = ""
        if sorted_years:
            min_year, max_year = sorted_years[0][0], sorted_years[-1][0]
            trend_text = f"{min_year}年至{max_year}年，该领域研究呈现"
            if len(sorted_years) >= 2 and sorted_years[-1][1] > sorted_years[0][1]:
                trend_text += "快速增长趋势，"
            else:
                trend_text += "稳定发展态势，"
            trend_text += f"最高年发文量为{max(year_counts.values())}篇。"
        
        # 热门期刊
        journals = Counter(p.get('journal', '') for p in papers if p.get('journal'))
        top_journals = [j for j, c in journals.most_common(5) if j]
        
        return {
            "year_trend": trend_text,
            "year_counts": dict(sorted_years),
            "top_journals": top_journals
        }

    def generate_review(self, topic: str, papers: List[Dict], clusters: List[Dict], trends: Dict) -> str:
        """生成综述草稿"""
        print(f"\n✍️  正在生成综述草稿...")
        
        current_year = datetime.now().year
        years_range = f"{current_year - self.config['default_years']}-{current_year}"
        
        review = f"""# {topic} 研究文献综述

**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**检索范围**: 近{self.config['default_years']}年文献（{years_range}）
**文献数量**: {len(papers)}篇

## 1. 摘要

本文基于{len(papers)}篇学术文献，对"{topic}"领域的研究进展进行了系统性综述。
通过文献计量分析，共识别出{len(clusters)}个主要研究方向。
{trends.get('year_trend', '')}

## 2. 主要研究方向

"""
        
        # 逐个主题生成
        for i, cluster in enumerate(clusters, 1):
            theme_name = cluster['name']
            theme_papers = cluster['papers']
            
            review += f"### 2.{i} {theme_name}\n\n"
            review += f"该方向共包含{len(theme_papers)}篇代表性文献。主要研究进展如下：\n\n"
            
            for paper in theme_papers[:5]:
                authors = ', '.join(paper.get('authors', ['Unknown']))
                title = paper.get('title', 'Untitled')
                year = paper.get('year', current_year)
                abstract = paper.get('abstract', '')
                
                # 提取摘要中的关键句
                key_sentence = ""
                if abstract:
                    sentences = re.split(r'[.!?。！？]', abstract)
                    for s in sentences:
                        if len(s.strip()) > 20 and len(s.strip()) < 100:
                            key_sentence = s.strip()
                            break
                
                citation = f"（引用{paper.get('citations', 0)}次）" if paper.get('citations', 0) > 0 else ""
                review += f"- **{title}** ({authors}, {year}){citation}\n"
                if key_sentence:
                    review += f"  {key_sentence}。\n"
            
            review += "\n"
        
        # 研究趋势与挑战
        review += "## 3. 研究趋势与挑战\n\n"
        review += f"{trends.get('year_trend', '')}\n\n"
        
        if trends.get('top_journals'):
            review += "**主要发表期刊**: " + ", ".join(trends['top_journals']) + "\n\n"
        
        review += "**当前研究热点方向**:\n"
        for i, cluster in enumerate(clusters[:4], 1):
            review += f"- {cluster['name']} ({cluster['count']}篇)\n"
        
        review += "\n**潜在研究机会与挑战**:\n"
        review += "- 跨领域融合方法仍有探索空间\n"
        review += "- 实际应用场景的落地挑战需持续关注\n"
        review += "- 可解释性与安全性问题有待深入研究\n\n"
        
        # 参考文献
        review += "## 4. 参考文献\n\n"
        for i, paper in enumerate(papers, 1):
            authors = ', '.join(paper.get('authors', ['Unknown']))
            title = paper.get('title', 'Untitled')
            year = paper.get('year', current_year)
            journal = paper.get('journal', 'Preprint')
            doi = paper.get('doi', '')
            url = paper.get('url', '')
            
            review += f"[{i}] {authors}. {title}. {journal}, {year}. "
            if doi:
                review += f"DOI: {doi} "
            if url:
                review += f"[链接]({url})"
            review += "\n"
        
        print("   综述生成完成！")
        return review

    def run(self, user_input: str, output_path: str = None) -> str:
        """执行完整的文献综述流程"""
        print("=" * 60)
        print("📚 文献智能检索与综述生成器")
        print("=" * 60)
        
        # 1. 解析请求
        params = self.parse_request(user_input)
        keywords = params["keywords"]
        en_keywords = params["en_keywords"]
        years = params["years"]
        max_papers = params["max_papers"]
        
        self.config["default_years"] = years
        self.config["max_papers"] = max_papers
        
        # 2. 检索文献
        papers = self.search_all(keywords, en_keywords, years, max_papers * 2)
        
        if not papers:
            print("\n❌ 未检索到相关文献，请尝试不同的关键词")
            return ""
        
        # 3. 去重
        papers = self.deduplicate_papers(papers)
        
        # 4. 相关性筛选
        papers = self.filter_by_relevance(papers, en_keywords, max_papers)
        self.papers = papers
        
        # 5. 主题聚类
        clusters = self.cluster_papers(papers)
        
        # 6. 趋势分析
        trends = self.analyze_trends(papers)
        
        # 7. 生成综述
        review = self.generate_review(keywords, papers, clusters, trends)
        
        # 8. 保存输出
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(review)
            print(f"\n💾 综述已保存至: {output_path}")
        
        print("\n" + "=" * 60)
        return review


def main():
    parser = argparse.ArgumentParser(description='文献智能检索与综述生成器')
    parser.add_argument('topic', nargs='?', help='研究主题关键词')
    parser.add_argument('--years', type=int, default=5, help='检索年数')
    parser.add_argument('--max-papers', type=int, default=50, help='最大文献数')
    parser.add_argument('--output', type=str, help='输出文件路径')
    parser.add_argument('--no-cluster', action='store_true', help='跳过聚类分析')
    
    args = parser.parse_args()
    
    if not args.topic:
        print("❌ 请提供研究主题关键词")
        print("\n使用示例:")
        print("  python lit_review.py \"联邦学习在工业视觉中的应用\"")
        print("  python lit_review.py \"大模型微调技术\" --years 3 --max-papers 30")
        print("  python lit_review.py \"柔性机器人\" --output review.md")
        return
    
    config = {
        "default_years": args.years,
        "max_papers": args.max_papers
    }
    
    reviewer = LiteratureReviewer(config)
    review = reviewer.run(args.topic, args.output)
    
    if review and not args.output:
        print("\n" + "=" * 60)
        print(review[:3000] + "..." if len(review) > 3000 else review)


if __name__ == "__main__":
    main()
