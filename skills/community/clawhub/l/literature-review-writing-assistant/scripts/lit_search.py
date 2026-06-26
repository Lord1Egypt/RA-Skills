#!/usr/bin/env python3
"""
Literature Search Tool
文献检索工具 - 支持多源检索、验证、格式化输出

Usage:
    python3 lit_search.py "主题关键词" -n 20 --sources semantic_scholar openalex crossref arxiv pubmed
    python3 lit_search.py "主题关键词" --validate
    python3 lit_search.py "主题关键词" -f apa
    python3 lit_search.py file://papers.txt -f bibtex
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

# ============== 配置 ==============
API_CONFIG = {
    "arxiv": {
        "base_url": "http://export.arxiv.org/api/query",
        "timeout": 30,
    },
    "semantic_scholar": {
        "base_url": "https://api.semanticscholar.org/graph/v1/paper/search",
        "timeout": 30,
        "requires_key": False,
    },
    "openalex": {
        "base_url": "https://api.openalex.org/works",
        "timeout": 30,
    },
    "crossref": {
        "base_url": "https://api.crossref.org/works",
        "timeout": 30,
    },
    "pubmed": {
        "base_url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
        "timeout": 30,
    },
}

# API Keys (可选)
API_KEYS = {
    "semantic_scholar": "",  # 申请: https://www.semanticscholar.org/api-keys
}

# ============== 数据模型 ==============
class Paper:
    """论文数据模型"""
    
    def __init__(self, source: str, paper_id: str, title: str, authors: list,
                 abstract: str = "", year: int = None, venue: str = "",
                 doi: str = "", url: str = "", citations: int = 0,
                 categories: list = None):
        self.source = source          # 来源: arxiv, semantic_scholar, etc.
        self.paper_id = paper_id       # 论文ID (DOI/PMID/arXiv ID)
        self.title = title            # 标题
        self.authors = authors        # 作者列表
        self.abstract = abstract     # 摘要
        self.year = year              # 年份
        self.venue = venue           # 发表场所
        self.doi = doi               # DOI
        self.url = url               # 链接
        self.citations = citations   # 引用数
        self.categories = categories or []  # 分类/关键词
    
    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi,
            "url": self.url,
            "citations": self.citations,
            "categories": self.categories,
        }
    
    def get_source_tag(self) -> str:
        """获取来源标注"""
        if self.source == "arxiv":
            return "[arXiv]"
        elif self.source == "pubmed":
            return "[PubMed]"
        else:
            return "[Published]"
    
    def get_id_type(self) -> str:
        """识别ID类型"""
        if self.paper_id.startswith("arXiv:"):
            return "arXiv"
        elif re.match(r"^\d+$", self.paper_id):
            return "PMID"
        elif self.doi:
            return "DOI"
        return "unknown"
    
    def __eq__(self, other):
        if not isinstance(other, Paper):
            return False
        # 按 DOI 去重
        if self.doi and other.doi and self.doi == other.doi:
            return True
        # 按 arXiv ID 去重
        if self.paper_id.startswith("arXiv:") and self.paper_id == other.paper_id:
            return True
        return False
    
    def __hash__(self):
        return hash(self.doi or self.paper_id)


# ============== 检索模块 ==============
class LiteratureSearcher:
    """文献检索器"""
    
    def __init__(self, sources: list = None, api_keys: dict = None):
        self.sources = sources or ["semantic_scholar", "openalex"]
        self.api_keys = api_keys or API_KEYS
        self.results = []
    
    def search(self, query: str, n: int = 20) -> list[Paper]:
        """搜索论文"""
        results = []
        
        for source in self.sources:
            try:
                papers = self._search_source(source, query, n)
                results.extend(papers)
            except Exception as e:
                print(f"Warning: {source} 检索失败: {e}", file=sys.stderr)
        
        # 去重
        results = self._deduplicate(results)
        
        # 按引用数/年份排序
        results.sort(key=lambda x: (x.citations or 0, x.year or 0), reverse=True)
        
        self.results = results[:n]
        return self.results
    
    def _search_source(self, source: str, query: str, n: int) -> list[Paper]:
        """调用单个源检索"""
        if source == "arxiv":
            return self._search_arxiv(query, n)
        elif source == "semantic_scholar":
            return self._search_semantic_scholar(query, n)
        elif source == "openalex":
            return self._search_openalex(query, n)
        elif source == "crossref":
            return self._search_crossref(query, n)
        elif source == "pubmed":
            return self._search_pubmed(query, n)
        else:
            return []
    
    def _search_arxiv(self, query: str, n: int) -> list[Paper]:
        """arXiv 检索"""
        params = {
            "search_query": f"all:{query}",
            "max_results": n,
            "start": 0,
        }
        
        try:
            resp = requests.get(
                API_CONFIG["arxiv"]["base_url"],
                params=params,
                timeout=API_CONFIG["arxiv"]["timeout"]
            )
            resp.raise_for_status()
            
            # 解析 Atom XML
            papers = []
            from xml.etree import ElementTree as ET
            root = ET.fromstring(resp.content)
            
            for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
                title = entry.findtext("{http://www.w3.org/2005/Atom}title", "")
                summary = entry.findtext("{http://www.w3.org/2005/Atom}summary", "")
                # 清理空白
                title = re.sub(r"\s+", " ", title).strip()
                summary = re.sub(r"\s+", " ", summary).strip()
                
                # arXiv ID
                id_text = entry.findtext("{http://www.w3.org/2005/Atom}id", "")
                arxiv_id = id_text.split("/")[-1] if id_text else ""
                
                # 作者
                authors = []
                for author in entry.findall(".//{http://www.w3.org/2005/Atom}author"):
                    name = author.findtext("{http://www.w3.org/2005/Atom}name")
                    if name:
                        authors.append(name)
                
                # 发布日期
                published = entry.findtext("{http://www.w3.org/2005/Atom}published", "")
                year = int(published[:4]) if published else None
                
                # 分类
                categories = []
                for cat in entry.findall(".//{http://www.w3.org/2005/Atom}category"):
                    term = cat.get("term")
                    if term:
                        categories.append(term)
                
                # URL
                url = f"https://arxiv.org/abs/{arxiv_id}"
                
                papers.append(Paper(
                    source="arxiv",
                    paper_id=f"arXiv:{arxiv_id}",
                    title=title,
                    authors=authors,
                    abstract=summary,
                    year=year,
                    url=url,
                    categories=categories,
                ))
            
            return papers
            
        except Exception as e:
            print(f"arXiv 检索错误: {e}", file=sys.stderr)
            return []
    
    def _search_semantic_scholar(self, query: str, n: int) -> list[Paper]:
        """Semantic Scholar 检索"""
        headers = {}
        if self.api_keys.get("semantic_scholar"):
            headers["x-api-key"] = self.api_keys["semantic_scholar"]
        
        params = {
            "query": query,
            "limit": n,
            "fields": "title,authors,abstract,year,venue,doi,citationCount,citationCount",
        }
        
        try:
            resp = requests.get(
                API_CONFIG["semantic_scholar"]["base_url"],
                params=params,
                headers=headers,
                timeout=API_CONFIG["semantic_scholar"]["timeout"]
            )
            resp.raise_for_status()
            
            data = resp.json()
            papers = []
            
            for item in data.get("data", []):
                # DOI
                doi = item.get("doi", "")
                paper_id = doi if doi else item.get("paperId", "")
                
                # 作者
                authors = []
                for author in item.get("authors", []):
                    name = author.get("name")
                    if name:
                        authors.append(name)
                
                # 年份
                year = item.get("year")
                
                # 引用数
                citations = item.get("citationCount", 0)
                
                # URL
                url = doi or f"https://www.semanticscholar.org/paper/{item.get('paperId', '')}"
                
                papers.append(Paper(
                    source="semantic_scholar",
                    paper_id=paper_id,
                    title=item.get("title", ""),
                    authors=authors,
                    abstract=item.get("abstract", ""),
                    year=year,
                    venue=item.get("venue", ""),
                    doi=doi,
                    url=url,
                    citations=citations,
                ))
            
            return papers
            
        except requests.exceptions.HTTPError as e:
            print(f"Semantic Scholar API 错误 (可能是 Rate Limit): {e}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"Semantic Scholar 检索错误: {e}", file=sys.stderr)
            return []
    
    def _search_openalex(self, query: str, n: int) -> list[Paper]:
        """OpenAlex 检索"""
        params = {
            "search": query,
            "per_page": n,
            "select": "id,title,authors,abstract,publication_year,primary_location",
        }
        
        try:
            resp = requests.get(
                API_CONFIG["openalex"]["base_url"],
                params=params,
                timeout=API_CONFIG["openalex"]["timeout"]
            )
            resp.raise_for_status()
            
            data = resp.json()
            papers = []
            
            for item in data.get("results", []):
                # ID
                doi = ""
                paper_id = ""
                if item.get("doi"):
                    doi = item["doi"]
                    paper_id = doi
                
                # 作者
                authors = []
                for author in item.get("authorships", []):
                    author_name = author.get("author", {}).get("display_name")
                    if author_name:
                        authors.append(author_name)
                
                # 年份
                year = item.get("publication_year")
                
                # 摘要
                abstract = item.get("abstract") or ""
                
                # 发表场所
                venue = ""
                primary_location = item.get("primary_location", {})
                if primary_location:
                    venue = primary_location.get("source", {}).get("display_name", "")
                
                # URL
                url = doi or item.get("id", "")
                
                papers.append(Paper(
                    source="openalex",
                    paper_id=paper_id,
                    title=item.get("title", ""),
                    authors=authors,
                    abstract=abstract,
                    year=year,
                    venue=venue,
                    doi=doi,
                    url=url,
                ))
            
            return papers
            
        except Exception as e:
            print(f"OpenAlex 检索错误: {e}", file=sys.stderr)
            return []
    
    def _search_crossref(self, query: str, n: int) -> list[Paper]:
        """CrossRef 检索"""
        params = {
            "query": query,
            "rows": n,
            "select": "DOI,title,author,abstract,published,container-title",
        }
        
        # 添加礼貌头
        headers = {"User-Agent": "LiteratureSearcher/1.0 (mailto:your@email.com)"}
        
        try:
            resp = requests.get(
                API_CONFIG["crossref"]["base_url"],
                params=params,
                headers=headers,
                timeout=API_CONFIG["crossref"]["timeout"]
            )
            resp.raise_for_status()
            
            data = resp.json()
            papers = []
            
            for item in data.get("message", {}).get("items", []):
                doi = item.get("DOI", "")
                
                # 作者
                authors = []
                for author in item.get("author", []):
                    given = author.get("given", "")
                    family = author.get("family", "")
                    if family:
                        authors.append(f"{given} {family}".strip())
                
                # 年份
                year = None
                published = item.get("published") or item.get("published-print") or {}
                if published:
                    date_parts = published.get("date-parts", [[]])
                    if date_parts and date_parts[0]:
                        year = date_parts[0][0]
                
                # 发表场所
                venue = ""
                container = item.get("container-title", [])
                if container:
                    venue = container[0]
                
                papers.append(Paper(
                    source="crossref",
                    paper_id=doi,
                    title=item.get("title", [""])[0],
                    authors=authors,
                    abstract=item.get("abstract", ""),
                    year=year,
                    venue=venue,
                    doi=doi,
                    url=f"https://doi.org/{doi}" if doi else "",
                ))
            
            return papers
            
        except Exception as e:
            print(f"CrossRef 检索错误: {e}", file=sys.stderr)
            return []
    
    def _search_pubmed(self, query: str, n: int) -> list[Paper]:
        """PubMed 检索"""
        base_url = API_CONFIG["pubmed"]["base_url"]
        
        # 搜索
        search_url = f"{base_url}/esearch.fcgi"
        search_params = {
            "db": "pubmed",
            "term": query,
            "retmax": n,
            "retmode": "json",
            "sort": "relevance",
        }
        
        try:
            resp = requests.get(search_url, params=search_params, timeout=30)
            resp.raise_for_status()
            search_data = resp.json()
            
            id_list = search_data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                return []
            
            # 详情
            summary_url = f"{base_url}/esummary.fcgi"
            summary_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "json",
            }
            
            resp = requests.get(summary_url, params=summary_params, timeout=30)
            resp.raise_for_status()
            summary_data = resp.json()
            
            papers = []
            for uid, item in summary_data.get("result", {}).items():
                if uid == "uids":
                    continue
                
                # 年份
                pubdate = item.get("pubdate", "")
                year = int(pubdate[:4]) if pubdate else None
                
                # 作者
                authors = []
                for author in item.get("authors", []):
                    name = author.get("name")
                    if name:
                        authors.append(name)
                
                papers.append(Paper(
                    source="pubmed",
                    paper_id=f"PMID:{uid}",
                    title=item.get("title", ""),
                    authors=authors,
                    abstract=item.get("pubmed_abstract", ""),
                    year=year,
                    venue=item.get("source", ""),
                    url=f"https://pubmed.ncbi.nlm.nih.gov/{uid}/",
                ))
            
            return papers
            
        except Exception as e:
            print(f"PubMed 检索错误: {e}", file=sys.stderr)
            return []
    
    def _deduplicate(self, papers: list[Paper]) -> list[Paper]:
        """去重"""
        seen = {}
        unique = []
        
        for paper in papers:
            key = None
            
            # 按 DOI 去重
            if paper.doi:
                key = paper.doi.lower()
            # 或按标题近似匹配
            elif paper.title:
                key = paper.title.lower()[:50]
            
            if key and key not in seen:
                seen[key] = True
                unique.append(paper)
        
        return unique


# ============== 验证模块 ==============
class CitationValidator:
    """引文验证器"""
    
    @staticmethod
    def validate_doi(doi: str) -> dict:
        """验证 DOI"""
        result = {
            "doi": doi,
            "valid": False,
            "url": "",
            "error": None,
        }
        
        # 格式检查
        doi_pattern = r"^10\.\d{4,}/[^\s]+$"
        if not re.match(doi_pattern, doi):
            result["error"] = "Invalid DOI format"
            return result
        
        # HEAD 请求
        url = f"https://doi.org/{doi}"
        try:
            resp = requests.head(url, timeout=10, allow_redirects=True)
            if resp.status_code < 400:
                result["valid"] = True
                result["url"] = url
            else:
                result["error"] = f"HTTP {resp.status_code}"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def validate_arxiv(arxiv_id: str) -> dict:
        """验证 arXiv ID"""
        result = {
            "arxiv_id": arxiv_id,
            "valid": False,
            "url": "",
            "error": None,
        }
        
        # 格式检查
        arxiv_pattern = r"^\d{4}\.\d{4,5}(v\d+)?$"
        if not re.match(arxiv_pattern, arxiv_id):
            result["error"] = "Invalid arXiv ID format"
            return result
        
        url = f"https://arxiv.org/abs/{arxiv_id}"
        try:
            resp = requests.head(url, timeout=10)
            if resp.status_code < 400:
                result["valid"] = True
                result["url"] = url
            else:
                result["error"] = f"HTTP {resp.status_code}"
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    @staticmethod
    def validate_paper(paper: Paper) -> dict:
        """验证单篇论文"""
        if paper.paper_id.startswith("arXiv:"):
            arxiv_id = paper.paper_id.replace("arXiv:", "")
            return CitationValidator.validate_arxiv(arxiv_id)
        elif paper.doi:
            return CitationValidator.validate_doi(paper.doi)
        else:
            return {"valid": None, "error": "No DOI or arXiv ID"}


# ============== 格式化模块 ==============
class CitationFormatter:
    """引文格式化"""
    
    @staticmethod
    def format_apa(paper: Paper) -> str:
        """APA 格式"""
        # 作者
        authors = paper.authors
        if len(authors) > 7:
            authors_str = ", ".join(authors[:7]) + ", ..."
        elif authors:
            authors_str = ", ".join(authors)
        else:
            authors_str = "Unknown"
        
        # 年份
        year = paper.year or "n.d."
        
        # 标题
        title = paper.title
        
        # 来源
        source = paper.venue or ""
        
        # 构建引用
        if paper.doi:
            citation = f"{authors_str} ({year}). {title}. {source}. https://doi.org/{paper.doi}"
        elif paper.paper_id.startswith("arXiv:"):
            arxiv_id = paper.paper_id.replace("arXiv:", "")
            citation = f"{authors_str} ({year}). {title}. arXiv:{arxiv_id} [arXiv]"
        elif source:
            citation = f"{authors_str} ({year}). {title}. {source}."
        else:
            citation = f"{authors_str} ({year}). {title}."
        
        return citation
    
    @staticmethod
    def format_mla(paper: Paper) -> str:
        """MLA 格式"""
        authors = ", ".join(paper.authors) if paper.authors else "Unknown"
        year = paper.year or "n.d."
        
        title = f'"{paper.title}."' if paper.title else ""
        source = paper.venue or ""
        
        if paper.doi:
            return f'{authors}. {year}. {title} {source}, doi:{paper.doi}.'
        else:
            return f'{authors}. {year}. {title} {source}.'
    
    @staticmethod
    def format_ieee(paper: Paper) -> str:
        """IEEE 格式"""
        authors = ", ".join(paper.authors) if paper.authors else "Unknown"
        year = paper.year or "n.d."
        
        title = paper.title
        source = paper.venue or ""
        
        if paper.doi:
            return f'{authors}, "{title}," {source}, {year}, doi:{paper.doi}.'
        else:
            return f'{authors}, "{title}," {source}, {year}.'
    
    @staticmethod
    def format_bibtex(paper: Paper) -> str:
        """BibTeX 格式"""
        # 生成 key
        first_author = paper.authors[0].split()[-1].lower() if paper.authors else "unknown"
        year = str(paper.year) if paper.year else "nd"
        key = f"{first_author}{year}"
        
        entry_type = "misc"
        if paper.paper_id.startswith("arXiv:"):
            entry_type = "article"
        elif paper.venue:
            entry_type = "inproceedings"
        
        lines = [f"@article{{{key},"]
        lines.append(f'  author = {{{" and ".join(paper.authors)}}},')
        lines.append(f'  title = {{{paper.title}}},')
        
        if paper.year:
            lines.append(f'  year = {{{paper.year}}},')
        if paper.venue:
            lines.append(f'  journal = {{{paper.venue}}},')
        if paper.doi:
            lines.append(f'  doi = {{{paper.doi}}},')
        if paper.url:
            lines.append(f'  url = {{{paper.url}}},')
        
        lines.append("}")
        
        return "\n".join(lines)
    
    @staticmethod
    def format_ris(paper: Paper) -> str:
        """RIS 格式"""
        lines = []
        
        # 根据来源判断类型
        if paper.source == "pubmed":
            lines.append("TY  - JOUR")
        elif paper.paper_id.startswith("arXiv:"):
            lines.append("TY  - EPRC")  # Electronic Preprint
        else:
            lines.append("TY  - JOUR")
        
        # 作者
        for author in paper.authors:
            lines.append(f"AU  - {author}")
        
        # 标题
        lines.append(f"TI  - {paper.title}")
        
        # 年份
        if paper.year:
            lines.append(f"PY  - {paper.year}")
            lines.append(f"Y1  - {paper.year}")
        
        # 发表场所
        if paper.venue:
            lines.append(f"JO  - {paper.venue}")
            lines.append(f"JF  - {paper.venue}")
        
        # DOI
        if paper.doi:
            lines.append(f"DO  - {paper.doi}")
        
        # URL
        if paper.url:
            lines.append(f"UR  - {paper.url}")
        
        # 摘要
        if paper.abstract:
            lines.append(f"AB  - {paper.abstract}")
        
        # 引用数
        if paper.citations:
            lines.append(f"NR  - {paper.citations}")
        
        # arXiv 特殊处理
        if paper.paper_id.startswith("arXiv:"):
            arxiv_id = paper.paper_id.replace("arXiv:", "")
            lines.append(f"M3  - arXiv:{arxiv_id}")
            lines.append("ER  - ")
        else:
            lines.append("ER  - ")
        
        return "\n".join(lines)

    @staticmethod
    def format_markdown(paper: Paper, index: int = None) -> str:
        """Markdown 格式"""
        idx = f"[{index}] " if index is not None else ""
        
        authors = ", ".join(paper.authors) if paper.authors else "Unknown"
        year = paper.year or "n.d."
        source_tag = paper.get_source_tag()
        
        lines = [
            f"{idx}**{paper.title}**",
            f"* {authors}. ({year}). {paper.venue or ''}*",
        ]
        
        if paper.doi:
            lines.append(f"DOI: [{paper.doi}](https://doi.org/{paper.doi}) {source_tag}")
        elif paper.paper_id.startswith("arXiv:"):
            arxiv_id = paper.paper_id.replace("arXiv:", "")
            lines.append(f"arXiv: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id}) [arXiv]")
        elif paper.url:
            lines.append(f"URL: [{paper.url}]({paper.url})")
        
        if paper.citations:
            lines.append(f"*Citations: {paper.citations}*")
        
        return "\n".join(lines)


# ============== 过滤模块 ==============
class PaperFilter:
    """论文过滤器"""
    
    @staticmethod
    def filter_by_source(papers: list[Paper], sources: list[str]) -> list[Paper]:
        """按来源过滤"""
        return [p for p in papers if p.source in sources]
    
    @staticmethod
    def filter_published_only(papers: list[Paper]) -> list[Paper]:
        """仅保留正式发表的论文"""
        return [p for p in papers if p.source != "arxiv"]
    
    @staticmethod
    def filter_preprint_only(papers: list[Paper]) -> list[Paper]:
        """仅保留预印本"""
        return [p for p in papers if p.source == "arxiv"]
    
    @staticmethod
    def filter_by_year(papers: list[Paper], min_year: int = None, max_year: int = None) -> list[Paper]:
        """按年份过滤"""
        result = papers
        if min_year:
            result = [p for p in result if p.year and p.year >= min_year]
        if max_year:
            result = [p for p in result if p.year and p.year <= max_year]
        return result
    
    @staticmethod
    def filter_by_citations(papers: list[Paper], min_citations: int = 0) -> list[Paper]:
        """按引用数过滤"""
        return [p for p in papers if p.citations and p.citations >= min_citations]


# ============== 冲突检测模块 ==============
class ConflictDetector:
    """跨源冲突检测器"""
    
    @staticmethod
    def detect_conflicts(papers: list[Paper]) -> list[dict]:
        """检测同一论文在不同源的数据冲突"""
        # 按 DOI 分组
        doi_groups = {}
        arxiv_groups = {}
        
        for paper in papers:
            if paper.doi:
                doi_groups.setdefault(paper.doi, []).append(paper)
            elif paper.paper_id.startswith("arXiv:"):
                arxiv_groups.setdefault(paper.paper_id, []).append(paper)
        
        conflicts = []
        
        # 检测同一个 DOI 的冲突
        for doi, group in doi_groups.items():
            if len(group) > 1:
                conflict = {
                    "type": "doi_conflict",
                    "id": doi,
                    "papers": [p.to_dict() for p in group],
                    "conflicts": ConflictDetector._compare_papers(group),
                }
                conflicts.append(conflict)
        
        # 检测同一个 arXiv ID 的冲突
        for arxiv_id, group in arxiv_groups.items():
            if len(group) > 1:
                conflict = {
                    "type": "arxiv_conflict",
                    "id": arxiv_id,
                    "papers": [p.to_dict() for p in group],
                    "conflicts": ConflictDetector._compare_papers(group),
                }
                conflicts.append(conflict)
        
        return conflicts
    
    
    @staticmethod
    def _compare_papers(papers: list[Paper]) -> list[str]:
        """比较论文元数据差异"""
        if len(papers) < 2:
            return []
        
        conflicts = []
        
        # 比较标题
        titles = set(p.title for p in papers if p.title)
        if len(titles) > 1:
            conflicts.append(f"Title mismatch: {titles}")
        
        # 比较年份
        years = set(str(p.year) for p in papers if p.year)
        if len(years) > 1:
            conflicts.append(f"Year mismatch: {years}")
        
        # 比较作者数量
        author_counts = set(len(p.authors) for p in papers)
        if len(author_counts) > 1:
            conflicts.append(f"Author count mismatch: {author_counts}")
        
        return conflicts
    
    @staticmethod
    def resolve_conflict(papers: list[Paper]) -> Paper:
        """解决冲突，选择最可靠的版本"""
        if len(papers) <= 1:
            return papers[0] if papers else None
        
        # 优先级：crossref > pubmed > semantic_scholar > openalex > arxiv
        source_priority = {"crossref": 5, "pubmed": 4, "semantic_scholar": 3, "openalex": 2, "arxiv": 1}
        
        # 选择优先级最高的
        papers.sort(key=lambda p: source_priority.get(p.source, 0), reverse=True)
        return papers[0]


# ============== 综述生成模块 ==============
class ReviewGenerator:
    """综述生成器"""
    
    @staticmethod
    def generate(papers: list[Paper], format: str = "markdown") -> str:
        """生成综述"""
        if not papers:
            return "No papers found."
        
        # 统计
        source_stats = {}
        year_stats = {}
        
        for paper in papers:
            # 来源统计
            tag = paper.get_source_tag()
            source_stats[tag] = source_stats.get(tag, 0) + 1
            
            # 年份统计
            if paper.year:
                year_stats[paper.year] = year_stats.get(paper.year, 0) + 1
        
        lines = ["# Literature Review\n"]
        
        # 来源统计
        lines.append("## Statistics")
        lines.append(f"- **Total Papers**: {len(papers)}")
        for tag, count in sorted(source_stats.items()):
            lines.append(f"- {tag}: {count}")
        lines.append("")
        
        # 时间线
        if year_stats:
            lines.append("## Timeline")
            for year in sorted(year_stats.keys(), reverse=True)[:10]:
                lines.append(f"- {year}: {year_stats[year]} papers")
            lines.append("")
        
        # 论文列表
        lines.append("## Papers")
        for i, paper in enumerate(papers, 1):
            lines.append(f"### {i}. {paper.title}")
            lines.append(f"**Authors**: {', '.join(paper.authors[:5])}")
            if paper.year:
                lines.append(f"**Year**: {paper.year}")
            if paper.venue:
                lines.append(f"**Venue**: {paper.venue}")
            if paper.citations:
                lines.append(f"**Citations**: {paper.citations}")
            
            if paper.doi:
                lines.append(f"**DOI**: [{paper.doi}](https://doi.org/{paper.doi})")
            elif paper.paper_id.startswith("arXiv:"):
                arxiv_id = paper.paper_id.replace("arXiv:", "")
                lines.append(f"**arXiv**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})")
            
            if paper.abstract:
                lines.append(f"\n**Abstract**: {paper.abstract[:300]}...")
            
            lines.append("")
        
        return "\n".join(lines)


# ============== 主程序 ==============
def parse_args():
    parser = argparse.ArgumentParser(
        description="Literature Search Tool - 文献检索工具"
    )
    
    parser.add_argument("query", help="搜索关键词或文件路径 (file://path)")
    parser.add_argument("-n", "--num", type=int, default=20, help="返回数量 (default: 20)")
    parser.add_argument("-s", "--sources", nargs="+", 
                      default=["semantic_scholar", "openalex"],
                      help="检索源")
    parser.add_argument("-f", "--format", choices=["apa", "mla", "ieee", "bibtex", "markdown", "ris"],
                      default="markdown", help="输出格式")
    parser.add_argument("--validate", action="store_true", help="验证 DOI")
    parser.add_argument("--published-only", action="store_true", help="仅保留正式发表的论文")
    parser.add_argument("--preprint-only", action="store_true", help="仅保留预印本")
    parser.add_argument("--min-year", type=int, help="最早年份")
    parser.add_argument("--max-year", type=int, help="最晚年份")
    parser.add_argument("--min-citations", type=int, default=0, help="最少引用数")
    parser.add_argument("--conflicts", action="store_true", help="检测跨源冲突")
    parser.add_argument("-o", "--output", help="输出文件")
    
    return parser.parse_args()


def load_papers_from_file(path: str) -> list[str]:
    """从文件加载论文ID"""
    # 去掉 file:// 前缀
    if path.startswith("file://"):
        path = path[7:]
    
    with open(path, "r") as f:
        lines = f.readlines()
    
    papers = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            papers.append(line)
    
    return papers


def main():
    args = parse_args()
    
    # 文件模式
    if args.query.startswith("file://"):
        paper_ids = load_papers_from_file(args.query)
        print(f"Loaded {len(paper_ids)} paper IDs from file")
        # TODO: 通过 ID 获取论文详情
        return
    
    # 检索
    print(f"Searching: {args.query}", file=sys.stderr)
    print(f"Sources: {', '.join(args.sources)}", file=sys.stderr)
    
    searcher = LiteratureSearcher(sources=args.sources, api_keys=API_KEYS)
    papers = searcher.search(args.query, args.num)
    
    print(f"Found {len(papers)} papers\n", file=sys.stderr)
    
    # 过滤
    if args.published_only:
        papers = PaperFilter.filter_published_only(papers)
        print(f"After published-only filter: {len(papers)} papers", file=sys.stderr)
    if args.preprint_only:
        papers = PaperFilter.filter_preprint_only(papers)
        print(f"After preprint-only filter: {len(papers)} papers", file=sys.stderr)
    if args.min_year:
        papers = PaperFilter.filter_by_year(papers, min_year=args.min_year)
        print(f"After min-year filter: {len(papers)} papers", file=sys.stderr)
    if args.max_year:
        papers = PaperFilter.filter_by_year(papers, max_year=args.max_year)
        print(f"After max-year filter: {len(papers)} papers", file=sys.stderr)
    if args.min_citations > 0:
        papers = PaperFilter.filter_by_citations(papers, min_citations=args.min_citations)
        print(f"After min-citations filter: {len(papers)} papers", file=sys.stderr)
    
    # 冲突检测
    if args.conflicts:
        conflicts = ConflictDetector.detect_conflicts(papers)
        print(f"\nFound {len(conflicts)} conflicts:", file=sys.stderr)
        for c in conflicts:
            print(f"  - {c['type']}: {c['id']}", file=sys.stderr)
            for detail in c['conflicts']:
                print(f"    {detail}", file=sys.stderr)
        return
    
    # 验证
    if args.validate:
        print("Validating papers...")
        for paper in papers:
            result = CitationValidator.validate_paper(paper)
            status = "✓" if result.get("valid") else "✗"
            print(f"{status} {paper.paper_id}: {result.get('error', 'OK')}")
        return
    
    # 格式化输出
    formatter = CitationFormatter()
    
    if args.format == "apa":
        output = "\n\n".join([formatter.format_apa(p) for p in papers])
    elif args.format == "mla":
        output = "\n\n".join([formatter.format_mla(p) for p in papers])
    elif args.format == "ieee":
        output = "\n\n".join([formatter.format_ieee(p) for p in papers])
    elif args.format == "bibtex":
        output = "\n\n".join([formatter.format_bibtex(p) for p in papers])
    elif args.format == "markdown":
        output = "\n\n".join([formatter.format_markdown(p, i+1) for i, p in enumerate(papers)])
    elif args.format == "ris":
        output = "\n\n".join([formatter.format_ris(p) for p in papers])
    else:
        output = ReviewGenerator.generate(papers)
    
    # 输出
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Output saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()