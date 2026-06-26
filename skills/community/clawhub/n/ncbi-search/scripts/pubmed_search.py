#!/usr/bin/env python3
"""
PubMed Search via NCBI E-Utilities API

Intelligent PubMed search with natural language query conversion.

Usage:
    python pubmed_search.py "your query" [options]

Features:
    - Automatic natural language to PubMed query conversion
    - MeSH term recognition and expansion
    - Smart field mapping (Title/Abstract, Author, Journal)
    - Date filtering
    - Article type filtering
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple

# Ensure we can import ncbi_utils from scripts directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from ncbi_utils import http_get, clean_xml_tags
except ImportError:
    print("Error: Could not import ncbi_utils.py from the scripts directory.", file=sys.stderr)
    sys.exit(1)

# NCBI E-Utilities Base URLs
EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ESEARCH_URL = f"{EUTILS_BASE}/esearch.fcgi"
EFETCH_URL = f"{EUTILS_BASE}/efetch.fcgi"

# Known MeSH terms for common medical concepts
MESH_TERMS = {
    # Diseases
    "alzheimer": "Alzheimer Disease",
    "alzheimer's": "Alzheimer Disease",
    "alzheimer disease": "Alzheimer Disease",
    "dementia": "Dementia",
    "parkinson": "Parkinson Disease",
    "parkinson's": "Parkinson Disease",
    "stroke": "Stroke",
    "cerebrovascular": "Cerebrovascular Disorders",
    "diabetes": "Diabetes Mellitus",
    "cancer": "Neoplasms",
    "tumor": "Neoplasms",
    "hypertension": "Hypertension",
    "depression": "Depression",
    "schizophrenia": "Schizophrenia",
    "autism": "Autistic Disorder",
    "epilepsy": "Epilepsy",
    "multiple sclerosis": "Multiple Sclerosis",
    
    # Anatomy
    "brain": "Brain",
    "heart": "Heart",
    "liver": "Liver",
    "kidney": "Kidney",
    "blood": "Blood",
    
    # Systems
    "nervous system": "Nervous System",
    "cardiovascular": "Cardiovascular System",
    "immune": "Immune System",
    
    # Concepts
    "neuroinflammation": "Neuroinflammation",
    "amyloid": "Amyloid",
    "tau": "Tau Proteins",
    
    # Processes
    "apoptosis": "Apoptosis",
    "autophagy": "Autophagy",
    "angiogenesis": "Angiogenesis",
}

# Gene symbols (common ones)
GENE_SYMBOLS = [
    "APOE", "APP", "PSEN1", "PSEN2", "TREM2", "MAPT", "SNCA", "TARDBP",
    "BRCA1", "BRCA2", "TP53", "EGFR", "KRAS", "MYC", "PTEN", "VEGF",
    "IL6", "TNF", "IFNG", "IL1B", "IL10", "TGFB1",
    "BDNF", "NGF", "GDNF", "NTF3",
]

# Stop words to exclude from query
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "must", "shall", "can", "need",
    "this", "that", "these", "those", "about", "after", "before", "during",
    "between", "into", "through", "during", "above", "below", "up", "down",
    "out", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "each", "few",
    "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "just", "also", "now",
}


def get_api_key(args: argparse.Namespace) -> Optional[str]:
    """Get NCBI API key from args or environment."""
    if args.api_key:
        return args.api_key
    return os.environ.get("NCBI_API_KEY")


def detect_query_elements(query: str) -> Dict[str, Any]:
    """
    Detect and categorize elements in natural language query.
    
    Returns:
        Dict with 'terms', 'genes', 'mesh', 'authors', 'journal', 'year'
    """
    query_lower = query.lower()
    elements = {
        "terms": [],
        "genes": [],
        "mesh": [],
        "authors": [],
        "journal": None,
        "year": None,
        "year_range": None,
        "article_type": None,
    }
    
    # Split into words
    words = re.findall(r'\b\w+\b', query)
    
    # Detect genes (uppercase or known symbols)
    for word in words:
        word_upper = word.upper()
        if word_upper in GENE_SYMBOLS:
            elements["genes"].append(word_upper)
        elif word.lower() not in STOP_WORDS and len(word) > 1:
            # Check if it's a MeSH term
            word_lower = word.lower()
            if word_lower in MESH_TERMS:
                elements["mesh"].append(MESH_TERMS[word_lower])
            elements["terms"].append(word)
    
    # Detect year patterns
    year_match = re.search(r'\b(19|20)\d{2}\b', query)
    if year_match:
        elements["year"] = int(year_match.group())
    
    # Detect "last N years" pattern
    last_years_match = re.search(r'last\s+(\d+)\s+years?', query_lower)
    if last_years_match:
        elements["year_range"] = int(last_years_match.group(1))
    
    # Detect article types
    type_patterns = {
        "review": ["review", "reviews"],
        "clinical_trial": ["clinical trial", "clinical trials", "trial"],
        "randomized": ["randomized", "rct"],
        "meta_analysis": ["meta-analysis", "meta analysis", "metaanalysis"],
        "case_report": ["case report", "case study"],
    }
    for atype, patterns in type_patterns.items():
        for pattern in patterns:
            if pattern in query_lower:
                elements["article_type"] = atype
                break
        if elements["article_type"]:
            break
    
    # Detect author pattern (Name followed by initial or just last name)
    author_match = re.search(r'\b([A-Z][a-z]+)\s+([A-Z](?:\s|$|,))', query)
    if author_match:
        elements["authors"].append(f"{author_match.group(1)} {author_match.group(2).strip()}")
    
    return elements


def build_pubmed_query(
    query: str,
    elements: Dict[str, Any],
    years: Optional[int] = None,
    article_type: Optional[str] = None,
    mesh_filter: Optional[str] = None
) -> Tuple[str, str]:
    """
    Build PubMed query from natural language and detected elements.
    
    Returns:
        Tuple of (pubmed_query, explanation)
    """
    query_parts = []
    explanation_parts = []
    
    # If query already has PubMed syntax, use it
    if any(tag in query for tag in ["[", " AND ", " OR ", " NOT "]):
        return query, "使用用户提供的 PubMed 检索式"
    
    # Process detected elements
    
    # 1. Genes - search in Title/Abstract
    for gene in elements.get("genes", []):
        query_parts.append(f'{gene}[Title/Abstract]')
        explanation_parts.append(f'Gene "{gene}" in title/abstract')
    
    # 2. MeSH terms
    for mesh in elements.get("mesh", []):
        query_parts.append(f'"{mesh}"[MeSH]')
        explanation_parts.append(f'MeSH term "{mesh}"')
    
    # 3. Other terms - Title/Abstract
    processed_terms = set()
    for term in elements.get("terms", []):
        term_lower = term.lower()
        # Skip if already processed as gene or mesh
        if term.upper() in elements.get("genes", []):
            continue
        if term_lower in [m.lower() for m in MESH_TERMS.keys()]:
            continue
        if term_lower in STOP_WORDS:
            continue
        if term_lower in processed_terms:
            continue
        processed_terms.add(term_lower)
        query_parts.append(f'{term}[Title/Abstract]')
    
    # 4. Authors
    for author in elements.get("authors", []):
        query_parts.append(f'{author}[Author]')
        explanation_parts.append(f'Author "{author}"')
    
    # 5. Article type
    atype = article_type or elements.get("article_type")
    if atype:
        type_map = {
            "review": "Review[pt]",
            "clinical_trial": "Clinical Trial[pt]",
            "randomized": "Randomized Controlled Trial[pt]",
            "meta_analysis": "Meta-Analysis[pt]",
            "case_report": "Case Reports[pt]",
        }
        if atype in type_map:
            query_parts.append(type_map[atype])
            explanation_parts.append(f'Article type: {atype.replace("_", " ").title()}')
    
    # 6. Date range
    year_range = years or elements.get("year_range")
    if year_range:
        end = datetime.now()
        start = end - timedelta(days=year_range * 365)
        date_filter = f"{start.strftime('%Y/%m/%d')}:{end.strftime('%Y/%m/%d')}[PDat]"
        query_parts.append(date_filter)
        explanation_parts.append(f'Last {year_range} years')
    
    # 7. Additional MeSH filter
    if mesh_filter:
        query_parts.append(f'"{mesh_filter}"[MeSH]')
        explanation_parts.append(f'MeSH filter: "{mesh_filter}"')
    
    # Combine with AND
    if not query_parts:
        # Fallback: search each word
        words = [w for w in query.split() if w.lower() not in STOP_WORDS and len(w) > 1]
        query_parts = [f'{w}[Title/Abstract]' for w in words[:5]]  # Limit to 5 terms
    
    pubmed_query = " AND ".join(query_parts)
    explanation = " -> ".join(explanation_parts) if explanation_parts else "Keywords in title/abstract"
    
    return pubmed_query, explanation


def search_pubmed(
    query: str,
    max_results: int = 10,
    api_key: Optional[str] = None,
    verbose: bool = False
) -> Dict[str, Any]:
    """Search PubMed and return PMIDs using shared http_get utility."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    }
    
    if api_key:
        params["api_key"] = api_key
        
    response_text = http_get(ESEARCH_URL, params=params, api_key=api_key, timeout=30, verbose=verbose)
    data = json.loads(response_text)
    result = data.get("esearchresult", {})
    
    return {
        "count": int(result.get("count", 0)),
        "ids": result.get("idlist", []),
    }


