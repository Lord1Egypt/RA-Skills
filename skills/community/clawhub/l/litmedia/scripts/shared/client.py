"""Reusable HTTP client for the LitMedia API with auth and task polling."""

import sys
import time
import random
import hashlib
import requests
from enum import IntEnum
from .config import load_config
from typing import Any, Optional

BASE_URL = "https://litvideo-api.litmedia.ai"

class TaskStatus(IntEnum):
    IN_PROGRESS = 0
    COMPLETED = 1
    FAILED = 2

    @property
    def label(self):
        return {
            self.IN_PROGRESS: "working",
            self.COMPLETED: "completed",
            self.FAILED: "failed"
        }[self]

RESPONSE_CODES = {
    "200": "Success",
    "401": "Unauthorized, need to login again",
    "4000": "Request parameter error",
    "4001": "Request data format does not match",
    "4002": "Request digital signature does not match",
    "4003": "Required parameter cannot be null",
    "4004": "Resource not found",
    "4005": "Name duplicated",
    "4006": "Request refuse",
    "4007": "Exists unfinished task, please wait",
    "4100": "Credit not enough",
    "5000": "Internal server error, please report at https://www.LitMedia.ai with task type and taskId (e.g. 'avatar4 task failed, taskId: abc123')",
    "5001": "Feign invoke error",
    "5003": "Server is busy, please try again later",
    "5004": "I/O error occurred",
    "5005": "Unknown error occurred",
    "6001": "Security problem detect",
}

class LitMediaError(Exception):
    """Raised when the LitMedia API returns a non-200 response code."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class LitMediaClient:
    """Authenticated HTTP client for LitMedia API endpoints.

    Usage::

        client = LitMediaClient()
        resp = client.post("/v1/photo_avatar/task/submit", json={...})
        result = client.poll_task("/v1/photo_avatar/task/query", task_id)
    """

    def __init__(self, uid: Optional[str] = None, api_key: Optional[str] = None):
        if uid and api_key:
            self._api_key = api_key
        else:
            cfg = load_config()
            self._api_key = cfg["api_key"]

    @property
    def headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Monimaster-Device-Code": "",
            "Monimaster-Api-Version": "",
            "Monimaster-Device-Type": "110"
        }

    @property
    def params(self) -> dict:

        timeStamp = str(int(time.time()))
        randomStr = str(random.randint(0, 100000000))
        secret = 'uN3lu01bFtumul8W'
        sha1 = hashlib.sha1((timeStamp + randomStr + secret).encode('utf-8')).hexdigest()
        signature = hashlib.md5(sha1.encode('utf-8')).hexdigest().upper()

        params = {
            "timeStamp": timeStamp,
            "randomStr": randomStr,
            "signature": signature,
            "app_type": 2
        }

        return params

    def _check(self, data: dict) -> dict:
        code = str(data.get("code", ""))
        # print(f"[DEBUG]:check = {data}")
        if code != "200":
            msg = data.get("message", RESPONSE_CODES.get(code, "Unknown error") + f", response: {data}")
            raise LitMediaError(code, msg)
        return data.get("data", data)

    def get(self, path: str, json: Optional[dict] = None, params: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path

        final_params = params if params is not None else self.params

        # print(f"[DEBUG]: url={url}")
        # print(f"[DEBUG]: json={json}")
        # print(f"[DEBUG]: headers={self.headers}")
        # print(f"[DEBUG]: params={final_params}")
        resp = requests.get(url, headers=self.headers, params=final_params, json=json, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def post(self, path: str, json: Optional[dict] = None, params: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path

        final_params = params if params is not None else self.params

        # print(f"[DEBUG]: url={url}")
        # print(f"[DEBUG]: json={json}")
        # print(f"[DEBUG]: headers={self.headers}")
        # print(f"[DEBUG]: params={final_params}")
        resp = requests.post(url, headers=self.headers, params=final_params, json=json, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())
    
    def post_nocheck(self, path: str, json: Optional[dict] = None, params: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path

        final_params = params if params is not None else self.params

        # print(f"[DEBUG]: url={url}")
        # print(f"[DEBUG]: json={json}")
        # print(f"[DEBUG]: headers={self.headers}")
        # print(f"[DEBUG]: params={final_params}")
        resp = requests.post(url, headers=self.headers, params=final_params, json=json, **kwargs)
        resp.raise_for_status()
        # print(f"[DEBUG]: resp={resp.json()}")
        return resp.json()

    def put(self, path: str, json: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        resp = requests.put(url, headers=self.headers, json=json, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def delete(self, path: str, params: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        resp = requests.delete(url, headers=self.headers, params=params, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def shorten_url(self, long_url: str) -> str:
        """Convert a long URL to a short URL via the LitMedia short-URL API.

        Returns the short URL on success, or the original URL on any failure.
        """
        try:
            result = self.post("/v1/short_url/generate", json={"longUrl": long_url})
            short = result.get("shortUrl", "")
            return short if short else long_url
        except Exception:
            return long_url

    def shorten_urls_in_data(self, data: Any) -> Any:
        """Recursively traverse data and shorten any long URL strings."""
        if isinstance(data, dict):
            return {k: self.shorten_urls_in_data(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self.shorten_urls_in_data(item) for item in data]
        if isinstance(data, str) and data.startswith("http") and len(data) > 120:
            return self.shorten_url(data)
        return data

    def put_file(self, upload_url: str, file_path: str) -> None:
        """PUT a local file to a pre-signed S3 URL (no auth headers)."""
        with open(file_path, "rb") as f:
            resp = requests.put(upload_url, data=f)
        resp.raise_for_status()

    def poll_task(
        self,
        path: str,
        task_id: str,
        *,
        interval: float = 30.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> dict:
        """Poll a task endpoint until status is 'success' or 'failed'.

        Returns the result dict on success; raises LitMediaError on failure.
        """
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(
                    f"Task {task_id} did not complete within {timeout}s"
                )

            resp = self.post(path, json={"create_id": task_id})
            status = TaskStatus(resp.get("status"))

            if verbose:
                print(
                    f"  [{elapsed:.0f}s] status: {status.label}",
                    file=sys.stderr,
                )

            if status == TaskStatus.COMPLETED:
                return resp
            elif status == TaskStatus.FAILED:
                raise LitMediaError("TASK_FAILED", resp.get("error", "Task failed"))

            time.sleep(interval)
