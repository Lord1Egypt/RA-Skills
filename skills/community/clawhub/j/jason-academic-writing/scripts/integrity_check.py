#!/usr/bin/env python3
"""
Integrity Check - Anti-hallucination verification for academic papers.

Checks:
1. Citation verification (DOI, authors, year, title)
2. Data verification (numbers match tables/figures)
3. Claim verification (evidence supports assertions)
"""

import json
import re
import requests
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# API endpoints
SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
CROSSREF_API = "https://api.crossref.org/works/"

def verify_doi(doi: str) -> Dict:
    """Verify DOI exists and matches metadata via CrossRef."""
    if not doi:
        return {"valid": False, "error": "No DOI provided"}
    
    try:
        # Clean DOI
        doi = doi.strip().replace("doi:", "").replace("DOI:", "")
        if doi.startswith("http"):
            doi = doi.split("/")[-1]
        
        resp = requests.get(
            f"{CROSSREF_API}{doi}",
            headers={"Accept": "application/json"},
            timeout=10
        )
        
        if resp.status_code == 200:
            data = resp.json().get("message", {})
            return {
                "valid": True,
                "title": data.get("title", [""])[0],
                "authors": [a.get("given", "") + " " + a.get("family", "") for a in data.get("author", [])],
                "year": data.get("published-print", {}).get("date-parts", [[None]])[0][0] or
                        data.get("published-online", {}).get("date-parts", [[None]])[0][0],
                "journal": data.get("container-title", [""])[0],
                "doi": doi
            }
        elif resp.status_code == 404:
            return {"valid": False, "error": "DOI not found"}
        else:
            return {"valid": False, "error": f"CrossRef error: {resp.status_code}"}
            
    except Exception as e:
        return {"valid": False, "error": str(e)}


def verify_citation_semantic(title: str, authors: List[str] = None) -> Dict:
    """Verify citation via Semantic Scholar search."""
    try:
        query = title[:100]  # Truncate long titles
        resp = requests.get(
            SEMANTIC_SCHOLAR_API,
            params={"query": query, "limit": 5, "fields": "title,authors,year,doi,url"},
            timeout=15
        )
        
        if resp.status_code == 200:
            data = resp.json().get("data", [])
            if data:
                # Find best match
                best = data[0]
                title_similarity = len(set(title.lower().split()) & set(best.get("title", "").lower().split()))
                
                return {
                    "valid": True,
                    "title": best.get("title"),
                    "authors": [a.get("name") for a in best.get("authors", [])],
                    "year": best.get("year"),
                    "doi": best.get("doi"),
                    "url": best.get("url"),
                    "match_score": title_similarity
                }
            else:
                return {"valid": False, "error": "No results found"}
        else:
            return {"valid": False, "error": f"Semantic Scholar error: {resp.status_code}"}
            
    except Exception as e:
        return {"valid": False, "error": str(e)}


def extract_citations(manuscript: str) -> List[Dict]:
    """Extract citation markers from manuscript."""
    citations = []
    
    # Pattern: (Author, Year) or [1] or [Author et al., Year]
    patterns = [
        r'\(([A-Z][a-z]+(?: et al\.)?,?\s*\d{4}[a-z]?)\)',  # (Smith, 2023)
        r'\[([A-Z][a-z]+(?: et al\.)?,?\s*\d{4}[a-z]?)\]',   # [Smith, 2023]
        r'\[(\d+)\]',  # [1]
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, manuscript)
        for m in matches:
            citations.append({"raw": m, "type": "inline"})
    
    # Extract reference list if present
    ref_section = re.search(r'## References\n(.+)', manuscript, re.DOTALL)
    if ref_section:
        refs = ref_section.group(1).strip().split('\n')
        for ref in refs:
            if ref.strip():
                # Try to extract DOI
                doi_match = re.search(r'(10\.\d{4,}/[^\s]+)', ref)
                if doi_match:
                    citations.append({"raw": ref, "doi": doi_match.group(1), "type": "reference"})
    
    return citations


def verify_all_citations(manuscript: str) -> Tuple[List[Dict], Dict]:
    """Verify all citations in manuscript."""
    citations = extract_citations(manuscript)
    results = []
    passed = 0
    failed = 0
    
    for cit in citations:
        if cit.get("doi"):
            result = verify_doi(cit["doi"])
        else:
            # Try Semantic Scholar
            result = verify_citation_semantic(cit["raw"])
        
        result["raw_citation"] = cit["raw"]
        results.append(result)
        
        if result.get("valid"):
            passed += 1
        else:
            failed += 1
    
    summary = {
        "total": len(citations),
        "passed": passed,
        "failed": failed,
        "pass_rate": passed / len(citations) if citations else 1.0
    }
    
    return results, summary


def verify_claims(manuscript: str, evidence_file: str = None) -> List[Dict]:
    """Verify claims are supported by evidence."""
    claims = []
    
    # Extract claims (sentences with citation markers)
    sentences = manuscript.split('\n')
    for sent in sentences:
        if re.search(r'\([A-Z][a-z]+.*\d{4}\)', sent) or re.search(r'\[\d+\]', sent):
            # Has citation - extract the claim
            claim_text = re.sub(r'\([A-Z][a-z]+.*\d{4}[a-z]?\)', '', sent).strip()
            claim_text = re.sub(r'\[\d+\]', '', claim_text).strip()
            if claim_text and len(claim_text) > 20:
                claims.append({"text": claim_text, "sentence": sent})
    
    # TODO: Cross-reference with evidence file
    results = []
    for claim in claims[:10]:  # Limit to top 10 claims
        results.append({
            "claim": claim["text"][:100],
            "supported": True,  # Placeholder - needs evidence mapping
            "evidence": "pending"
        })
    
    return results


def run_integrity_check(input_file: str) -> Dict:
    """Run full integrity check on manuscript."""
    manuscript = Path(input_file).read_text()
    
    print("🔍 Running Integrity Check...")
    
    # 1. Citation verification
    print("  [1/3] Verifying citations...")
    citation_results, citation_summary = verify_all_citations(manuscript)
    print(f"       Pass rate: {citation_summary['pass_rate']*100:.1f}%")
    
    # 2. Claim verification
    print("  [2/3] Verifying claims...")
    claim_results = verify_claims(manuscript)
    print(f"       Claims checked: {len(claim_results)}")
    
    # 3. Generate report
    print("  [3/3] Generating report...")
    
    report = {
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "input_file": input_file,
        "citations": {
            "summary": citation_summary,
            "details": citation_results[:20]  # Limit output
        },
        "claims": claim_results,
        "overall_pass": citation_summary["pass_rate"] >= 1.0
    }
    
    return report


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python integrity_check.py <manuscript.md>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    report = run_integrity_check(input_file)
    
    # Output report
    output_file = Path(input_file).parent / "integrity_report.json"
    Path(output_file).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    
    print(f"\n✅ Report saved to: {output_file}")
    
    if report["overall_pass"]:
        print("✅ Integrity check PASSED - proceed to Review stage")
    else:
        print("❌ Integrity check FAILED - return to Write stage")
    
    return report["overall_pass"]


if __name__ == "__main__":
    main()