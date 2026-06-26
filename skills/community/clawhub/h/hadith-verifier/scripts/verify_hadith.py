#!/usr/bin/env python3
"""
Hadith Verification Engine
Verifies hadith authenticity against major collections via fawazahmed0/hadith-api.
Returns: verified / weak / fabricated-not-found / needs-manual-review
"""

import json
import sys
import re
import urllib.request
from typing import Dict, List, Optional, Tuple

BASE_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"

# Major collections with their grading authority
COLLECTIONS = {
    "bukhari": {"name": "صحيح البخاري", "weight": "highest", "langs": ["eng-bukhari", "ara-bukhari"]},
    "muslim": {"name": "صحيح مسلم", "weight": "highest", "langs": ["eng-muslim", "ara-muslim"]},
    "tirmidhi": {"name": "جامع الترمذي", "weight": "high", "langs": ["eng-tirmidhi", "ara-tirmidhi"]},
    "abudawud": {"name": "سنن أبي داود", "weight": "high", "langs": ["eng-abudawud", "ara-abudawud"]},
    "nasai": {"name": "سنن النسائي", "weight": "high", "langs": ["eng-nasai", "ara-nasai"]},
    "ibnmajah": {"name": "سنن ابن ماجه", "weight": "medium", "langs": ["eng-ibnmajah", "ara-ibnmajah"]},
    "malik": {"name": "موطأ مالك", "weight": "high", "langs": ["eng-malik", "ara-malik"]},
}

# Known fabricated / weak patterns (common in AI-generated hadith)
FABRICATED_PATTERNS = [
    r"من قرأ آية كذا.*فله أجر كذا",  # Vague reward promises
    r"من فعل شيئا.*?دخل الجنة",  # Simple action = guaranteed paradise
    r"النبي.* قال.* إن الله يحب",  # Generic "Allah loves" without source
]


