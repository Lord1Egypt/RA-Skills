"""Helpers for creating or locating Apify tasks for a user."""

from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TASK_SPECS = [
    {
        "env_var": "APIFY_TASK_ID",
        "name": "portfolio-risk-desk-primary-web",
        "title": "Portfolio Risk Desk Primary Web Evidence",
        "actId": "igolaizola~google-search-scraper-ppe",
        "input": {
            "query": "NVIDIA investor relations earnings",
            "maxItems": 10,
            "country": "us",
            "language": "en",
            "domain": "google.com",
        },
        "options": {
            "timeoutSecs": 180,
            "memoryMbytes": 1024,
            "restartOnError": False,
        },
    },
    {
        "env_var": "APIFY_X_TASK_ID",
        "name": "portfolio-risk-desk-x-signals",
        "title": "Portfolio Risk Desk X Signals",
        "actId": "xtdata~twitter-x-scraper",
        "input": {
            "searchTerms": ['("NVDA" OR "$NVDA") lang:en -is:retweet'],
            "maxItems": 20,
            "sort": "Top",
            "tweetLanguage": "en",
            "includeSearchTerms": True,
        },
        "options": {
            "timeoutSecs": 180,
            "memoryMbytes": 1024,
            "restartOnError": False,
        },
    },
]


def ensure_apify_tasks(
    *,
    token: str,
    base_url: str = "https://api.apify.com/v2",
    include_x_signals: bool = True,
) -> list[dict[str, str]]:
    """Create or update the saved Apify tasks needed by the skill."""

    normalized_base_url = base_url.rstrip("/")
    existing_tasks = _list_tasks(base_url=normalized_base_url, token=token)
    specs = [
        spec
        for spec in TASK_SPECS
        if include_x_signals or spec["env_var"] != "APIFY_X_TASK_ID"
    ]
    created: list[dict[str, str]] = []
    for spec in specs:
        task = _upsert_task(spec, existing_tasks, base_url=normalized_base_url, token=token)
        created.append(
            {
                "env_var": spec["env_var"],
                "task_id": task["id"],
                "task_ref": f"{task.get('username')}~{task.get('name')}",
                "name": task["name"],
                "actId": task["actId"],
            }
        )
    return created


def _request_json(
    method: str,
    path: str,
    *,
    base_url: str,
    token: str,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    url = f"{base_url}{path}"
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=60) as response:
            raw_body = response.read().decode("utf-8")
            return json.loads(raw_body) if raw_body else {}
    except HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} failed with {error.code}: {details}") from error


def _list_tasks(*, base_url: str, token: str) -> list[dict[str, Any]]:
    response = _request_json(
        "GET",
        f"/actor-tasks?{urlencode({'limit': 1000})}",
        base_url=base_url,
        token=token,
    )
    return response.get("data", {}).get("items", [])


def _delete_task(task_id: str, *, base_url: str, token: str) -> None:
    _request_json("DELETE", f"/actor-tasks/{task_id}", base_url=base_url, token=token)


def _upsert_task(
    spec: dict[str, Any],
    existing_tasks: list[dict[str, Any]],
    *,
    base_url: str,
    token: str,
) -> dict[str, Any]:
    existing = next((task for task in existing_tasks if task.get("name") == spec["name"]), None)
    payload = {
        "name": spec["name"],
        "title": spec["title"],
        "actId": spec["actId"],
        "input": spec["input"],
        "options": spec["options"],
    }
    if existing:
        existing_actor = (
            f"{existing.get('actUsername')}~{existing.get('actName')}"
            if existing.get("actUsername") and existing.get("actName")
            else None
        )
        if existing_actor and existing_actor != spec["actId"]:
            _delete_task(existing["id"], base_url=base_url, token=token)
            response = _request_json("POST", "/actor-tasks", base_url=base_url, token=token, payload=payload)
        else:
            response = _request_json(
                "PUT",
                f"/actor-tasks/{existing['id']}",
                base_url=base_url,
                token=token,
                payload=payload,
            )
    else:
        response = _request_json("POST", "/actor-tasks", base_url=base_url, token=token, payload=payload)
    return response["data"]
