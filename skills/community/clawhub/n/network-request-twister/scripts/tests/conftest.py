"""Shared test fixtures and helpers."""

from __future__ import annotations

import json

import pytest

SAMPLE_CONFIG = {
    "id": "test-001",
    "name": "test config",
    "version": "1.0",
    "rules": [
        {
            "id": "rule-001",
            "name": "block analytics",
            "enabled": True,
            "priority": 10,
            "stage": "request",
            "match": {
                "allOf": [
                    {"type": "urlContains", "value": "analytics"},
                ],
            },
            "actions": [
                {"type": "block", "statusCode": 204},
            ],
        },
    ],
}


@pytest.fixture
def sample_config_json() -> bytes:
    return json.dumps(SAMPLE_CONFIG).encode("utf-8")


def make_fetch_event(
    url: str = "https://example.com/api",
    method: str = "GET",
    headers: dict[str, str] | None = None,
    resource_type: str = "XHR",
    response_status: int | None = None,
    post_data: str | None = None,
    has_post_data: bool = False,
) -> dict:
    """Build a minimal Fetch.requestPaused event dict."""
    ev: dict = {
        "requestId": "req-001",
        "request": {
            "url": url,
            "method": method,
            "headers": headers or {},
        },
        "resourceType": resource_type,
    }
    if response_status is not None:
        ev["responseStatusCode"] = response_status
        ev["responseHeaders"] = [
            {"name": "Content-Type", "value": "application/json"},
        ]
    if post_data is not None or has_post_data:
        ev["request"]["hasPostData"] = True
        if post_data:
            ev["request"]["postData"] = post_data
    return ev