def fetch_json(url: str) -> Optional[dict]:
    """Fetch JSON from URL with timeout."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HadithVerifier/1.0"})
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read())
    except Exception as e:
        return None


def normalize_text(text: str) -> str:
    """Normalize Arabic/English text for comparison."""
    # Remove diacritics
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Remove common prefixes
    text = re.sub(r'^(narrated|عن|حدثنا|أخبرنا|قال)', '', text, flags=re.IGNORECASE).strip()
    return text[:300]  # Limit for comparison


def search_hadith_by_number(collection: str, hadith_num: int) -> Optional[dict]:
    """Look up a hadith by collection slug and number."""
    url = f"{base_url_eng(collection)}"
    data = fetch_json(url)
    if not data:
        return None
    
    hadiths = data.get("hadiths", [])
    for h in hadiths:
        if h.get("hadithnumber") == hadith_num:
            return {
                "collection": collection,
                "number": hadith_num,
                "text_en": h.get("text", ""),
                "text_ar": "",
                "reference": h.get("reference", {}),
                "grades": h.get("grades", []),
            }
    return None


def base_url_eng(collection: str) -> str:
    return f"{BASE_URL}/editions/eng-{collection}.json"


def base_url_ar(collection: str) -> str:
    return f"{BASE_URL}/editions/ara-{collection}.json"


def search_text_in_collection(text: str, collection: str) -> List[dict]:
    """Search for matching hadith text in a collection."""
    url = base_url_eng(collection)
    data = fetch_json(url)
    if not data:
        return []
    
    hadiths = data.get("hadiths", [])
    norm_input = normalize_text(text)
    results = []
    
    for h in hadiths:
        norm_h = normalize_text(h.get("text", ""))
        # Simple similarity: check if significant portion matches
        if len(norm_input) > 20 and len(norm_h) > 20:
            # Check for substantial text overlap
            words_input = set(norm_input.split())
            words_h = set(norm_h.split())
            overlap = len(words_input & words_h)
            if overlap > 5:  # At least 5 common words
                similarity = overlap / max(len(words_input), 1)
                if similarity > 0.3:  # 30% overlap threshold
                    results.append({
                        "collection": collection,
                        "number": h.get("hadithnumber"),
                        "text": h.get("text", "")[:200],
                        "reference": h.get("reference", {}),
                        "grades": h.get("grades", []),
                        "similarity": round(similarity, 2),
                    })
    
    return results[:5]  # Max 5 results per collection


def check_fabricated_patterns(text: str) -> List[str]:
    """Check for patterns common in AI-generated fabricated hadith."""
    flags = []
    
    # Check for overly specific numerical promises
    if re.search(r'\d+\s*(مرة|مرة\s*واحدة|أضعاف|درجات)', text):
        flags.append("SPECIFIC_NUMBER_PROMISE")
    
    # Check for guaranteed paradise for simple acts
    if re.search(r'(دخل الجنة|كُتب له أجر|مح的日ي)', text) and len(text) < 150:
        flags.append("SIMPLE_ACT_PARADISE")
    
    # Very short "hadith" without isnad is suspicious
    if len(text) < 100:
        flags.append("TOO_SHORT_NO_ISNAD")
    
    return flags


def verify_hadith(hadith_text: str, claimed_source: str = None, claimed_number: int = None) -> dict:
    """
    Main verification function.
    
    Args:
        hadith_text: The hadith text to verify
        claimed_source: Optional claimed source (e.g., "bukhari", "muslim")
        claimed_number: Optional claimed hadith number
    
    Returns:
        Verification result with status and details
    """
    result = {
        "status": "unknown",
        "confidence": 0.0,
        "found_in": [],
        "not_found_in": [],
        "warnings": [],
        "recommendation": "",
    }
    
    # Step 1: Check fabricated patterns
    fab_flags = check_fabricated_patterns(hadith_text)
    if fab_flags:
        result["warnings"].extend(fab_flags)
    
    # Step 2: If source and number provided, verify directly
    if claimed_source and claimed_number:
        collection = claimed_source.lower().replace(" ", "")
        if collection in COLLECTIONS:
            found = search_hadith_by_number(collection, claimed_number)
            if found:
                result["found_in"].append(found)
                # Now verify text similarity
                if hadith_text and found.get("text_en"):
                    norm_input = normalize_text(hadith_text)
                    norm_found = normalize_text(found["text_en"])
                    words_input = set(norm_input.split())
                    words_found = set(norm_found.split())
                    overlap = len(words_input & words_found)
                    similarity = overlap / max(len(words_input), 1)
                    
                    if similarity > 0.5:
                        result["status"] = "verified"
                        result["confidence"] = min(similarity * 100, 99)
                    elif similarity > 0.3:
                        result["status"] = "partial_match"
                        result["confidence"] = similarity * 100
                        result["warnings"].append("TEXT_PARTIALLY_MATCHES")
                    else:
                        result["status"] = "text_mismatch"
                        result["confidence"] = 0
                        result["warnings"].append("TEXT_DOES_NOT_MATCH_SOURCE")
            else:
                result["not_found_in"].append(collection)
                result["status"] = "not_found"
        else:
            result["warnings"].append(f"UNKNOWN_COLLECTION: {claimed_source}")
    
    # Step 3: Cross-search all collections if no specific source
    if not claimed_source and hadith_text:
        all_results = []
        for slug in COLLECTIONS:
            results = search_text_in_collection(hadith_text, slug)
            all_results.extend(results)
        
        if all_results:
            # Sort by similarity
            all_results.sort(key=lambda x: x["similarity"], reverse=True)
            best = all_results[0]
            
            if best["similarity"] > 0.6:
                result["status"] = "likely_authentic"
                result["confidence"] = best["similarity"] * 100
            elif best["similarity"] > 0.4:
                result["status"] = "possible_match"
                result["confidence"] = best["similarity"] * 100
            else:
                result["status"] = "weak_match"
                result["confidence"] = best["similarity"] * 100
            
            result["found_in"] = all_results[:3]
        else:
            result["status"] = "not_found"
            result["confidence"] = 0
    
    # Step 4: Final recommendation
    if result["status"] in ["verified", "likely_authentic"]:
        if result.get("warnings"):
            result["recommendation"] = "AUTHENTIC_BUT_REVIEW_WARNINGS"
        else:
            result["recommendation"] = "AUTHENTIC_PUBLISH_WITH_SOURCE"
    elif result["status"] in ["partial_match", "possible_match", "weak_match"]:
        result["recommendation"] = "NEEDS_MANUAL_REVIEW"
    elif result["status"] in ["not_found", "text_mismatch"]:
        if fab_flags:
            result["recommendation"] = "LIKELY_FABRICATED_DO_NOT_PUBLISH"
        else:
            result["recommendation"] = "NOT_FOUND_DO_NOT_PUBLISH"
    else:
        result["recommendation"] = "INSUFFICIENT_DATA"
    
    return result


def main():
    """CLI interface for hadith verification."""
    if len(sys.argv) < 2:
        print("Usage: python verify_hadith.py '<hadith_text>' [--source <collection>] [--number <num>]")
        print("\nExample:")
        print("  python verify_hadith.py 'Actions are judged by intentions' --source bukhari --number 1")
        print("  python verify_hadith.py 'من غشنا ليس منا' --source muslim")
        sys.exit(1)
    
    hadith_text = sys.argv[1]
    claimed_source = None
    claimed_number = None
    
    # Parse optional args
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--source" and i + 1 < len(sys.argv):
            claimed_source = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--number" and i + 1 < len(sys.argv):
            claimed_number = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    result = verify_hadith(hadith_text, claimed_source, claimed_number)
    
    # Output as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
