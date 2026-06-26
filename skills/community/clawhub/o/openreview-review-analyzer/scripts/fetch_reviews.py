#!/usr/bin/env python3
"""
Fetch all public reviews and comments for a given OpenReview forum ID.
Outputs structured JSON to /tmp/openreview_<forum_id>.json

Uses the OpenReview REST API directly — NO openreview-py dependency.
Works with just Python standard library (urllib). Uses requests if available.

Usage:
    python3 fetch_reviews.py <forum_id>
    python3 fetch_reviews.py uZWbPNVBUU
    python3 fetch_reviews.py "https://openreview.net/forum?id=uZWbPNVBUU"
"""

import json
import sys
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# ---------------------------------------------------------------------------
# HTTP helper — use requests if available, otherwise fall back to urllib
# ---------------------------------------------------------------------------

try:
    import requests

    def http_get(url, params=None):
        r = requests.get(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()

except ImportError:
    import urllib.request
    import urllib.error

    def http_get(url, params=None):
        if params:
            from urllib.parse import urlencode
            url = url + "?" + urlencode(params)
        req = urllib.request.Request(url, headers={"User-Agent": "OpenReview-Fetcher/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------

API_V2 = "https://api2.openreview.net"
API_V1 = "https://api.openreview.net"

# ---------------------------------------------------------------------------
# Content extraction helpers
# ---------------------------------------------------------------------------

def extract_value(obj):
    """Extract value from OpenReview content field (handles both v1 and v2 formats)."""
    if isinstance(obj, dict) and "value" in obj:
        return obj["value"]
    return obj


def extract_content(content_dict):
    """Flatten a note's content dict, extracting all values."""
    if not content_dict:
        return {}
    return {k: extract_value(v) for k, v in content_dict.items()}


def classify_note(note, api_version=2):
    """Classify a note by its invitation type."""
    if api_version == 2:
        invitations = note.get("invitations", [])
        inv_str = " ".join(invitations).lower()
    else:
        inv_str = (note.get("invitation", "") or "").lower()

    if "official_review" in inv_str or "/review" in inv_str:
        return "review"
    elif "meta_review" in inv_str or "metareview" in inv_str:
        return "meta_review"
    elif "decision" in inv_str:
        return "decision"
    elif "rebuttal" in inv_str:
        return "rebuttal"
    else:
        return "comment"


def format_timestamp(ts_ms):
    """Convert millisecond timestamp to readable date string."""
    if not ts_ms:
        return "N/A"
    try:
        return datetime.fromtimestamp(ts_ms / 1000).strftime("%Y-%m-%d %H:%M")
    except (ValueError, OSError):
        return "N/A"


def parse_rating(value):
    """Extract numeric rating from string like '5: Borderline accept' or plain int."""
    if isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        try:
            return int(value.split(":")[0].strip())
        except ValueError:
            return value
    return value


def build_note_entry(note, api_version=2):
    """Build a standardized entry dict from a raw note."""
    content = extract_content(note.get("content", {}))
    return {
        "id": note.get("id"),
        "signatures": note.get("signatures", []),
        "invitations": note.get("invitations", []) if api_version == 2 else [note.get("invitation", "")],
        "created": format_timestamp(note.get("cdate")),
        "content": content,
    }


# ---------------------------------------------------------------------------
# API v2 fetcher
# ---------------------------------------------------------------------------

def fetch_v2(forum_id):
    """Fetch paper + all replies via OpenReview API v2."""
    print("  Fetching submission...")
    data = http_get(f"{API_V2}/notes", params={"id": forum_id})
    notes = data.get("notes", [])
    if not notes:
        raise Exception(f"No submission found for forum ID: {forum_id}")
    submission = notes[0]

    paper_content = extract_content(submission.get("content", {}))
    paper_info = {
        "id": submission["id"],
        "title": paper_content.get("title", "N/A"),
        "authors": paper_content.get("authors", []),
        "abstract": paper_content.get("abstract", "N/A"),
        "keywords": paper_content.get("keywords", []),
        "venue": paper_content.get("venue", "N/A"),
        "venueid": paper_content.get("venueid", "N/A"),
        "domain": submission.get("domain", "N/A"),
        "url": f"https://openreview.net/forum?id={forum_id}",
    }

    # Fetch all replies in the forum
    print("  Fetching all replies...")
    all_replies = []
    offset = 0
    limit = 1000
    while True:
        data = http_get(f"{API_V2}/notes", params={
            "forum": forum_id,
            "offset": offset,
            "limit": limit,
        })
        batch = data.get("notes", [])
        all_replies.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    # Classify replies
    result = {"review": [], "comment": [], "meta_review": [], "decision": [], "rebuttal": []}
    for note in all_replies:
        if note["id"] == forum_id:
            continue
        category = classify_note(note, api_version=2)
        result[category].append(build_note_entry(note, api_version=2))

    return paper_info, result


# ---------------------------------------------------------------------------
# API v1 fetcher (fallback for older venues)
# ---------------------------------------------------------------------------

def fetch_v1(forum_id):
    """Fetch paper + all replies via OpenReview API v1."""
    print("  Fetching submission (API v1)...")
    data = http_get(f"{API_V1}/notes", params={"id": forum_id})
    notes = data.get("notes", [])
    if not notes:
        raise Exception(f"No submission found for forum ID: {forum_id} (API v1)")
    submission = notes[0]

    content = submission.get("content", {})
    paper_info = {
        "id": submission["id"],
        "title": content.get("title", "N/A"),
        "authors": content.get("authors", []),
        "abstract": content.get("abstract", "N/A"),
        "keywords": content.get("keywords", []),
        "venue": content.get("venue", "N/A"),
        "venueid": content.get("venueid", "N/A"),
        "url": f"https://openreview.net/forum?id={forum_id}",
    }

    print("  Fetching all replies (API v1)...")
    all_replies = []
    offset = 0
    limit = 1000
    while True:
        data = http_get(f"{API_V1}/notes", params={
            "forum": forum_id,
            "offset": offset,
            "limit": limit,
        })
        batch = data.get("notes", [])
        all_replies.extend(batch)
        if len(batch) < limit:
            break
        offset += limit

    result = {"review": [], "comment": [], "meta_review": [], "decision": [], "rebuttal": []}
    for note in all_replies:
        if note["id"] == forum_id:
            continue
        category = classify_note(note, api_version=1)
        result[category].append(build_note_entry(note, api_version=1))

    return paper_info, result


# ---------------------------------------------------------------------------
# Rating / confidence extraction
# ---------------------------------------------------------------------------

def extract_scores(reviews):
    """Extract ratings and confidences from review entries."""
    ratings = []
    confidences = []

    for r in reviews:
        c = r.get("content", {})

        # Rating — try common field names
        for key in ["rating", "recommendation", "score", "overall_assessment", "overall"]:
            if key in c:
                ratings.append(parse_rating(c[key]))
                break

        # Confidence
        for key in ["confidence", "reviewer_confidence"]:
            if key in c:
                confidences.append(parse_rating(c[key]))
                break

    return ratings, confidences


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_reviews.py <forum_id_or_url>")
        print("Example: python3 fetch_reviews.py uZWbPNVBUU")
        print('Example: python3 fetch_reviews.py "https://openreview.net/forum?id=uZWbPNVBUU"')
        sys.exit(1)

    raw_input = sys.argv[1].strip()

    # Parse URL if provided
    if "openreview.net" in raw_input:
        parsed = urlparse(raw_input)
        params = parse_qs(parsed.query)
        forum_id = params.get("id", [raw_input])[0]
    else:
        forum_id = raw_input

    print(f"Fetching reviews for forum ID: {forum_id}")
    print(f"URL: https://openreview.net/forum?id={forum_id}\n")

    paper_info = None
    classified = None

    # Try API v2 first, then v1
    for api_name, fetch_fn in [("API v2", fetch_v2), ("API v1", fetch_v1)]:
        try:
            print(f"Trying {api_name}...")
            paper_info, classified = fetch_fn(forum_id)
            print(f"  ✓ Success with {api_name}\n")
            break
        except Exception as e:
            print(f"  ✗ {api_name} failed: {e}\n")

    if paper_info is None:
        print("ERROR: Could not fetch paper from either API.")
        print("Possible reasons:")
        print("  - Invalid forum ID")
        print("  - Reviews are not yet public")
        print("  - Paper has been deleted")
        print("  - Network connectivity issue")
        sys.exit(1)

    reviews = classified["review"]
    ratings, confidences = extract_scores(reviews)

    summary = {
        "total_reviews": len(reviews),
        "total_comments": len(classified["comment"]),
        "total_meta_reviews": len(classified["meta_review"]),
        "total_decisions": len(classified["decision"]),
        "total_rebuttals": len(classified["rebuttal"]),
        "ratings": ratings,
        "confidences": confidences,
    }

    if ratings and all(isinstance(r, (int, float)) for r in ratings):
        summary["avg_rating"] = round(sum(ratings) / len(ratings), 2)
    if confidences and all(isinstance(c, (int, float)) for c in confidences):
        summary["avg_confidence"] = round(sum(confidences) / len(confidences), 2)

    output = {
        "paper": paper_info,
        "reviews": reviews,
        "comments": classified["comment"],
        "meta_reviews": classified["meta_review"],
        "decisions": classified["decision"],
        "rebuttals": classified["rebuttal"],
        "summary": summary,
    }

    output_path = f"/tmp/openreview_{forum_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2, default=str)

    # Print summary
    print("=" * 55)
    print(f"  Paper:   {paper_info.get('title', 'N/A')}")
    print(f"  Venue:   {paper_info.get('venue', 'N/A')}")
    print(f"  Domain:  {paper_info.get('domain', 'N/A')}")
    print("-" * 55)
    print(f"  Reviews:      {len(reviews)}")
    print(f"  Comments:     {len(classified['comment'])}")
    print(f"  Meta-reviews: {len(classified['meta_review'])}")
    print(f"  Decisions:    {len(classified['decision'])}")
    print(f"  Rebuttals:    {len(classified['rebuttal'])}")
    if ratings:
        print(f"  Ratings:      {ratings}")
        if "avg_rating" in summary:
            print(f"  Avg rating:   {summary['avg_rating']}")
    if confidences:
        print(f"  Confidences:  {confidences}")
    print("=" * 55)
    print(f"\n✓ Output saved to: {output_path}")


if __name__ == "__main__":
    main()