def fetch_articles(
    pmids: List[str],
    api_key: Optional[str] = None,
    verbose: bool = False
) -> List[Dict[str, Any]]:
    """Fetch article details by PMID using shared http_get utility."""
    if not pmids:
        return []
        
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "rettype": "xml",
        "retmode": "xml"
    }
    
    if api_key:
        params["api_key"] = api_key
        
    response_text = http_get(EFETCH_URL, params=params, api_key=api_key, timeout=60, verbose=verbose)
    return parse_pubmed_xml(response_text)


def parse_pubmed_xml(xml_text: str) -> List[Dict[str, Any]]:
    """Parse PubMed XML response into structured data."""
    articles = []
    
    article_pattern = r'<PubmedArticle>(.*?)</PubmedArticle>'
    article_matches = re.findall(article_pattern, xml_text, re.DOTALL)
    
    for article_xml in article_matches:
        article = {}
        
        # PMID
        pmid_match = re.search(r'<PMID[^>]*>(\d+)</PMID>', article_xml)
        if pmid_match:
            article["pmid"] = pmid_match.group(1)
        
        # Title
        title_match = re.search(r'<ArticleTitle[^>]*>(.*?)</ArticleTitle>', article_xml, re.DOTALL)
        if title_match:
            article["title"] = clean_xml_tags(title_match.group(1))
        
        # Authors
        authors = []
        author_pattern = r'<Author[^>]*>.*?<LastName>([^<]+)</LastName>.*?<ForeName>([^<]+)</ForeName>.*?</Author>'
        for author_match in re.finditer(author_pattern, article_xml, re.DOTALL):
            last_name = author_match.group(1)
            fore_name = author_match.group(2)
            authors.append(f"{last_name} {fore_name[0] if fore_name else ''}")
        article["authors"] = authors
        
        # Journal
        journal_match = re.search(r'<Journal[^>]*>.*?<Title>([^<]+)</Title>', article_xml, re.DOTALL)
        if journal_match:
            article["journal"] = journal_match.group(1)
        
        # Publication Year
        year_match = re.search(r'<PubDate[^>]*>.*?<Year>(\d{4})</Year>', article_xml, re.DOTALL)
        if year_match:
            article["year"] = year_match.group(1)
        else:
            # Try MedlineDate
            medline_match = re.search(r'<MedlineDate>(\d{4})', article_xml)
            if medline_match:
                article["year"] = medline_match.group(1)
        
        # Abstract
        abstract_parts = []
        abstract_pattern = r'<AbstractText[^>]*>(.*?)</AbstractText>'
        for abstract_match in re.finditer(abstract_pattern, article_xml, re.DOTALL):
            abstract_parts.append(clean_xml_tags(abstract_match.group(1)))
        if abstract_parts:
            article["abstract"] = " ".join(abstract_parts)
        
        # DOI
        doi_match = re.search(r'<ArticleId IdType="doi">([^<]+)</ArticleId>', article_xml)
        if doi_match:
            article["doi"] = doi_match.group(1)
        
        # MeSH Terms
        mesh_terms = []
        mesh_pattern = r'<DescriptorName[^>]*>([^<]+)</DescriptorName>'
        for mesh_match in re.finditer(mesh_pattern, article_xml):
            mesh_terms.append(mesh_match.group(1))
        if mesh_terms:
            article["mesh_terms"] = list(dict.fromkeys(mesh_terms))  # Remove duplicates, preserve order
        
        # URL
        if article.get("pmid"):
            article["url"] = f"https://pubmed.ncbi.nlm.nih.gov/{article['pmid']}/"
        
        if article.get("pmid"):
            articles.append(article)
    
    return articles


