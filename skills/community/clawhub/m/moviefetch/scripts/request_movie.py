#!/usr/bin/env python3
"""
homeflix / request_movie
Looks up a movie via Radarr (TMDB) and adds it to the download queue.
Triggers an immediate search via Prowlarr/YTS.
"""
import json
import os
import sys
import requests
import string

RADARR_URL              = os.environ.get("RADARR_URL", "http://localhost:7878/api/v3")
RADARR_API_KEY          = os.environ.get("RADARR_API_KEY", "")
QUALITY_PROFILE_ID      = int(os.environ.get("RADARR_QUALITY_PROFILE_ID", "1"))
ROOT_FOLDER_PATH        = os.environ.get("RADARR_ROOT_FOLDER", "/tmp/plex_movies/")

HEADERS = {"X-Api-Key": RADARR_API_KEY}


def lookup_movie(title: str):
    """Search TMDB via Radarr — returns top match or None."""
    resp = requests.get(
        f"{RADARR_URL}/movie/lookup",
        headers=HEADERS,
        params={"term": title},
        timeout=10,
    )
    if resp.status_code != 200 or not resp.json():
        return None
    return resp.json()[0]


def get_clean_words(text: str):
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    return set(text.split())

def extract_extra_keywords(query: str, title: str):
    query_words = get_clean_words(query)
    title_words = get_clean_words(title)
    # Stopwords specific to natural language requests
    stopwords = {"in", "with", "a", "an", "the", "of", "for", "and", "version", "movie", "film", "i", "want", "to", "download", "get"}
    return query_words - title_words - stopwords

def get_movie_id(tmdb_id: int):
    """Fetch internal Radarr movie ID from TMDB ID."""
    resp = requests.get(
        f"{RADARR_URL}/movie",
        headers=HEADERS,
        params={"tmdbId": tmdb_id},
        timeout=10,
    )
    if resp.status_code == 200:
        movies = resp.json()
        if movies:
            return movies[0].get("id")
    return None

def search_and_download_release(movie_id: int, extra_words: set):
    """Search releases for a movie and queue the first one that matches all extra keywords."""
    resp = requests.get(
        f"{RADARR_URL}/release",
        headers=HEADERS,
        params={"movieId": movie_id},
        timeout=60,
    )
    if resp.status_code != 200:
        return False, f"Release search failed (HTTP {resp.status_code})"

    releases = resp.json()
    valid_releases = []
    
    for r in releases:
        rtitle = r.get("title", "").translate(str.maketrans('', '', string.punctuation)).lower()
        if all(w in rtitle for w in extra_words) and not r.get("rejected", False):
            valid_releases.append(r)
            
    # Fallback: maybe allow rejected ones if no valid ones found?
    # Sometimes language rejections happen but user still wants it
    if not valid_releases:
        for r in releases:
            rtitle = r.get("title", "").translate(str.maketrans('', '', string.punctuation)).lower()
            if all(w in rtitle for w in extra_words):
                valid_releases.append(r)

    if not valid_releases:
        return False, f"No release found matching extra keywords: {', '.join(extra_words)}"
        
    valid_releases.sort(key=lambda x: x.get("seeders", 0), reverse=True)
    best_release = valid_releases[0]

    dl_payload = {
        "guid": best_release["guid"],
        "indexerId": best_release["indexerId"],
        "movieId": movie_id
    }
    dl_resp = requests.post(
        f"{RADARR_URL}/release",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=dl_payload,
        timeout=10,
    )
    
    if dl_resp.status_code in (200, 201):
        return True, best_release.get("title")
    else:
        return False, f"Failed to queue release: {dl_resp.status_code}"

def add_movie(movie: dict, original_query: str):
    """POST to Radarr to monitor + specific search if query has extra words."""
    extra_words = extract_extra_keywords(original_query, movie["title"])
    is_specific_version = len(extra_words) > 0

    payload = {
        "title":            movie["title"],
        "year":             movie["year"],
        "tmdbId":           movie["tmdbId"],
        "titleSlug":        movie["titleSlug"],
        "images":           movie["images"],
        "qualityProfileId": QUALITY_PROFILE_ID,
        "rootFolderPath":   ROOT_FOLDER_PATH,
        "monitored":        True,
        "addOptions": {
            # Only do automatic search if no specific version requested
            "searchForMovie": not is_specific_version
        },
    }
    resp = requests.post(
        f"{RADARR_URL}/movie",
        headers={**HEADERS, "Content-Type": "application/json"},
        json=payload,
        timeout=10,
    )
    
    # 201 Created successfully
    if resp.status_code == 201:
        result = {
            "status": "queued",
            "title":  movie["title"],
            "year":   movie["year"],
        }
        if is_specific_version:
            movie_id = resp.json().get("id")
            if movie_id:
                success, msg = search_and_download_release(movie_id, extra_words)
                if success:
                    result["status"] = "queued_specific_version"
                    result["release_title"] = msg
                else:
                    result["status"] = "queued_base_version_only"
                    result["message"] = msg
        return result

    # 400 Bad Request (Already exists)
    elif resp.status_code == 400 and "already" in resp.text.lower():
        result = {
            "title":  movie["title"],
            "year":   movie["year"],
        }
        if is_specific_version:
            movie_id = get_movie_id(movie["tmdbId"])
            if movie_id:
                success, msg = search_and_download_release(movie_id, extra_words)
                if success:
                    result["status"] = "queued_specific_version"
                    result["release_title"] = msg
                    return result
                else:
                    result["status"] = "duplicate_no_specific_version_found"
                    result["message"] = msg
                    return result

        result["status"] = "duplicate"
        return result

    # Other API Errors
    else:
        return {
            "status": "error",
            "message": f"Radarr returned {resp.status_code}: {resp.text[:200]}",
        }


def main():
    try:
        input_data = json.loads(sys.argv[1])
        title_query = input_data.get("movie_title", "").strip()
        if not title_query:
            print(json.dumps({"error": "movie_title is required"}))
            return

        movie = lookup_movie(title_query)
        if not movie:
            print(json.dumps({"error": f"No TMDB match found for '{title_query}'"}))
            return

        result = add_movie(movie, title_query)
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
