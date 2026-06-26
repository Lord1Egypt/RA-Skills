#!/usr/bin/env python3
"""
Multi-Source Academic Paper Search
Downloads papers from arXiv, Semantic Scholar, DBLP with progress tracking for background execution.

Usage:
    python multi_source_search.py -q "machine learning" -l 20 [--background]
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


class ProgressTracker:
    """Handle progress file creation and updates for background task monitoring."""
    
    def __init__(self, output_dir: Path, task_id: str = "literature_search"):
        self.task_id = task_id
        self.progress_file = output_dir.parent / f"search-progress-{task_id}.json"
        self.start_time = datetime.now()
        
    def update(self, stage: str, progress_percent: int) -> None:
        """Write progress status to file for monitoring."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        status = {
            "task_id": self.task_id,
            "stage": stage,
            "progress_percent": progress_percent,
            "elapsed_seconds": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(),
            "status": "running" if progress_percent < 100 else "completed",
        }
        
        self.progress_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)
            
        print(f"[{progress_percent}%] {stage} ({elapsed:.1f}s)")
        
    def complete(self, summary_dict: dict) -> None:
        """Mark task as completed with final statistics."""
        status = {
            "task_id": self.task_id,
            "stage": "completed",
            "progress_percent": 100,
            "completed_at": datetime.now().isoformat(),
            "status": "completed successfully",
            "summary": summary_dict
        }
        
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(status, f, indent=2)

        print(f"✅ COMPLETED: {summary_dict.get('total_papers_found', 0)} papers found")


def search_arxiv(query: str, year_from: int = None, limit: int = 10) -> list:
    """Search arXiv API (mock implementation - replace with actual requests)."""
    
    progress_tracker.update(f"Querying arXiv for '{query[:30]}...'", 15)
    
    # TODO: Implement actual arXiv API request
    mock_results = [
        {
            "title": f"Paper title from arXiv - search query: {query}",
            "authors": ["Author1", "Author2"],
            "year": 2023,
            "doi": "arxiv:2301.xxxxxx",
            "abstract": "This paper addresses the research problem..."
        }
        for _ in range(min(5, limit))
    ]
    
    return mock_results


def search_semantic_scholar(query: str, year_from: int = None, limit: int = 10) -> list:
    """Search Semantic Scholar API (mock implementation)."""
    
    progress_tracker.update(f"Querying Semantic Scholar...", 30)
    
    # TODO: Implement semantic scholar Open Review / API v2
    mock_results = [
        {
            "title": f"Semantic Scholar paper on {query[:40]}...",
            "authors": ["Researcher A", "Researcher B"], 
            "year": 2022,
            "venue": "NeurIPS 2022",
            "citations": 45,
            "abstract": "Abstract text for semantic scholar result..."
        } 
        for _ in range(min(4, limit))
    ]
    
    return mock_results


def process_and_deduplicate(results_list: list) -> dict:
    """Organize search results by source and remove duplicates."""
    
    progress_tracker.update("Deduplicating results...", 70)
    
    organized = {
        "arxiv": [],
        "semantic_scholar": [],
        "total_unique": 0
    }
    
    seen_titles = set()
    
    for result in results_list:  
        title_key = result["title"].lower().strip()
        
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            
            if "arxiv" in str(result.get("doi", "")).lower():
                organized["arxiv"].append(result)  
            else: 
                organized["semantic_scholar"].append(result)

    organized["total_unique"] = len(seen_titles)
    
    return organized


def save_results(results_dict: dict, output_dir: Path, args):
    """Save search results to multiple formats for downstream processing."""
    
    progress_tracker.update(f"Saving results to {output_dir.name}...", 85)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    bibtex_file = output_dir / f"search-results-{timestamp}.bibtex"
    
    bibtex_content = generate_bibtex_from_results(results_dict, args)  
    
    with open(bibtex_file, 'w', encoding='utf-8') as f:
        f.write(bibtex_content)

    summary_file = output_dir / f"search-summary-{timestamp}.md"
    
    markdown_content = generate_markdown_summary(results_dict, args)
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)

    return str(bibtex_file), str(summary_file)


def generate_bibtex_from_results(results: dict, args) -> str:
    """Generate BibTeX entries for all papers."""
    
    bibtex_entries = []
    all_papers = results["arxiv"] + results["semantic_scholar"]
    
    for idx, paper in enumerate(all_papers, 1): 
        citation_key = f"{paper['year']}{paper['authors'][0].lower().replace(' ', '')}_" \
                      f"{''.join(paper['title'].split()[:2]).replace(' ', '_')}"
        
        bibtex_entry = f'@article{{--{citation_key}--}}'  # Simplified format to avoid f-string issues
