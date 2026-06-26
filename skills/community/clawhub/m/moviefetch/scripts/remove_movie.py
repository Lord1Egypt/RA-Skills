#!/usr/bin/env python3
"""
homeflix / remove_movie
Finds a movie in Radarr by title and removes it from the library.
Optionally deletes the downloaded files.
"""
import json
import os
import sys
import requests

RADARR_URL     = os.environ.get("RADARR_URL", "http://localhost:7878/api/v3")
RADARR_API_KEY = os.environ.get("RADARR_API_KEY", "")

HEADERS = {"X-Api-Key": RADARR_API_KEY}


def find_movie_in_library(title: str):
    """Search the Radarr library for a movie by title (case-insensitive partial match)."""
    resp = requests.get(f"{RADARR_URL}/movie", headers=HEADERS, timeout=10)
    resp.raise_for_status()
    title_lower = title.lower()
    matches = [m for m in resp.json() if title_lower in m["title"].lower()]
    if not matches:
        return None
    # Prefer exact match, fall back to first partial
    for m in matches:
        if m["title"].lower() == title_lower:
            return m
    return matches[0]


def remove_from_queue(movie_id: int, delete_files: bool):
    """Delete the movie record from Radarr (and optionally its files)."""
    params = {
        "deleteFiles":            str(delete_files).lower(),
        "addImportExclusion":     "false",
    }
    resp = requests.delete(
        f"{RADARR_URL}/movie/{movie_id}",
        headers=HEADERS,
        params=params,
        timeout=10,
    )
    return resp.status_code in (200, 204)


def main():
    try:
        input_data   = json.loads(sys.argv[1])
        title        = input_data.get("movie_title", "").strip()
        delete_files = input_data.get("delete_files", True)

        if not title:
            print(json.dumps({"error": "movie_title is required"}))
            return

        movie = find_movie_in_library(title)
        if not movie:
            print(json.dumps({
                "status":  "not_found",
                "message": f"'{title}' is not in your Radarr library.",
            }))
            return

        success = remove_from_queue(movie["id"], delete_files)
        if success:
            action = "removed with files" if delete_files else "removed from library"
            print(json.dumps({
                "status":  "removed",
                "title":   movie["title"],
                "year":    movie["year"],
                "action":  action,
            }))
        else:
            print(json.dumps({
                "status":  "error",
                "message": f"Radarr failed to delete '{movie['title']}'.",
            }))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
