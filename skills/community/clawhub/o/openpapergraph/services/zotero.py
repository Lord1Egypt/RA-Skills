"""Zotero API client (sync)."""
from typing import List, Optional

import httpx

from schemas import Paper

ZOTERO_API = "https://api.zotero.org"


def get_collections(user_id: str, api_key: str) -> list:
    headers = {"Zotero-API-Key": api_key, "Zotero-API-Version": "3"}
    with httpx.Client(timeout=30) as client:
        resp = client.get(f"{ZOTERO_API}/users/{user_id}/collections", headers=headers, params={"format": "json"})
        resp.raise_for_status()
    return [{"key": c["data"]["key"], "name": c["data"]["name"], "num_items": c["meta"].get("numItems", 0)}
            for c in resp.json()]


def import_papers(user_id: str, api_key: str, collection_key: Optional[str] = None, limit: int = 50) -> List[Paper]:
    base = f"{ZOTERO_API}/users/{user_id}/items"
    if collection_key:
        base = f"{ZOTERO_API}/users/{user_id}/collections/{collection_key}/items"
    headers = {"Zotero-API-Key": api_key, "Zotero-API-Version": "3"}
    with httpx.Client(timeout=30) as client:
        resp = client.get(base, headers=headers, params={"limit": limit, "format": "json"})
        resp.raise_for_status()

    papers = []
    for item in resp.json():
        data = item.get("data", {})
        if data.get("itemType") in ("attachment", "note"):
            continue
        creators = data.get("creators", [])
        authors = [f"{c.get('firstName', '')} {c.get('lastName', '')}".strip() for c in creators]
        authors = [a for a in authors if a]
        date_str = data.get("date", "")
        year = None
        for part in date_str.split("-"):
            if part.isdigit() and len(part) == 4:
                year = int(part)
                break
        doi = data.get("DOI", "")
        papers.append(Paper(
            id=f"DOI:{doi}" if doi else f"zotero:{item.get('key', '')}",
            title=data.get("title", "Untitled"), authors=authors, year=year,
            abstract=data.get("abstractNote"),
            url=data.get("url") or (f"https://doi.org/{doi}" if doi else None),
        ))
    return papers
