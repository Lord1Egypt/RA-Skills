from __future__ import annotations

import json

import gitea_api as g


def read(owner: str, repo: str) -> dict:
    try:
        raw = g.read_text(owner, repo, "catalog.json")
        return json.loads(raw)
    except Exception:
        return {"documents": [], "concepts": [], "resources": [], "people": [], "projects": [], "reviews": [], "imports": []}
