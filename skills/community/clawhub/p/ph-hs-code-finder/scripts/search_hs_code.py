#!/usr/bin/env python3
"""
Search HS code in a Philippines Tariff PDF file.
"""

import sys
import re
import json
from typing import List, Dict

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is required. Install with: pip install pdfplumber")
    sys.exit(1)


def normalize_keyword(keyword: str) -> str:
    """Normalize keyword for better matching."""
    keyword = keyword.lower().strip()
    # Remove plural forms for simple words
    if keyword.endswith('s') and len(keyword) > 3:
        keyword = keyword[:-1]
    return keyword


def extract_hs_codes_from_pdf(pdf_path: str, keywords: List[str], max_results: int = 20) -> List[Dict]:
    """
    Search for HS codes in a PDF file based on keywords.
    
    Args:
        pdf_path: Path to the PDF file
        keywords: List of keywords to search for
        max_results: Maximum number of results to return
        
    Returns:
        List of dictionaries containing HS code information
    """
    results = []
    seen_codes = set()
    
    # Normalize keywords
    normalized_keywords = [normalize_keyword(kw) for kw in keywords]
    keyword_patterns = [re.compile(r'\b' + re.escape(kw) + r'[a-z]*\b', re.IGNORECASE) for kw in normalized_keywords]
    
    # HS code patterns
    hs_code_patterns = [
        re.compile(r'\b\d{4}\.\d{2}\.\d{2}\b'),  # 8516.31.00
        re.compile(r'\b\d{4}\.\d{2}\b'),         # 8516.31
        re.compile(r'\b\d{4}\b'),                # 8516
    ]
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            try:
                text = page.extract_text()
                if not text:
                    continue
                
                lines = text.split('\n')
                for line_num, line in enumerate(lines, 1):
                    # Check if any keyword matches
                    if any(pattern.search(line) for pattern in keyword_patterns):
                        # Extract HS code from the line
                        hs_code = ""
                        for pattern in hs_code_patterns:
                            match = pattern.search(line)
                            if match:
                                hs_code = match.group(0)
                                break
                        
                        # Clean up the description
                        description = line.strip()
                        # Remove excessive whitespace
                        description = ' '.join(description.split())
                        
                        # Create unique key to avoid duplicates
                        unique_key = f"{hs_code}_{description[:50]}"
                        
                        if unique_key not in seen_codes and len(description) > 10:
                            seen_codes.add(unique_key)
                            results.append({
                                "hs_code": hs_code,
                                "description": description,
                                "page": page_num,
                                "line": line_num
                            })
                            
                            if len(results) >= max_results:
                                return results
            except Exception as e:
                print(f"Warning: Error processing page {page_num}: {e}")
                continue
    
    return results


def format_results_as_markdown(results: List[Dict], source_url: str, product_name: str = "") -> str:
    """Format search results as markdown."""
    if not results:
        return "未找到匹配的海关编码。\n"
    
    output = f"## 查询结果{f': {product_name}' if product_name else ''}\n\n"
    output += f"**源文件**: [{source_url}]({source_url})\n\n"
    output += "| HS编码 | 商品描述 | 页码 |\n"
    output += "|--------|----------|------|\n"
    
    # Sort by HS code (more specific codes first)
    sorted_results = sorted(results, key=lambda x: len(x["hs_code"]) if x["hs_code"] else 0, reverse=True)
    
    for r in sorted_results:
        desc = r["description"]
        # Clean description
        if len(desc) > 80:
            desc = desc[:77] + "..."
        # Escape pipe characters
        desc = desc.replace('|', '\\|')
        hs = r["hs_code"] if r["hs_code"] else "-"
        output += f"| {hs} | {desc} | {r['page']} |\n"
    
    return output


def suggest_best_match(results: List[Dict], keywords: List[str]) -> Dict:
    """Suggest the best matching result based on keyword relevance."""
    if not results:
        return None
    
    # Score each result
    scored_results = []
    for r in results:
        score = 0
        desc_lower = r["description"].lower()
        
        # Score based on keyword matches
        for kw in keywords:
            kw_lower = kw.lower()
            if kw_lower in desc_lower:
                score += 10
                # Bonus for exact word match
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', desc_lower):
                    score += 5
        
        # Bonus for longer HS codes (more specific)
        if r["hs_code"]:
            score += len(r["hs_code"])
        
        scored_results.append((score, r))
    
    # Sort by score
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return scored_results[0][1] if scored_results else None


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: search_hs_code.py <pdf_path> <keyword1> [keyword2] ... [options]")
        print("\nOptions:")
        print("  --json      Output as JSON")
        print("  --source <url>  Source URL to include in output")
        print("\nExamples:")
        print('  python3 search_hs_code.py Chapter_85.pdf "hair" "dryer"')
        print('  python3 search_hs_code.py Chapter_85.pdf "mobile" "phone" --json')
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    # Parse arguments
    keywords = []
    output_json = False
    source_url = ""
    
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--json":
            output_json = True
        elif arg == "--source" and i + 1 < len(sys.argv):
            source_url = sys.argv[i + 1]
            i += 1
        elif not arg.startswith("--"):
            keywords.append(arg)
        i += 1
    
    if not keywords:
        print("Error: No keywords provided")
        sys.exit(1)
    
    results = extract_hs_codes_from_pdf(pdf_path, keywords)
    
    if output_json:
        output = {
            "keywords": keywords,
            "results": results,
            "source_url": source_url,
            "count": len(results)
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(format_results_as_markdown(results, source_url))
        
        # Show best match
        best = suggest_best_match(results, keywords)
        if best:
            print(f"\n**最可能匹配**: {best['hs_code']} - {best['description'][:60]}...")
