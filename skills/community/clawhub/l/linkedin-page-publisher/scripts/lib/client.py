"""LinkedIn REST API client.

A thin wrapper around `requests` that enforces the headers LinkedIn's versioned
API requires on every call:

- Authorization: Bearer <token>
- LinkedIn-Version: YYYYMM
- X-Restli-Protocol-Version: 2.0.0

Keeping this in one place means we never forget one of them, which is the
single most common cause of opaque 400s from LinkedIn.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import requests


DEFAULT_API_VERSION = "202602"  # February 2026. Bump deliberately.
API_BASE = "https://api.linkedin.com/rest"
MAX_COMMENTARY_LENGTH = 3000


class LinkedInAPIError(Exception):
    """Raised when LinkedIn returns a non-2xx response.

    The `body` attribute holds the parsed response body (dict if JSON, str
    otherwise). LinkedIn's real error signal lives in `serviceErrorCode` and
    `message` fields inside that body — check them before guessing.
    """

    def __init__(self, status: int, body: Any, url: str):
        self.status = status
        self.body = body
        self.url = url
        super().__init__(f"LinkedIn API {status} at {url}: {body}")


@dataclass
class LinkedInClient:
    """Wraps credentials and gives you `get`, `post`, and `put` helpers.

    Reads from env vars by default; override via constructor for tests or
    multi-tenant use.
    """

    access_token: str | None = None
    org_id: str | None = None
    api_version: str | None = None
    timeout: float = 60.0

    def __post_init__(self) -> None:
        self.access_token = self.access_token or os.environ.get("LINKEDIN_ACCESS_TOKEN")
        self.org_id = self.org_id or os.environ.get("LINKEDIN_ORG_ID")
        self.api_version = (
            self.api_version
            or os.environ.get("LINKEDIN_API_VERSION")
            or DEFAULT_API_VERSION
        )

        if not self.access_token:
            raise RuntimeError(
                "LINKEDIN_ACCESS_TOKEN is not set. Run scripts/get_token.py or "
                "export the token before calling this script."
            )
        if not self.org_id:
            raise RuntimeError(
                "LINKEDIN_ORG_ID is not set. Set it to the numeric organization "
                "ID of the Company Page (not the full URN)."
            )
        if not self.api_version.isdigit() or len(self.api_version) != 6:
            raise RuntimeError(
                f"LINKEDIN_API_VERSION must be YYYYMM (e.g. 202602); got {self.api_version!r}."
            )

    # --- URNs -------------------------------------------------------------

    @property
    def author_urn(self) -> str:
        """The organization URN used in the `author` field of every post."""
        return f"urn:li:organization:{self.org_id}"

    # --- Headers ----------------------------------------------------------

    def _headers(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "LinkedIn-Version": self.api_version,
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json",
        }
        if extra:
            headers.update(extra)
        return headers

    # --- Verbs ------------------------------------------------------------

    def post(self, path: str, body: dict[str, Any]) -> requests.Response:
        """POST to /rest/<path>. Returns the raw Response so callers can
        read response headers too (post IDs come back in `x-restli-id`)."""
        url = f"{API_BASE}/{path.lstrip('/')}"
        resp = requests.post(url, headers=self._headers(), json=body, timeout=self.timeout)
        self._check(resp)
        return resp

    def get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        url = f"{API_BASE}/{path.lstrip('/')}"
        resp = requests.get(url, headers=self._headers(), params=params, timeout=self.timeout)
        self._check(resp)
        return resp.json() if resp.content else {}

    def put_upload(self, upload_url: str, data: bytes, extra_headers: dict[str, str] | None = None) -> requests.Response:
        """PUT raw bytes to an upload URL returned by initializeUpload.

        These uploads do NOT use the standard LinkedIn auth headers — the URL
        itself is pre-signed. We only forward `extra_headers` (mostly used for
        multipart uploads that need specific Content-Type per part).
        """
        headers = extra_headers or {}
        resp = requests.put(upload_url, headers=headers, data=data, timeout=max(self.timeout, 300))
        # Upload URLs return a variety of 2xx codes; 200 and 201 are both fine.
        if not (200 <= resp.status_code < 300):
            raise LinkedInAPIError(resp.status_code, resp.text, upload_url)
        return resp

    # --- Error handling ---------------------------------------------------

    @staticmethod
    def _check(resp: requests.Response) -> None:
        if 200 <= resp.status_code < 300:
            return
        try:
            body: Any = resp.json()
        except ValueError:
            body = resp.text
        raise LinkedInAPIError(resp.status_code, body, resp.url)
