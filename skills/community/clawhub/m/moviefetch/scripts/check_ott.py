#!/usr/bin/env python3
import json
import os
import sys
import requests

TMDB_API_KEY = os.environ.get("TMDB_API_KEY", "")
TMDB_URL = "https://api.themoviedb.org/3"

def search_tmdb(query: str, media_type: str = "movie"):
    """Search for a movie or TV series on TMDB."""
    url = f"{TMDB_URL}/search/{media_type}"
    params = {"api_key": TMDB_API_KEY, "query": query}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results", [])
    return results[0] if results else None

def get_watch_providers(tmdb_id: int, media_type: str = "movie"):
    """Get OTT providers for a movie/TV series."""
    url = f"{TMDB_URL}/{media_type}/{tmdb_id}/watch/providers"
    params = {"api_key": TMDB_API_KEY}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    # Looking for India (IN) by default as per user's timezone
    results = resp.json().get("results", {})
    return results.get("IN", {})

def main():
    try:
        if len(sys.argv) < 2:
            print(json.dumps({"error": "Usage: check_ott.py <query> [movie|tv]"}))
            return
            
        query = sys.argv[1]
        media_type = sys.argv[2] if len(sys.argv) > 2 else "movie"
        
        # Try both if media_type not specified
        result = search_tmdb(query, media_type)
        if not result and len(sys.argv) <= 2:
            media_type = "tv"
            result = search_tmdb(query, media_type)
            
        if not result:
            print(json.dumps({"error": f"No results found for '{query}'"}))
            return
            
        tmdb_id = result["id"]
        title = result.get("title") or result.get("name")
        year = (result.get("release_date") or result.get("first_air_date", ""))[:4]
        
        providers = get_watch_providers(tmdb_id, media_type)
        
        output = {
            "title": title,
            "year": year,
            "media_type": media_type,
            "streaming": providers.get("flatrate", []),
            "rent": providers.get("rent", []),
            "buy": providers.get("buy", []),
            "link": providers.get("link")
        }
        print(json.dumps(output))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    main()
