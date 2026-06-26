#!/usr/bin/env python3
"""
PubMed Search Script
使用NCBI E-Utilities API搜索PubMed文献
"""

import requests
import xml.etree.ElementTree as ET
import json
import time
from typing import List, Dict, Optional

class PubMedSearcher:
    """PubMed搜索器"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: Optional[str] = None, email: str = "anonymous@example.org"):
        """
        初始化搜索器
        
        Args:
            api_key: NCBI API key（可选，用于提高速率限制）
            email: 用于"Polite Pool"的邮箱
        """
        self.api_key = api_key
        self.email = email
        self.rate_limit = 10 if api_key else 3  # 每秒请求数
        self.last_request_time = 0
    
    def _rate_limit_wait(self):
        """等待速率限制"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 1.0 / self.rate_limit
        
        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def search(self, query: str, limit: int = 10, sort: str = "relevance") -> Dict:
        """
        搜索PubMed文献
        
        Args:
            query: 搜索查询
            limit: 返回结果数量
            sort: 排序方式（relevance/date）
        
        Returns:
            搜索结果字典
        """
        self._rate_limit_wait()
        
        url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": limit,
            "retmode": "json",
            "sort": sort,
            "tool": "openclaw-pubmed-skill",
            "email": self.email
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def fetch_details(self, pmid: str) -> Dict:
        """
        获取文献详情
        
        Args:
            pmid: PubMed ID
        
        Returns:
            文献详情字典
        """
        self._rate_limit_wait()
        
        url = f"{self.BASE_URL}/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": pmid,
            "retmode": "xml",
            "tool": "openclaw-pubmed-skill",
            "email": self.email
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return self._parse_xml(response.text)
        except requests.RequestException as e:
            return {"error": str(e)}
    
    def fetch_batch(self, pmids: List[str]) -> List[Dict]:
        """
        批量获取文献详情
        
        Args:
            pmids: PubMed ID列表
        
        Returns:
            文献详情列表
        """
        results = []
        for pmid in pmids:
            details = self.fetch_details(pmid)
            if "error" not in details:
                results.append(details)
        return results
    
    def _parse_xml(self, xml_text: str) -> Dict:
        """解析PubMed XML响应"""
        try:
            root = ET.fromstring(xml_text)
            article = root.find('.//PubmedArticle')
            
            if article is None:
                return {"error": "No article found"}
            
            # 提取标题
            title_elem = article.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else "N/A"
            
            # 提取摘要
            abstract_elem = article.find('.//Abstract/AbstractText')
            abstract = abstract_elem.text if abstract_elem is not None else "No abstract available"
            
            # 提取作者
            authors = []
            for author in article.findall('.//Author'):
                last_name = author.find('LastName')
                first_name = author.find('ForeName')
                if last_name is not None:
                    name = f"{last_name.text}"
                    if first_name is not None:
                        name = f"{last_name.text}, {first_name.text}"
                    authors.append(name)
            
            # 提取期刊
            journal_elem = article.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else "N/A"
            
            # 提取年份
            year_elem = article.find('.//PubDate/Year')
            year = year_elem.text if year_elem is not None else "N/A"
            
            # 提取DOI
            doi_elem = article.find('.//ArticleId[@IdType="doi"]')
            doi = doi_elem.text if doi_elem is not None else "N/A"
            
            # 提取PMID
            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else "N/A"
            
            return {
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "authors": authors,
                "journal": journal,
                "year": year,
                "doi": doi
            }
        except ET.ParseError as e:
            return {"error": f"XML parse error: {e}"}
    
    def format_citation(self, article: Dict, style: str = "apa") -> str:
        """
        格式化引用
        
        Args:
            article: 文章信息字典
            style: 引用格式（apa/mla/ieee/gbt7714）
        
        Returns:
            格式化引用字符串
        """
        authors = article.get("authors", [])
        title = article.get("title", "N/A")
        journal = article.get("journal", "N/A")
        year = article.get("year", "N/A")
        doi = article.get("doi", "N/A")
        
        # 格式化作者
        if len(authors) > 1:
            author_str = f"{authors[0]} et al."
        elif len(authors) == 1:
            author_str = authors[0]
        else:
            author_str = "Unknown"
        
        if style.lower() == "apa":
            return f"{author_str} ({year}). {title}. *{journal}*. https://doi.org/{doi}"
        elif style.lower() == "mla":
            return f"{author_str}. \"{title}.\" *{journal}* ({year})."
        elif style.lower() == "ieee":
            return f"{author_str}, \"{title},\" *{journal}*, {year}."
        elif style.lower() == "gbt7714":
            return f"{author_str}. {title}[J]. {journal}, {year}. DOI: {doi}"
        else:
            return f"{author_str}. {title}. {journal}, {year}."


def main():
    """主函数"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pubmed_search.py <query> [limit] [style]")
        print("Example: python pubmed_search.py 'machine learning' 5 apa")
        sys.exit(1)
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    style = sys.argv[3] if len(sys.argv) > 3 else "apa"
    
    # 创建搜索器
    searcher = PubMedSearcher()
    
    print(f"🔍 Searching PubMed for: {query}")
    print(f"📊 Limit: {limit} results")
    print("-" * 60)
    
    # 搜索
    search_results = searcher.search(query, limit)
    
    if "error" in search_results:
        print(f"❌ Error: {search_results['error']}")
        sys.exit(1)
    
    # 获取PMID列表
    idlist = search_results.get("esearchresult", {}).get("idlist", [])
    
    if not idlist:
        print("❌ No results found")
        sys.exit(0)
    
    print(f"✅ Found {len(idlist)} results")
    
    # 获取详情
    articles = searcher.fetch_batch(idlist)
    
    for i, article in enumerate(articles, 1):
        print(f"\n📄 Result {i}:")
        print(f"  PMID: {article.get('pmid')}")
        print(f"  Title: {article.get('title')}")
        print(f"  Authors: {', '.join(article.get('authors', []))}")
        print(f"  Journal: {article.get('journal')} ({article.get('year')})")
        print(f"  DOI: {article.get('doi')}")
        
        citation = searcher.format_citation(article, style)
        print(f"  Citation ({style}): {citation}")
        
        # 显示摘要（前100字符）
        abstract = article.get('abstract', '')
        if abstract:
            print(f"  Abstract preview: {abstract[:100]}...")
    
    print("-" * 60)
    print(f"📚 Total results: {len(articles)}")


if __name__ == "__main__":
    main()