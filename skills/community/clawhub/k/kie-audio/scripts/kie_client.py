"""Shared Kie.ai HTTP client used by all kie-* skills.

Public surface:
    KieClient(api_key=None)
        .create_task(endpoint, payload, callback_url=None) -> str  # taskId
        .get_task(task_id, endpoint="/api/v1/jobs/recordInfo") -> dict
        .poll_task(task_id, endpoint=..., timeout=900) -> dict     # resultJson on success
        .wait_for_webhook(port, timeout=900, verify_hmac=True) -> dict
        .get_credits() -> int
        .download(url, out_path) -> Path
        .request(method, path, **kwargs) -> dict

Errors:
    KieError            — base class
    KieAuthError        — 401
    KieCreditsError     — 402
    KieRateLimitError   — 429
    KieValidationError  — 4xx with msg surfaced verbatim
    KieTaskFailed       — task state == fail
    KieTimeout          — polling / webhook exceeded --timeout

Env vars read lazily:
    KIE_API_KEY          — required
    KIE_WEBHOOK_HMAC_KEY — only when wait_for_webhook(verify_hmac=True)

Stdlib only. No requests/httpx dependency so skills stay zero-install.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any


def _load_openclaw_global_env() -> None:
    """Auto-load globalEnv from ~/.openclaw/openclaw.json on import.

    OpenClaw skills don't inherit the user's shell env by default. Users put
    KIE_API_KEY (and similar) under "globalEnv" in openclaw.json and expect
    every skill to pick it up automatically. Existing env vars always win —
    this only fills in what's missing.
    """
    try:
        cfg_path = Path.home() / ".openclaw" / "openclaw.json"
        if not cfg_path.is_file():
            return
        with open(cfg_path, encoding="utf-8") as f:
            cfg = json.load(f)
        global_env = cfg.get("globalEnv") or {}
        if not isinstance(global_env, dict):
            return
        for key, value in global_env.items():
            if key not in os.environ and value is not None:
                os.environ[key] = str(value)
    except (OSError, ValueError):
        # Silently ignore — skill will fail later with a clear KIE_API_KEY error
        # if the key really is missing.
        pass


_load_openclaw_global_env()


BASE_URL = "https://api.kie.ai"
DEFAULT_POLL_ENDPOINT = "/api/v1/jobs/recordInfo"
DEFAULT_TIMEOUT = 900  # 15 minutes
POLL_INITIAL_DELAY = 3.0
POLL_MAX_DELAY = 30.0
POLL_BACKOFF = 1.5


class KieError(Exception):
    pass


class KieAuthError(KieError):
    pass


class KieCreditsError(KieError):
    pass


class KieRateLimitError(KieError):
    pass


class KieValidationError(KieError):
    pass


class KieTaskFailed(KieError):
    def __init__(self, task_id: str, fail_code: Any, fail_msg: str):
        self.task_id = task_id
        self.fail_code = fail_code
        self.fail_msg = fail_msg
        super().__init__(f"task {task_id} failed (code={fail_code}): {fail_msg}")


class KieTimeout(KieError):
    pass


class KieClient:
    def __init__(self, api_key: str | None = None, base_url: str = BASE_URL):
        self.api_key = api_key or os.environ.get("KIE_API_KEY")
        if not self.api_key:
            raise KieAuthError(
                "KIE_API_KEY environment variable is not set. "
                "Get a key at https://kie.ai/api-key and export it before running."
            )
        self.base_url = base_url.rstrip("/")

    # ---------------- low-level request ----------------

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict | None = None,
        query: dict | None = None,
        extra_headers: dict | None = None,
        timeout: float = 60.0,
    ) -> dict:
        url = self.base_url + path
        if query:
            url += "?" + urllib.parse.urlencode(query)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        data: bytes | None = None
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)

        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body_text = e.read().decode("utf-8", errors="replace")
            self._raise_for_status(e.code, body_text)
            raise  # unreachable
        except urllib.error.URLError as e:
            raise KieError(f"network error talking to {url}: {e}") from e

        if not body:
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError as e:
            raise KieError(f"non-JSON response from {url}: {body[:200]}") from e

    @staticmethod
    def _raise_for_status(status: int, body_text: str) -> None:
        try:
            body = json.loads(body_text)
            msg = body.get("msg") or body.get("message") or body_text
        except Exception:
            msg = body_text
        if status == 401:
            raise KieAuthError(f"401 unauthorized — check KIE_API_KEY. {msg}")
        if status == 402:
            raise KieCreditsError(
                f"402 insufficient credits — top up at https://kie.ai/dashboard. {msg}"
            )
        if status == 429:
            raise KieRateLimitError(f"429 rate limited. {msg}")
        if 400 <= status < 500:
            raise KieValidationError(f"{status}: {msg}")
        raise KieError(f"{status}: {msg}")

    # ---------------- task helpers ----------------

    def create_task(
        self,
        endpoint: str,
        payload: dict,
        callback_url: str | None = None,
    ) -> str:
        """POST a task creation request. Returns the taskId."""
        body = dict(payload)
        if callback_url:
            body.setdefault("callBackUrl", callback_url)
        resp = self.request("POST", endpoint, json_body=body)
        code = resp.get("code")
        if code not in (200, None):
            raise KieError(f"task creation returned code={code}: {resp.get('msg')}")
        data = resp.get("data") or {}
        task_id = data.get("taskId") if isinstance(data, dict) else None
        if not task_id:
            raise KieError(f"no taskId in response: {resp}")
        return task_id

    def get_task(self, task_id: str, endpoint: str = DEFAULT_POLL_ENDPOINT) -> dict:
        return self.request("GET", endpoint, query={"taskId": task_id})

    def poll_task(
        self,
        task_id: str,
        endpoint: str = DEFAULT_POLL_ENDPOINT,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        initial_delay: float = POLL_INITIAL_DELAY,
        max_delay: float = POLL_MAX_DELAY,
        backoff: float = POLL_BACKOFF,
        on_progress=None,
    ) -> dict:
        """Poll until the task reaches a terminal state.

        Returns the parsed `data` block on success. Raises KieTaskFailed / KieTimeout.
        Works for both the generic `/api/v1/jobs/recordInfo` endpoint (uses `state`)
        and the model-specific endpoints that use `successFlag` / numeric statuses.
        """
        start = time.monotonic()
        delay = initial_delay
        last_state = None
        while True:
            resp = self.get_task(task_id, endpoint=endpoint)
            data = resp.get("data") or {}
            if not isinstance(data, dict):
                raise KieError(f"unexpected task payload: {resp}")

            state = self._extract_state(data)
            if on_progress and state != last_state:
                on_progress(state, data)
                last_state = state

            if self._is_success(state):
                return data
            if self._is_failure(state):
                raise KieTaskFailed(
                    task_id,
                    data.get("failCode") or data.get("errorCode"),
                    data.get("failMsg") or data.get("errorMessage") or resp.get("msg") or "unknown",
                )

            if time.monotonic() - start > timeout:
                raise KieTimeout(
                    f"task {task_id} did not finish within {timeout:.0f}s (last state={state})"
                )
            time.sleep(delay)
            delay = min(delay * backoff, max_delay)

    @staticmethod
    def _extract_state(data: dict) -> str:
        """Normalize task state across Kie's different response shapes."""
        # Generic endpoint: "state": "waiting|queuing|generating|success|fail"
        if "state" in data and isinstance(data["state"], str):
            return data["state"].lower()
        # Suno / some others: "status": string
        if "status" in data and isinstance(data["status"], str):
            return data["status"].upper()
        # Model-specific numeric successFlag: 0=processing 1=success 2/3=fail
        if "successFlag" in data:
            sf = data["successFlag"]
            if sf in (0, "0"):
                return "generating"
            if sf in (1, "1"):
                return "success"
            return "fail"
        return "unknown"

    @staticmethod
    def _is_success(state: str) -> bool:
        return state in {"success", "SUCCESS", "COMPLETE", "complete"}

    @staticmethod
    def _is_failure(state: str) -> bool:
        return state in {
            "fail",
            "failed",
            "FAIL",
            "FAILED",
            "CREATE_TASK_FAILED",
            "GENERATE_AUDIO_FAILED",
            "SENSITIVE_WORD_ERROR",
            "error",
            "ERROR",
        }

    # ---------------- webhook server ----------------

    def wait_for_webhook(
        self,
        port: int,
        *,
        timeout: float = DEFAULT_TIMEOUT,
        verify_hmac: bool = True,
        expected_task_id: str | None = None,
    ) -> dict:
        """Spin up a local HTTP server on 127.0.0.1:<port>, wait for one POST, return its JSON body.

        HMAC verification uses KIE_WEBHOOK_HMAC_KEY env var and headers
        X-Webhook-Timestamp / X-Webhook-Signature per Kie's spec.
        """
        hmac_key = os.environ.get("KIE_WEBHOOK_HMAC_KEY") if verify_hmac else None
        if verify_hmac and not hmac_key:
            raise KieError(
                "verify_hmac=True but KIE_WEBHOOK_HMAC_KEY is not set. "
                "Grab it from your Kie dashboard settings page or pass verify_hmac=False."
            )

        received: dict = {}

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):  # silence access log
                pass

            def do_POST(self):
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length)
                try:
                    body = json.loads(raw.decode("utf-8"))
                except Exception:
                    self.send_response(400)
                    self.end_headers()
                    return

                if verify_hmac:
                    ts = self.headers.get("X-Webhook-Timestamp", "")
                    sig = self.headers.get("X-Webhook-Signature", "")
                    task_id = (body.get("data") or {}).get("taskId") or body.get("taskId") or ""
                    msg = f"{task_id}.{ts}".encode("utf-8")
                    expected = base64.b64encode(
                        hmac.new(hmac_key.encode("utf-8"), msg, hashlib.sha256).digest()
                    ).decode("ascii")
                    if not hmac.compare_digest(expected, sig):
                        self.send_response(401)
                        self.end_headers()
                        return

                if expected_task_id:
                    body_task_id = (body.get("data") or {}).get("taskId") or body.get("taskId")
                    if body_task_id and body_task_id != expected_task_id:
                        self.send_response(200)
                        self.end_headers()
                        return

                received.update(body)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')

        server = HTTPServer(("127.0.0.1", port), Handler)
        server.timeout = 1.0
        start = time.monotonic()
        try:
            while not received:
                server.handle_request()
                if time.monotonic() - start > timeout:
                    raise KieTimeout(f"no webhook received within {timeout:.0f}s")
        finally:
            server.server_close()
        return received

    # ---------------- misc helpers ----------------

    def get_credits(self) -> int:
        resp = self.request("GET", "/api/v1/chat/credit")
        data = resp.get("data")
        if isinstance(data, dict):
            return int(data.get("credit") or data.get("credits") or 0)
        return int(data or 0)

    def download(self, url: str, out_path: str | Path) -> Path:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "kie-skills/1.0"})
        with urllib.request.urlopen(req, timeout=120) as resp, open(out, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
        return out


# ---------------- CLI sanity check ----------------

def _main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Kie.ai shared client sanity check")
    p.add_argument("--check-credits", action="store_true", help="print remaining credits and exit")
    p.add_argument("--get-task", metavar="TASK_ID", help="fetch a task status by id")
    p.add_argument(
        "--endpoint",
        default=DEFAULT_POLL_ENDPOINT,
        help="task status endpoint (default %(default)s)",
    )
    args = p.parse_args(argv)

    try:
        client = KieClient()
    except KieAuthError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if args.check_credits:
        credits = client.get_credits()
        print(f"Kie.ai credits remaining: {credits}")
        return 0
    if args.get_task:
        info = client.get_task(args.get_task, endpoint=args.endpoint)
        print(json.dumps(info, indent=2))
        return 0

    p.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
