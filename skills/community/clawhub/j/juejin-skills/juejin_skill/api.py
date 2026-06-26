"""Low-level HTTP wrapper for the Juejin API."""

from __future__ import annotations

import httpx
from typing import Any

from juejin_skill.config import DEFAULT_HEADERS


class JuejinAPI:
    """Thin HTTP client that talks to the Juejin REST API.

    All public methods return the parsed JSON body (``dict``).
    Raises ``httpx.HTTPStatusError`` on non-2xx responses.
    """

    def __init__(self, cookie: str = "", timeout: float = 30.0) -> None:
        self._cookie = cookie
        self._timeout = timeout

    # ------------------------------------------------------------------ #
    #  Internal helpers
    # ------------------------------------------------------------------ #

    def _build_headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {**DEFAULT_HEADERS}
        if self._cookie:
            headers["Cookie"] = self._cookie
        if extra:
            headers.update(extra)
        return headers

    def _request(
        self,
        method: str,
        url: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        with httpx.Client(timeout=self._timeout) as client:
            resp = client.request(
                method,
                url,
                headers=self._build_headers(extra_headers),
                json=json_body,
                params=params,
            )
            resp.raise_for_status()
            return resp.json()

    # ------------------------------------------------------------------ #
    #  Public convenience methods
    # ------------------------------------------------------------------ #

    def get(self, url: str, **kwargs: Any) -> dict[str, Any]:
        """Send a GET request and return JSON."""
        return self._request("GET", url, **kwargs)

    def post(self, url: str, json_body: dict[str, Any] | None = None, **kwargs: Any) -> dict[str, Any]:
        """Send a POST request and return JSON."""
        return self._request("POST", url, json_body=json_body, **kwargs)

    @property
    def cookie(self) -> str:
        return self._cookie

    @cookie.setter
    def cookie(self, value: str) -> None:
        self._cookie = value

    def is_authenticated(self) -> bool:
        """Return ``True`` if the current cookie is still valid."""
        if not self._cookie:
            return False
        try:
            data = self.get("https://api.juejin.cn/user_api/v1/user/get")
            return data.get("err_no") == 0 and data.get("data") is not None
        except Exception:
            return False
