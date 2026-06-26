#!/usr/bin/env python3
"""
Literature Search Pro - Python Core

Multi-source academic literature search with deduplication.
Integrates OpenAlex, Semantic Scholar, and arXiv.

Usage:
    python search.py "your query" --limit 10 --year-min 2020
"""

import argparse
import json
import logging
import hashlib
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Try to import optional dependencies
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    logger.warning("requests library not installed. Run: pip install requests")


@dataclass
class Author:
    name: str
    affiliation: str = ""


@dataclass
class Paper:
    paper_id: str
    title: str
    authors: List[Author]
    year: int
    abstract: str
    venue: str
    citation_count: int
    doi: str
    arxiv_id: str
    url: str
    source: str


class LiteratureSearcher:
    """Multi-source literature searcher with deduplication."""
    
    def __init__(self, cache_dir: Optional[Path] = None, cache_ttl_hours: int = 24):
        self.cache_dir = cache_dir or Path(__file__).parent / "cache"
        self.cache_ttl_hours = cache_ttl_hours
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # API endpoints
        self.openalex_url = "https://api.openalex.org/works"
        self.s2_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.arxiv_url = "http://export.arxiv.org/api/query"
        
    def search(self, query: str, limit: int = 10, year_min: int = 2020,
               sources: List[str] = None, deduplicate: bool = True,
               refresh: bool = False) -> Dict[str, Any]:
        """
        Search literature across multiple sources.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            year_min: Minimum publication year
            sources: List of sources to search ['openalex', 'semantic_scholar', 'arxiv']
            deduplicate: Enable deduplication
            refresh: Force cache refresh
            
        Returns:
            Dictionary with 'total' and 'papers' keys
        """
        if sources is None:
            sources = ['openalex', 'semantic_scholar', 'arxiv']
            
        if not HAS_REQUESTS:
            raise RuntimeError("requests library required. Install with: pip install requests")
        
        # Check cache
        cache_key = self._get_cache_key(query, limit, year_min, sources)
        cached = self._get_cache(cache_key) if not refresh else None
        
        if cached:
            logger.info("Returning cached results")
            return cached
        
        # Search each source
        all_papers: List[Paper] = []
        
        if 'openalex' in sources:
            try:
                papers = self._search_openalex(query, limit, year_min)
                logger.info(f"OpenAlex: found {len(papers)} papers")
                all_papers.extend(papers)
            except Exception as e:
                logger.warning(f"OpenAlex search failed: {e}")
        
        if 'semantic_scholar' in sources:
            try:
                papers = self._search_semantic_scholar(query, limit, year_min)
                logger.info(f"Semantic Scholar: found {len(papers)} papers")
                all_papers.extend(papers)
            except Exception as e:
                logger.warning(f"Semantic Scholar search failed: {e}")
        
        if 'arxiv' in sources:
            try:
                papers = self._search_arxiv(query, limit, year_min)
                logger.info(f"arXiv: found {len(papers)} papers")
                all_papers.extend(papers)
            except Exception as e:
                logger.warning(f"arXiv search failed: {e}")
        
        # Deduplicate
        if deduplicate:
            papers = self._deduplicate(all_papers)
            logger.info(f"After deduplication: {len(papers)} unique papers")
        else:
            papers = all_papers
        
        # Sort by citation count
        papers.sort(key=lambda p: p.citation_count, reverse=True)
        
        # Limit results
        papers = papers[:limit]
        
        # Cache results
        result = {
            'total': len(papers),
            'papers': [asdict(p) for p in papers],
            'cached_at': datetime.now().isoformat()
        }
        self._put_cache(cache_key, result)
        
        return result
    
    def _search_openalex(self, query: str, limit: int, year_min: int) -> List[Paper]:
        """Search OpenAlex API."""
        params = {
            'filter': f'from_publication_date:{year_min}-01-01',
            'per_page': min(limit, 200),
            'select': 'id,title,authorship,publication_year,abstract,venue,cited_by_count,doi,open_access'
        }
        
        # OpenAlex uses natural language search with ?filter=
        response = requests.get(
            f"{self.openalex_url}?search={query}",
            params=params,
            timeout=30
        )
        response.raise_for_status()
        
        data = response.json()
        papers = []
        
        for work in data.get('results', []):
            try:
                authors = [
                    Author(name=a.get('author', {}).get('display_name', ''),
                          affiliation=a.get('institutions', [{}])[0].get('display_name', ''))
                    for a in work.get('authorship', [])[:10]
                ]
                
                paper = Paper(
                    paper_id=work.get('id', ''),
                    title=work.get('title', '') or 'No title',
                    authors=authors,
                    year=work.get('publication_year', 0),
                    abstract=work.get('abstract', '') or '',
                    venue=work.get('venue', '') or '',
                    citation_count=work.get('cited_by_count', 0),
                    doi=work.get('doi', ''),
                    arxiv_id='',
                    url=work.get('open_access', {}).get('oa_url', ''),
                    source='openalex'
                )
                papers.append(paper)
            except Exception as e:
                logger.debug(f"Skip OpenAlex result: {e}")
                continue
        
        return papers
    
    def _search_semantic_scholar(self, query: str, limit: int, year_min: int) -> List[Paper]:
        """Search Semantic Scholar API."""
        params = {
            'query': query,
            'limit': min(limit, 100),
            'fields': 'title,authors,year,abstract,venue,citationCount,externalIds,url',
            'year': f'{year_min}-'
        }
        
        response = requests.get(self.s2_url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        papers = []
        
        for item in data.get('data', []):
            try:
                authors = [
                    Author(name=a.get('name', ''), affiliation='')
                    for a in item.get('authors', [])[:10]
                ]
                
                external_ids = item.get('externalIds', {})
                
                paper = Paper(
                    paper_id=item.get('paperId', ''),
                    title=item.get('title', '') or 'No title',
                    authors=authors,
                    year=item.get('year', 0),
                    abstract=item.get('abstract', '') or '',
                    venue=item.get('venue', '') or '',
                    citation_count=item.get('citationCount', 0),
                    doi=external_ids.get('DOI', ''),
                    arxiv_id=external_ids.get('ArXiv', ''),
                    url=item.get('url', ''),
                    source='semantic_scholar'
                )
                papers.append(paper)
            except Exception as e:
                logger.debug(f"Skip S2 result: {e}")
                continue
        
        return papers
    
    def _search_arxiv(self, query: str, limit: int, year_min: int) -> List[Paper]:
        """Search arXiv API."""
        # Build arXiv query
        search_query = f'all:{query.replace(" ", "+")}'
        start = 0
        max_results = min(limit, 100)
        
        response = requests.get(
            self.arxiv_url,
            params={
                'search_query': search_query,
                'start': start,
                'max_results': max_results,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            },
            timeout=30
        )
        response.raise_for_status()
        
        # Parse Atom XML (simplified)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            try:
                title_elem = entry.find('atom:title', ns)
                title = title_elem.text.strip() if title_elem is not None else 'No title'
                
                summary_elem = entry.find('atom:summary', ns)
                abstract = summary_elem.text.strip() if summary_elem is not None else ''
                
                published_elem = entry.find('atom:published', ns)
                year = int(published_elem.text[:4]) if published_elem is not None else 0
                
                if year < year_min:
                    continue
                
                authors = []
                for author_elem in entry.findall('atom:author', ns):
                    name_elem = author_elem.find('atom:name', ns)
                    if name_elem is not None:
                        authors.append(Author(name=name_elem.text))
                
                id_elem = entry.find('atom:id', ns)
                arxiv_id = id_elem.text.split('/')[-1] if id_elem is not None else ''
                
                paper = Paper(
                    paper_id=arxiv_id,
                    title=title,
                    authors=authors[:10],
                    year=year,
                    abstract=abstract,
                    venue='arXiv',
                    citation_count=0,  # arXiv doesn't provide citation count
                    doi='',
                    arxiv_id=arxiv_id,
                    url=arxiv_id,
                    source='arxiv'
                )
                papers.append(paper)
                
                if len(papers) >= limit:
                    break
            except Exception as e:
                logger.debug(f"Skip arXiv result: {e}")
                continue
        
        return papers
    
    def _deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """Deduplicate papers by DOI, arXiv ID, or title."""
        seen_dois = set()
        seen_arxiv = set()
        seen_titles = set()
        unique = []
        
        for paper in papers:
            # Check DOI
            if paper.doi and paper.doi.lower() in seen_dois:
                continue
            
            # Check arXiv ID
            if paper.arxiv_id and paper.arxiv_id.lower() in seen_arxiv:
                continue
            
            # Check title (fuzzy - normalize)
            title_norm = self._normalize_title(paper.title)
            if title_norm in seen_titles:
                continue
            
            # Add to seen sets
            if paper.doi:
                seen_dois.add(paper.doi.lower())
            if paper.arxiv_id:
                seen_arxiv.add(paper.arxiv_id.lower())
            seen_titles.add(title_norm)
            
            unique.append(paper)
        
        return unique
    
    def _normalize_title(self, title: str) -> str:
        """Normalize title for comparison."""
        import re
        # Lowercase, remove punctuation, collapse whitespace
        title = title.lower()
        title = re.sub(r'[^\w\s]', '', title)
        title = ' '.join(title.split())
        return title
    
    def _get_cache_key(self, query: str, limit: int, year_min: int, sources: List[str]) -> str:
        """Generate cache key from search parameters."""
        key_str = f"{query}|{limit}|{year_min}|{','.join(sorted(sources))}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_cache(self, key: str) -> Optional[Dict]:
        """Get cached results."""
        cache_file = self.cache_dir / f"{key}.json"
        
        if not cache_file.exists():
            return None
        
        try:
            data = json.loads(cache_file.read_text())
            cached_at = datetime.fromisoformat(data.get('cached_at', ''))
            age_hours = (datetime.now() - cached_at).total_seconds() / 3600
            
            if age_hours > self.cache_ttl_hours:
                cache_file.unlink()
                return None
            
            return data
        except Exception as e:
            logger.debug(f"Cache read error: {e}")
            return None
    
    def _put_cache(self, key: str, data: Dict):
        """Cache search results."""
        cache_file = self.cache_dir / f"{key}.json"
        cache_file.write_text(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(description='Search academic literature')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--limit', type=int, default=10, help='Max results')
    parser.add_argument('--year-min', type=int, default=2020, help='Minimum year')
    parser.add_argument('--sources', type=str, default='openalex,semantic_scholar,arxiv',
                       help='Comma-separated sources')
    parser.add_argument('--deduplicate', action='store_true', default=True,
                       help='Enable deduplication')
    parser.add_argument('--no-deduplicate', action='store_false', dest='deduplicate',
                       help='Disable deduplication')
    parser.add_argument('--refresh', action='store_true', help='Force cache refresh')
    
    args = parser.parse_args()
    
    searcher = LiteratureSearcher()
    sources = [s.strip() for s in args.sources.split(',')]
    
    results = searcher.search(
        query=args.query,
        limit=args.limit,
        year_min=args.year_min,
        sources=sources,
        deduplicate=args.deduplicate,
        refresh=args.refresh
    )
    
    # Output as JSON
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
