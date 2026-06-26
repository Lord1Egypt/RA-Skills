#!/usr/bin/env python3
"""
Google Scholar Search Script

This script provides functionality to search Google Scholar via SerpAPI,
parse results, and download PDFs when available.

Requirements:
- serpapi Python package: pip install google-search-results
- SERP_API_KEY environment variable or direct parameter
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs
import time

class GoogleScholarSearch:
    """Google Scholar search client using SerpAPI"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Google Scholar search client.
        
        Args:
            api_key: SerpAPI key. If None, will try to get from SERP_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv('SERP_API_KEY')
        if not self.api_key:
            raise ValueError("SerpAPI key is required. Set SERP_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://serpapi.com/search"
    
    def search(self, query: str, num_results: int = 10, start: int = 0, 
               year_from: Optional[int] = None, year_to: Optional[int] = None,
               sort_by: str = "relevance", include_citations: bool = True,
               language: str = "en", only_reviews: bool = False) -> Dict[str, Any]:
        """
        Search Google Scholar for papers using SerpAPI.
        
        Args:
            query: Search query string (supports advanced syntax like author:, source:)
            num_results: Number of results to return (1-20, default 10)
            start: Starting position for pagination (0, 10, 20, etc.)
            year_from: Filter results from this year (as_ylo)
            year_to: Filter results to this year (as_yhi)
            sort_by: Sort method ("relevance" or "date")
            include_citations: Whether to include citations in results
            language: Language code (hl parameter)
            only_reviews: Whether to show only review articles
            
        Returns:
            Dictionary containing search results
        """
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": self.api_key,
            "num": min(max(num_results, 1), 20),  # SerpAPI限制1-20
            "start": start,
            "hl": language,
            "as_vis": "0" if include_citations else "1",  # 0=include citations
            "as_rr": "1" if only_reviews else "0"  # 1=only review articles
        }
        
        # Add year filter if specified
        if year_from or year_to:
            if year_from and year_to:
                params["as_ylo"] = year_from
                params["as_yhi"] = year_to
            elif year_from:
                params["as_ylo"] = year_from
            elif year_to:
                params["as_yhi"] = year_to
        
        # Add sort parameter
        if sort_by == "date":
            params["scisbd"] = "1"  # Sort by date, abstracts only
        elif sort_by == "date_all":
            params["scisbd"] = "2"  # Sort by date, all content
        else:
            params["scisbd"] = "0"  # Sort by relevance (default)
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "error" in data:
                print(f"SerpAPI Error: {data['error']}", file=sys.stderr)
            
            return data
            
        except requests.exceptions.Timeout:
            print("Error: Request timeout", file=sys.stderr)
            return {"error": "Request timeout", "organic_results": []}
        except requests.exceptions.RequestException as e:
            print(f"Error searching Google Scholar: {e}", file=sys.stderr)
            return {"error": str(e), "organic_results": []}
    
    def parse_results(self, search_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Parse SerpAPI search results into a structured format.
        
        Args:
            search_data: Raw search data from SerpAPI
            
        Returns:
            List of parsed paper information
        """
        papers = []
        
        if "organic_results" not in search_data:
            return papers
        
        for result in search_data["organic_results"]:
            # Extract basic information
            paper = {
                "position": result.get("position", 0),
                "title": result.get("title", ""),
                "result_id": result.get("result_id", ""),
                "link": result.get("link", ""),
                "snippet": result.get("snippet", ""),
                "type": result.get("type", ""),
                "publication_info": result.get("publication_info", {}),
                "resources": result.get("resources", []),
                "inline_links": result.get("inline_links", {})
            }
            
            # Extract citation count
            cited_by = result.get("inline_links", {}).get("cited_by", {})
            paper["cited_by"] = cited_by.get("total", 0) if cited_by else 0
            paper["cites_id"] = cited_by.get("cites_id", "") if cited_by else ""
            
            # Extract version information
            versions = result.get("inline_links", {}).get("versions", {})
            paper["versions"] = versions.get("total", 0) if versions else 0
            paper["cluster_id"] = versions.get("cluster_id", "") if versions else ""
            
            # Extract year from publication info
            publication_summary = result.get("publication_info", {}).get("summary", "")
            paper["year"] = self._extract_year(publication_summary)
            
            # Extract authors - try both methods
            paper["authors"] = self._extract_authors_from_info(result.get("publication_info", {}))
            if not paper["authors"]:
                paper["authors"] = self._extract_authors(publication_summary)
            
            # Try to find PDF link
            pdf_link = self._find_pdf_link(result)
            if pdf_link:
                paper["pdf_link"] = pdf_link
                paper["has_pdf"] = True
            else:
                paper["has_pdf"] = False
            
            # Extract related links
            inline_links = result.get("inline_links", {})
            paper["cite_link"] = inline_links.get("serpapi_cite_link", "")
            paper["related_pages_link"] = inline_links.get("related_pages_link", "")
            
            papers.append(paper)
        
        return papers
    
    def _extract_authors_from_info(self, publication_info: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract authors from publication_info.authors array."""
        authors = []
        if "authors" in publication_info:
            for author in publication_info["authors"]:
                author_info = {"name": author.get("name", "")}
                if "link" in author:
                    author_info["link"] = author["link"]
                if "author_id" in author:
                    author_info["author_id"] = author["author_id"]
                authors.append(author_info)
        return authors
    
    def _extract_year(self, summary: str) -> Optional[int]:
        """Extract publication year from summary string."""
        import re
        year_match = re.search(r'\b(19|20)\d{2}\b', summary)
        return int(year_match.group()) if year_match else None
    
    def _extract_authors(self, summary: str) -> List[str]:
        """Extract authors from summary string."""
        # Simple extraction - in practice, you might want more sophisticated parsing
        if " - " in summary:
            authors_part = summary.split(" - ")[0]
            return [author.strip() for author in authors_part.split(",")]
        return []
    
    def _find_pdf_link(self, result: Dict[str, Any]) -> Optional[str]:
        """Find PDF link in search result."""
        # Check resources
        for resource in result.get("resources", []):
            if resource.get("title", "").lower() == "pdf":
                return resource.get("link", "")
        
        # Check inline links
        inline_links = result.get("inline_links", {})
        for link_type, link_data in inline_links.items():
            if link_type == "pdf" and "link" in link_data:
                return link_data["link"]
        
        return None
    
    def download_pdf(self, pdf_url: str, save_path: str) -> bool:
        """
        Download a PDF file from a URL.
        
        Args:
            pdf_url: URL of the PDF file
            save_path: Local path to save the PDF
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(pdf_url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"PDF downloaded successfully: {save_path}")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"Error downloading PDF: {e}", file=sys.stderr)
            return False
    
    def search_by_author(self, author_name: str, num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search papers by specific author.
        
        Args:
            author_name: Author name to search for
            num_results: Number of results to return
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary with search results
        """
        query = f'author:"{author_name}"'
        return self.search(query, num_results=num_results, **kwargs)
    
    def search_cited_by(self, cites_id: str, num_results: int = 10, **kwargs) -> Dict[str, Any]:
        """
        Search papers that cite a specific paper.
        
        Args:
            cites_id: The cites ID of the paper
            num_results: Number of results to return
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary with search results
        """
        params = {
            "engine": "google_scholar",
            "cites": cites_id,
            "api_key": self.api_key,
            "num": min(max(num_results, 1), 20),
            "hl": kwargs.get("language", "en")
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching citations: {e}", file=sys.stderr)
            return {"error": str(e), "organic_results": []}
    
    def search_versions(self, cluster_id: str, **kwargs) -> Dict[str, Any]:
        """
        Search all versions of a specific paper.
        
        Args:
            cluster_id: The cluster ID of the paper
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary with search results
        """
        params = {
            "engine": "google_scholar",
            "cluster": cluster_id,
            "api_key": self.api_key,
            "hl": kwargs.get("language", "en")
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error searching versions: {e}", file=sys.stderr)
            return {"error": str(e), "organic_results": []}
    
    def search_and_download(self, query: str, download_dir: str = "./downloads", 
                           max_papers: int = 5, **kwargs) -> Dict[str, Any]:
        """
        Search for papers and download available PDFs.
        
        Args:
            query: Search query
            download_dir: Directory to save downloaded PDFs
            max_papers: Maximum number of papers to process
            **kwargs: Additional search parameters
            
        Returns:
            Dictionary with search results and download status
        """
        # Create download directory if it doesn't exist
        os.makedirs(download_dir, exist_ok=True)
        
        # Search for papers
        print(f"Searching for: {query}")
        
        # 从kwargs中移除num_results，因为我们在search方法中单独传递
        search_kwargs = kwargs.copy()
        if 'num_results' in search_kwargs:
            del search_kwargs['num_results']
            
        search_data = self.search(query, num_results=max_papers, **search_kwargs)
        
        if "error" in search_data:
            return {"error": search_data["error"], "papers": []}
        
        # Parse results
        papers = self.parse_results(search_data)
        
        # Download PDFs
        download_results = []
        successful_downloads = 0
        
        for i, paper in enumerate(papers[:max_papers]):
            print(f"\n[{i+1}/{len(papers[:max_papers])}] Processing: {paper['title'][:80]}...")
            
            if paper.get("has_pdf", False) and "pdf_link" in paper:
                # Generate filename
                safe_title = "".join(c for c in paper['title'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_title = safe_title[:100]  # Limit filename length
                
                # Add year if available
                if paper.get('year'):
                    filename = f"{paper['year']}_{safe_title}.pdf"
                else:
                    filename = f"{safe_title}.pdf"
                    
                filepath = os.path.join(download_dir, filename)
                
                print(f"  Found PDF: {paper['pdf_link']}")
                print(f"  Downloading to: {filepath}")
                
                success = self.download_pdf(paper['pdf_link'], filepath)
                paper['download_success'] = success
                paper['download_path'] = filepath if success else None
                
                if success:
                    successful_downloads += 1
            else:
                print(f"  No PDF available")
                paper['download_success'] = False
                paper['download_path'] = None
            
            download_results.append(paper)
        
        # Get search metadata
        search_info = search_data.get("search_information", {})
        
        return {
            "query": query,
            "total_results": search_info.get("total_results", 0),
            "papers_found": len(papers),
            "papers_with_pdf": sum(1 for p in papers if p.get("has_pdf", False)),
            "successful_downloads": successful_downloads,
            "search_metadata": search_data.get("search_metadata", {}),
            "papers": download_results
        }


def main():
    """Command-line interface for Google Scholar search."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Search Google Scholar using SerpAPI and download PDFs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "machine learning" --num 10
  %(prog)s "author:\"Yoshua Bengio\"" --sort date
  %(prog)s "transformer" --year-from 2020 --year-to 2024
  %(prog)s "deep learning" --output ./papers --no-citations
        """
    )
    
    # Basic arguments
    parser.add_argument("query", nargs="?", help="Search query (use author:\"name\" for author search)")
    parser.add_argument("--api-key", help="SerpAPI key (or set SERP_API_KEY env var)")
    
    # Search parameters
    parser.add_argument("--num", type=int, default=10, help="Number of results (1-20, default: 10)")
    parser.add_argument("--output", default="./downloads", help="Output directory for PDFs")
    parser.add_argument("--year-from", type=int, help="Filter results from this year")
    parser.add_argument("--year-to", type=int, help="Filter results to this year")
    parser.add_argument("--sort", choices=["relevance", "date", "date_all"], default="relevance", 
                       help="Sort method: relevance, date (abstracts only), date_all")
    
    # Advanced filters
    parser.add_argument("--language", default="en", help="Language code (default: en)")
    parser.add_argument("--no-citations", action="store_true", help="Exclude citations from results")
    parser.add_argument("--only-reviews", action="store_true", help="Show only review articles")
    
    # Special search modes
    parser.add_argument("--cites", help="Search papers citing a specific paper (cites ID)")
    parser.add_argument("--cluster", help="Search all versions of a paper (cluster ID)")
    
    # Output options
    parser.add_argument("--no-download", action="store_true", help="Search only, don't download PDFs")
    parser.add_argument("--json-only", action="store_true", help="Output only JSON results")
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.query and not args.cites and not args.cluster:
        parser.error("Either query, --cites, or --cluster must be provided")
    
    if args.cites and args.cluster:
        parser.error("Cannot use both --cites and --cluster")
    
    if args.num < 1 or args.num > 20:
        parser.error("--num must be between 1 and 20")
    
    try:
        # Initialize client
        client = GoogleScholarSearch(api_key=args.api_key)
        
        if args.cites:
            # Search citations
            print(f"Searching papers citing: {args.cites}")
            result = client.search_cited_by(args.cites, num_results=args.num, language=args.language)
            
        elif args.cluster:
            # Search versions
            print(f"Searching versions of: {args.cluster}")
            result = client.search_versions(args.cluster, language=args.language)
            
        else:
            # Regular search
            search_kwargs = {
                "num_results": args.num,
                "year_from": args.year_from,
                "year_to": args.year_to,
                "sort_by": args.sort,
                "include_citations": not args.no_citations,
                "language": args.language,
                "only_reviews": args.only_reviews
            }
            
            if args.no_download:
                # Search only
                print(f"Searching: {args.query}")
                result = client.search(args.query, **search_kwargs)
            else:
                # Search and download
                result = client.search_and_download(
                    query=args.query,
                    download_dir=args.output,
                    max_papers=args.num,
                    **search_kwargs
                )
        
        # Handle JSON-only output
        if args.json_only:
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return
        
        # Print summary for regular searches
        if "query" in result:
            print("\n" + "="*60)
            print("SEARCH SUMMARY")
            print("="*60)
            print(f"Query: {result['query']}")
            
            if 'search_metadata' in result:
                metadata = result['search_metadata']
                print(f"Search ID: {metadata.get('id', 'N/A')}")
                print(f"Status: {metadata.get('status', 'N/A')}")
            
            if 'search_information' in result:
                info = result.get('search_information', {})
                print(f"Total results: {info.get('total_results', 'N/A')}")
            
            print(f"Papers found: {result.get('papers_found', len(result.get('papers', [])))}")
            print(f"Papers with PDF: {result.get('papers_with_pdf', 'N/A')}")
            
            if not args.no_download:
                print(f"Successfully downloaded: {result.get('successful_downloads', 0)}")
        
        # Save results to JSON
        if not args.json_only:
            json_path = os.path.join(args.output, "search_results.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"\nDetailed results saved to: {json_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if not args.json_only:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()