```python
# Improved paper metadata extraction with proper error handling
def extract_paper_info(paper_entry):
    """Extract paper info from arXiv entry element"""
    try:
        title = ''
        for elem in paper_entry.findall('atom:title', namespaces):
            text = ''.join(elem.itertext()) if elem.text else str(paper_entry.findtext('atom/title'))
            titles = text.split(',')
            title = ', '.join(titles[:3])  # Avoid overly long titles with comma
        return {
            'title': title.strip(),
            'id': paper_entry.get('http://arxiv.org/schemas/atom') or paper_entry.findtext('atom/id'),
            'summary': ''.join([elem.text for elem in paper_entry.findall('atom:summary')]) or ''
        }
    except Exception as e:
        print(f"⚠️ Warning: Could not parse entry {paper_entry.get('http://arxiv.org/schemas/atom')} - error: {e}")
        return {}
```
  title = {{{paper.get('title', 'Untitled')}},
  author = {{{', '.join([a if isinstance(a, str) else str(a) for a in paper.get('authors', ['Author'])])}}},  
  year = {{}}{{{{paper['year']}},
  journal = {paper.get('venue', 'arXiv preprint')}},
  doi = {{{paper.get('doi', 'N/A')}}}
}}"""

        bibtex_entries.append(bibtex_entry)
    
    header = f"""% PhD Research Companion - Multi-Source Search Results  
% Generated: {datetime.now().isoformat()}
% Query: "{args.query}"  
% Sources used: {','.join(args.sources)}
% Total unique papers found: {results['total_unique']}

"""

    return header + "\\n\\n".join(bibtex_entries)


def generate_markdown_summary(results: dict, args) -> str:  
    """Create human-readable markdown summary for reviewer/advisor."""
    
    total = results['total_unique']
    arxiv_count = len(results["arxiv"])
    ss_count = len(results["semantic_scholar"]) 
    
    md_content = f"""# Literature Search Results Summary

Search Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
Query: "{args.query}"  
Total Unique Papers Found: {total}  

## Source Breakdown:
- arXiv preprints: {arxiv_count} papers  
- Semantic Scholar indexed: {ss_count} papers

## Top Results (first 5):

"""
    
    all_results = results["arxiv"] + results["semantic_scholar"][:min(5, total)]
    
    for i, paper in enumerate(all_results[:10], 1): 
        md_content += f"""### {i}. {paper.get('title', 'Untitled')}  

Authors: {', '.join([str(a) for a in paper.get('authors', ['Unknown'])])}  
Year/Venue: {paper.get('year', 'N/A')} | {paper.get('venue', '')}  
DOI: {paper.get('doi', 'Not provided')}
"""
        
    md_content += """---
Generated by PhD Research Companion - Literature Search Module"""

    return md_content


progress_tracker = None


def main():
    global progress_tracker
    
    parser = argparse.ArgumentParser(description="Multi-source academic paper search with background execution support")
    
    parser.add_argument("--query", "-q", required=True, help="Search query keywords for literature discovery")
    parser.add_argument("--sources", "-s", nargs='+', default=["arxiv"], choices=["arxiv", "semanticscholar", "dblp", "ieee"], help="Which sources to search (default: arxiv)")
    parser.add_argument("--year-from", type=int, default=None, help="Minimum publication year filter") 
    parser.add_argument("--limit", "-l", type=int, default=15, help="Maximum papers to retrieve per source")
    parser.add_argument("--output-dir", "-o", type=str, required=True, help="Output directory for search results")
    parser.add_argument("--background", "-b", action='store_true', help="Run with progress tracking for background execution monitoring")
    
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir).expanduser().resolve()  
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Starting PhD Research Companion - Literature Search")
    print(f"   Query: {args.query}")
    print(f"   Sources: {', '.join(args.sources)}")
    print(f"   Output: {output_dir}")
    
    progress_tracker = ProgressTracker(output_dir, task_id="search") if args.background else None
    
    if progress_tracker: 
        progress_tracker.update("Starting literature search", 10)
    else:
        print("[10%] Starting literature search.\\n")

    all_results = [] 
    
    for source_num, source in enumerate(args.sources, 1):
        if "arxiv" in source.lower():
            progress_tracker.update(f"Querying arXiv ({source_num}/{len(args.sources)})", 50)
            results_arxiv = search_arxiv(args.query, args.year_from, args.limit)
            all_results.extend(results_arxiv)
            
        elif "semantic" in source.lower() or "scholar" in source.lower():
            progress_tracker.update(f"Querying Semantic Scholar ({source_num}/{len(args.sources)})", 65)
            results_ss = search_semantic_scholar(args.query, args.year_from, args.limit)
            all_results.extend(results_ss)

    results_dict = process_and_deduplicate(all_results)
    
    if progress_tracker:
        progress_tracker.update("Deduplicating and saving results.", 80)
        
    bibtex_path, summary_path = save_results(results_dict, output_dir, args)
    
    if progress_tracker: 
        summary_stats = {"query": args.query, "sources_used": list(args.sources), "papers_found": results_dict["total_unique"], "output_bibtex": bibtex_path, "output_summary": summary_path}
        progress_tracker.complete(summary_stats)
        
    else:
        print(f"\nSearch completed!")
        print(f"Results saved to:")
        print(f"   - BibTeX: {bibtex_path}")
        print(f"   - Summary: {summary_path}")

    print(f"\nFinal Statistics: ")
    print(f"   Total unique papers: {results_dict['total_unique']}")
    if 'arxiv' in results_dict:
        print(f"   - From arXiv: {len(results_dict['arxiv'])}")
    if 'semantic_scholar' in results_dict:
        print(f"   - From Semantic Scholar: {len(results_dict['semantic_scholar'])}")

if __name__ == "__main__":
    main()