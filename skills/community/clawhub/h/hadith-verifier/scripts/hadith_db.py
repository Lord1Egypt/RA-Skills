#!/usr/bin/env python3
"""
Hadith Database Search Engine
Searches fawazahmed0/hadith-api (via jsDelivr) across major collections.
Returns matching hadiths with full reference info.
"""

import json
import re
import sys
import urllib.request
from typing import Dict, List, Optional

BASE_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1"

COLLECTIONS = {
    "bukhari": "Sahih al-Bukhari",
    "muslim": "Sahih Muslim",
    "tirmidhi": "Jami' at-Tirmidhi",
    "abudawud": "Sunan Abu Dawud",
    "nasai": "Sunan an-Nasai",
    "ibnmajah": "Sunan Ibn Majah",
    "malik": "Muwatta Malik",
    "nawawi": "Forty Hadith of an-Nawawi",
    "qudsi": "Forty Hadith Qudsi",
    "dehlawi": "Forty Hadith of Shah Waliullah Dehlawi",
}

_cache = {}


def fetch_collection(collection: str, lang: str = "eng") -> Optional[dict]:
    """Fetch a collection's data, with caching."""
    key = f"{lang}-{collection}"
    if key in _cache:
        return _cache[key]
    
    url = f"{BASE_URL}/editions/{key}.json"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "HadithDB/1.0"})
        resp = urllib.request.urlopen(req, timeout=20)
        data = json.loads(resp.read())
        _cache[key] = data
        return data
    except Exception:
        return None


def normalize(text: str) -> str:
    """Normalize text for comparison."""
    # Remove Arabic diacritics
    text = re.sub(r'[\u064B-\u065F\u0670\u0610-\u061A]', '', text)
    # Common normalization
    text = text.lower()
    text = re.sub(r'[^a-z\u0600-\u06FF\s]', ' ', text)  # Keep Arabic + English only
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_keywords(text: str, min_len: int = 3) -> List[str]:
    """Extract meaningful keywords from text."""
    norm = normalize(text)
    # Split and filter
    words = [w for w in norm.split() if len(w) >= min_len]
    return words


def keyword_match_score(query_words: List[str], target_words: List[str]) -> float:
    """Calculate keyword overlap score between query and target."""
    if not query_words:
        return 0.0
    query_set = set(query_words)
    target_set = set(target_words)
    overlap = query_set & target_set
    # Jaccard-like similarity
    return len(overlap) / len(query_set)


def search(query: str, collections: List[str] = None, limit: int = 5, lang: str = "eng") -> List[dict]:
    """Search for matching hadiths across collections."""
    if collections is None:
        collections = list(COLLECTIONS.keys())
    
    query_words = extract_keywords(query)
    if not query_words:
        return []
    
    results = []
    for coll in collections:
        data = fetch_collection(coll, lang)
        if not data:
            continue
        
        hadiths = data.get("hadiths", [])
        for h in hadiths:
            text = h.get("text", "")
            if not text:
                continue
            
            text_words = extract_keywords(text)
            score = keyword_match_score(query_words, text_words)
            
            if score > 0.15:  # Minimum threshold
                # Get reference info
                ref = h.get("reference", {})
                ref_str = ""
                if isinstance(ref, dict):
                    book_num = ref.get("book", "?")
                    hadith_num_ref = ref.get("hadith", "?")
                    ref_str = f"Book {book_num}, Hadith {hadith_num_ref}"
                
                # Also get Arabic if available
                ar_text = ""
                if lang == "eng":
                    ar_data = fetch_collection(coll, "ara")
                    if ar_data:
                        for ah in ar_data.get("hadiths", []):
                            if ah.get("hadithnumber") == h.get("hadithnumber"):
                                ar_text = ah.get("text", "")[:300]
                                break
                
                results.append({
                    "collection": COLLECTIONS.get(coll, coll),
                    "collection_slug": coll,
                    "hadith_number": h.get("hadithnumber"),
                    "text_en": text[:400],
                    "text_ar": ar_text,
                    "reference": ref_str,
                    "grades": h.get("grades", []),
                    "score": round(score, 3),
                })
    
    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]


def get_by_number(collection: str, hadith_num: int) -> Optional[dict]:
    """Get a specific hadith by collection and number."""
    eng_data = fetch_collection(collection, "eng")
    ar_data = fetch_collection(collection, "ara")
    
    if not eng_data:
        return None
    
    for h in eng_data.get("hadiths", []):
        if h.get("hadithnumber") == hadith_num:
            result = {
                "collection": COLLECTIONS.get(collection, collection),
                "hadith_number": hadith_num,
                "text_en": h.get("text", ""),
                "grades": h.get("grades", []),
                "reference": h.get("reference", {}),
            }
            
            # Get Arabic text
            if ar_data:
                for ah in ar_data.get("hadiths", []):
                    if ah.get("hadithnumber") == hadith_num:
                        result["text_ar"] = ah.get("text", "")
                        break
            
            return result
    
    return None


def main():
    """CLI for search."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python hadith_db.py search '<query>' [--collections bukhari,muslim] [--limit 5]")
        print("  python hadith_db.py get <collection> <hadith_number>")
        print("\nExamples:")
        print("  python hadith_db.py search 'intention actions judged'")
        print("  python hadith_db.py search 'من غشنا ليس منا' --collections muslim,bukhari")
        print("  python hadith_db.py get bukhari 1")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "search":
        query = sys.argv[2]
        collections = None
        limit = 5
        
        i = 3
        while i < len(sys.argv):
            if sys.argv[i] == "--collections" and i + 1 < len(sys.argv):
                collections = sys.argv[i + 1].split(",")
                i += 2
            elif sys.argv[i] == "--limit" and i + 1 < len(sys.argv):
                limit = int(sys.argv[i + 1])
                i += 2
            else:
                i += 1
        
        results = search(query, collections, limit)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif cmd == "get":
        collection = sys.argv[2]
        num = int(sys.argv[3])
        result = get_by_number(collection, num)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"error": "Hadith not found"}, ensure_ascii=False))
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