def format_output(
    articles: List[Dict[str, Any]],
    total_count: int,
    query: str,
    explanation: str,
    format: str = "summary"
) -> str:
    """Format output for display."""
    
    if format == "json":
        output = {
            "pubmed_query": query,
            "query_explanation": explanation,
            "total_results": total_count,
            "returned": len(articles),
            "search_date": datetime.now().isoformat(),
            "articles": articles
        }
        return json.dumps(output, indent=2, ensure_ascii=False)
    
    # Summary format (default)
    lines = []
    lines.append("=" * 70)
    lines.append("PubMed Search Results")
    lines.append("=" * 70)
    lines.append(f"Query: {query}")
    lines.append(f"Parsed: {explanation}")
    lines.append(f"Total: {total_count} articles")
    lines.append(f"Returned: {len(articles)} articles")
    lines.append("=" * 70)
    
    for i, article in enumerate(articles, 1):
        lines.append(f"\n[{i}] PMID: {article.get('pmid', 'N/A')}")
        lines.append(f"Title: {article.get('title', 'N/A')}")
        
        authors = article.get("authors", [])
        if authors:
            author_str = ", ".join(authors[:5])
            if len(authors) > 5:
                author_str += f" et al. ({len(authors)} authors)"
            lines.append(f"Authors: {author_str}")
        
        journal = article.get("journal", "N/A")
        year = article.get("year", "N/A")
        lines.append(f"Journal: {journal} ({year})")
        
        if article.get("doi"):
            lines.append(f"DOI: {article['doi']}")
        
        if article.get("mesh_terms"):
            mesh_str = ", ".join(article["mesh_terms"][:3])
            if len(article["mesh_terms"]) > 3:
                mesh_str += " ..."
            lines.append(f"MeSH: {mesh_str}")
        
        if article.get("abstract"):
            abstract = article["abstract"]
            preview = abstract[:200] + "..." if len(abstract) > 200 else abstract
            lines.append(f"Abstract: {preview}")
        
        lines.append(f"URL: {article.get('url', 'N/A')}")
        lines.append("-" * 70)
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="PubMed 智能检索 (NCBI E-Utilities)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    %(prog)s "Alzheimer disease cerebrovascular mechanisms"
    %(prog)s "APOE gene and Alzheimer disease" --years 5
    %(prog)s "Smith J author Alzheimer" --max 20
    %(prog)s "diabetes treatment review" --type review
        """
    )
    
    parser.add_argument("query", help="自然语言检索词或 PubMed 检索式")
    parser.add_argument("--max", type=int, default=10, help="最大返回结果数 (默认: 10)")
    parser.add_argument("--years", type=int, help="限制最近 N 年")
    parser.add_argument("--type", help="文章类型: review, clinical_trial, randomized, meta_analysis")
    parser.add_argument("--mesh", help="MeSH 主题词筛选")
    parser.add_argument("--format", choices=["json", "summary"], default="summary", help="输出格式")
    parser.add_argument("--output", "-o", help="保存到文件")
    parser.add_argument("--api-key", help="NCBI API key")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")
    
    args = parser.parse_args()
    
    api_key = get_api_key(args)
    
    # Detect query elements
    elements = detect_query_elements(args.query)
    
    if args.verbose:
        print(f"检测到的元素: {json.dumps(elements, ensure_ascii=False, indent=2)}", file=sys.stderr)
    
    # Build PubMed query
    pubmed_query, explanation = build_pubmed_query(
        args.query,
        elements,
        years=args.years,
        article_type=args.type,
        mesh_filter=args.mesh
    )
    
    if args.verbose:
        print(f"PubMed 检索式: {pubmed_query}", file=sys.stderr)
    
    # Search
    search_result = search_pubmed(pubmed_query, args.max, api_key, args.verbose)
    pmids = search_result["ids"]
    total = search_result["count"]
    
    if args.verbose:
        print(f"找到 {total} 篇文献, 获取 {len(pmids)} 篇...", file=sys.stderr)
    
    # Fetch articles
    articles = fetch_articles(pmids, api_key, args.verbose) if pmids else []
    
    # Format output
    output = format_output(articles, total, pubmed_query, explanation, args.format)
    
    # Print or save
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"已保存到 {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()