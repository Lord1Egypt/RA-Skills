#!/usr/bin/env python3
"""Client utilities for Moodle Web Services REST API."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass, field
from typing import Any

import requests


class MoodleAPIError(Exception):
    """Raised when Moodle returns an API-level exception."""


def _flatten_params(prefix: str, value: Any, out: dict[str, Any]) -> None:
    """Flatten dict/list params into Moodle's PHP-style query format."""
    if value is None:
        return
    if isinstance(value, dict):
        for key, child in value.items():
            child_prefix = f"{prefix}[{key}]" if prefix else str(key)
            _flatten_params(child_prefix, child, out)
        return
    if isinstance(value, list):
        for index, child in enumerate(value):
            child_prefix = f"{prefix}[{index}]"
            _flatten_params(child_prefix, child, out)
        return
    out[prefix] = value


def flatten_params(params: dict[str, Any] | None) -> dict[str, Any]:
    """Public helper to flatten nested params for Moodle API calls."""
    if not params:
        return {}
    flattened: dict[str, Any] = {}
    for key, value in params.items():
        _flatten_params(str(key), value, flattened)
    return flattened


@dataclass
class MoodleClient:
    """Small Moodle REST client with built-in rate limiting and error checks."""

    base_url: str
    token: str
    rate_limit_seconds: float = 15.0
    timeout_seconds: float = 30.0
    session: requests.Session = field(default_factory=requests.Session)

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        if not self.base_url:
            raise ValueError("base_url must not be empty")
        if not self.token:
            raise ValueError("token must not be empty")

    @classmethod
    def from_env(
        cls,
        rate_limit_seconds: float = 15.0,
        timeout_seconds: float = 30.0,
    ) -> "MoodleClient":
        base_url = os.environ.get("MOODLE_URL", "").strip()
        token = os.environ.get("MOODLE_TOKEN", "").strip()
        if not base_url:
            raise ValueError("MOODLE_URL is required")
        if not token:
            raise ValueError("MOODLE_TOKEN is required")
        return cls(
            base_url=base_url,
            token=token,
            rate_limit_seconds=rate_limit_seconds,
            timeout_seconds=timeout_seconds,
        )

    @property
    def endpoint(self) -> str:
        return f"{self.base_url}/webservice/rest/server.php"

    def call(self, function: str, params: dict[str, Any] | None = None) -> Any:
        if not function:
            raise ValueError("function is required")
        request_params: dict[str, Any] = {
            "wstoken": self.token,
            "wsfunction": function,
            "moodlewsrestformat": "json",
        }
        request_params.update(flatten_params(params))

        response = self.session.get(
            self.endpoint,
            params=request_params,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        data = response.json()

        if isinstance(data, dict) and "exception" in data:
            error_code = data.get("errorcode", "unknown_error")
            message = data.get("message", "Unknown Moodle API error")
            raise MoodleAPIError(f"{error_code}: {message}")

        if self.rate_limit_seconds > 0:
            time.sleep(self.rate_limit_seconds)

        return data

    def get_site_info(self) -> dict[str, Any]:
        data = self.call("core_webservice_get_site_info")
        if not isinstance(data, dict):
            raise MoodleAPIError("Unexpected site info response format")
        return data

    def resolve_user_id(self) -> int:
        env_value = os.environ.get("MOODLE_USER_ID", "").strip()
        if env_value:
            return int(env_value)
        site_info = self.get_site_info()
        user_id = site_info.get("userid")
        if user_id is None:
            raise MoodleAPIError("Unable to resolve user id from site info")
        return int(user_id)

    def get_courses(self, user_id: int) -> list[dict[str, Any]]:
        data = self.call("core_enrol_get_users_courses", {"userid": user_id})
        if not isinstance(data, list):
            raise MoodleAPIError("Unexpected courses response format")
        return [item for item in data if isinstance(item, dict)]

    def get_upcoming(self) -> dict[str, Any]:
        data = self.call("core_calendar_get_calendar_upcoming_view")
        if not isinstance(data, dict):
            raise MoodleAPIError("Unexpected upcoming calendar response format")
        return data

    def get_grade_overview(self, user_id: int) -> list[dict[str, Any]]:
        data = self.call("gradereport_overview_get_course_grades", {"userid": user_id})
        if not isinstance(data, list):
            raise MoodleAPIError("Unexpected grade overview response format")
        return [item for item in data if isinstance(item, dict)]

    def get_notifications(self, limit: int = 10) -> dict[str, Any]:
        data = self.call("message_popup_get_popup_notifications", {"limit": limit})
        if not isinstance(data, dict):
            raise MoodleAPIError("Unexpected notifications response format")
        return data

    def get_course_contents(self, course_id: int) -> list[dict[str, Any]]:
        data = self.call("core_course_get_contents", {"courseid": course_id})
        if not isinstance(data, list):
            raise MoodleAPIError("Unexpected course contents response format")
        return [item for item in data if isinstance(item, dict)]

