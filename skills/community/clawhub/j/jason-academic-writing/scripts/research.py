#!/usr/bin/env python3
"""
Research Agent - Literature search and evidence collection.

Uses Semantic Scholar API to search and grade evidence.
"""

import json
import os
import sys
import requests
from pathlib import Path
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"

# Evidence levels
EVIDENCE_LEVELS = {
    'A': 'Meta-analysis or systematic review',
    'B': 'Randomized controlled trial',
    'C': 'Observational study or cohort',
    'D': 'Case report or expert opinion'
}


def search_papers(query: str, limit: int = 20) -> List[Dict]:
    """Search Semantic Scholar for papers."""
    try:
        response = requests.get(
            SEMANTIC_SCHOLAR_API,
            params={
                "query": query,
                "limit": limit,
                "fields": "title,authors,year,abstract,venue,citationCount,referenceCount,url,doi"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json().get("data", [])
            return data
        else:
            print(f"⚠️ Semantic Scholar error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"⚠️ Search failed: {e}")
        return []


def grade_evidence(paper: Dict) -> str:
    """Grade evidence level based on paper type."""
    venue = paper.get("venue", "").lower()
    abstract = paper.get("abstract", "").lower()
    
    # Meta-analysis indicators
    meta_keywords = ["meta-analysis", "systematic review", "review of", "synthesis"]
    if any(kw in venue or kw in abstract for kw in meta_keywords):
        return 'A'
    
    # RCT indicators
    rct_keywords = ["randomized", "randomised", "controlled trial", "rct"]
    if any(kw in abstract for kw in rct_keywords):
        return 'B'
    
    # Observational indicators
    obs_keywords = ["observational", "cohort", "cross-sectional", "survey", "longitudinal"]
    if any(kw in abstract for kw in obs_keywords):
        return 'C'
    
    # Default
    return 'D'


def collect_evidence(topic: str, output_dir: str = "research") -> Dict:
    """Collect and organize evidence for a topic."""
    print(f"📚 Collecting evidence for: {topic}")
    
    # Multiple search queries for coverage
    queries = [
        topic,
        f"{topic} review",
        f"{topic} systematic",
        f"{topic} recent advances"
    ]
    
    all_papers = []
    for query in queries:
        print(f"  Searching: {query}")
        papers = search_papers(query, limit=10)
        all_papers.extend(papers)
    
    # Deduplicate by DOI
    unique_papers = {}
    for paper in all_papers:
        doi = paper.get("doi") or paper.get("url")
        if doi and doi not in unique_papers:
            paper["evidence_level"] = grade_evidence(paper)
            unique_papers[doi] = paper
    
    papers_list = list(unique_papers.values())
    
    # Sort by citation count (proxy for importance)
    papers_list.sort(key=lambda x: x.get("citationCount", 0), reverse=True)
    
    # Grade distribution
    grade_dist = {}
    for paper in papers_list:
        grade = paper["evidence_level"]
        grade_dist[grade] = grade_dist.get(grade, 0) + 1
    
    print(f"  ✅ Found {len(papers_list)} unique papers")
    print(f"     Evidence distribution: A={grade_dist.get('A',0)}, B={grade_dist.get('B',0)}, C={grade_dist.get('C',0)}, D={grade_dist.get('D',0)}")
    
    # Save evidence file
    output_path = Path(output_dir) / "evidence.json"
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    evidence_data = {
        "topic": topic,
        "papers": papers_list[:30],  # Top 30
        "grade_distribution": grade_dist,
        "total_count": len(papers_list),
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    
    Path(output_path).write_text(json.dumps(evidence_data, indent=2, ensure_ascii=False))
    print(f"  ✅ Saved to {output_path}")
    
    return evidence_data


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python research.py <topic>")
        sys.exit(1)
    
    topic = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "research"
    
    evidence = collect_evidence(topic, output_dir)
    
    # Quality gate check
    grade_a_count = evidence["grade_distribution"].get('A', 0)
    grade_b_count = evidence["grade_distribution"].get('B', 0)
    
    if grade_a_count >= 2 and (grade_a_count + grade_b_count) >= 5:
        print("\n✅ Evidence quality gate PASSED - proceed to Write stage")
        return True
    else:
        print("\n❌ Evidence quality gate FAILED - need more high-quality sources")
        return False


if __name__ == "__main__":
    main()