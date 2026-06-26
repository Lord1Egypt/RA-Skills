"""Smoke-test cloud function. Echoes back a greeting."""
from typing import Any


def hello_world(body: dict[str, Any]) -> dict[str, Any]:
    name = (body or {}).get("name", "world")
    return {"greeting": f"hello, {name}"}
