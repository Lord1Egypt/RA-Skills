#!/usr/bin/env python3
"""
homeflix / check_plex
Checks whether a movie already exists in the Plex library.
"""
import json
import os
import sys
import requests

PLEX_URL   = os.environ.get("PLEX_URL", "http://localhost:32400")
PLEX_TOKEN = os.environ.get("PLEX_TOKEN", "")
PLEX_LIBRARY = os.environ.get("PLEX_MOVIE_LIBRARY", "Movies")


def get_library_key():
    """Returns the section key for the configured movie library."""
    url = f"{PLEX_URL}/library/sections"
    headers = {"X-Plex-Token": PLEX_TOKEN, "Accept": "application/json"}
    resp = requests.get(url, headers=headers, timeout=5)
    resp.raise_for_status()
    for section in resp.json()["MediaContainer"]["Directory"]:
        if section["title"].lower() == PLEX_LIBRARY.lower():
            return section["key"]
    return None


def search_plex(title: str, library_key: str):
    """Full-text search within the Plex movie library."""
    url = f"{PLEX_URL}/library/sections/{library_key}/search"
    headers = {"X-Plex-Token": PLEX_TOKEN, "Accept": "application/json"}
    params = {"query": title, "type": 1}  # type 1 = movies
    resp = requests.get(url, headers=headers, params=params, timeout=5)
    resp.raise_for_status()
    results = resp.json()["MediaContainer"].get("Metadata", [])
    return results


def main():
    try:
        input_data = json.loads(sys.argv[1])
        title = input_data.get("movie_title", "").strip()
        if not title:
            print(json.dumps({"error": "movie_title is required"}))
            return

        library_key = get_library_key()
        if not library_key:
            print(json.dumps({"error": f"Plex library '{PLEX_LIBRARY}' not found"}))
            return

        results = search_plex(title, library_key)

        if results:
            match = results[0]
            print(json.dumps({
                "found": True,
                "title": match.get("title"),
                "year": match.get("year"),
                "plex_key": match.get("ratingKey"),
            }))
        else:
            print(json.dumps({"found": False}))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
