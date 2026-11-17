"""
Lovart Agent OpenAPI Skill - Zero-dependency Python client.
All APIs use AK/SK HMAC-SHA256 authentication.
"""

import hashlib
import hmac
import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Optional

import os

# Pinned from lovartai/lovart-skill release v1.1.1
# (https://github.com/lovartai/lovart-skill/releases/tag/v1.1.1,
# upstream sha256 c53d7336cf7c66ea8d7f38dd18eb9c371b01e7c6745bc2a6a0cffdead4f45134).
# The upstream skill metadata declares the MIT license. TLS verification stays on.
_ssl_ctx = ssl.create_default_context()


def summarize_failures(failures: list) -> str:
    """One-line summary of rejected tool calls, for the `warning` field.

    Repeats of the same failure are collapsed with a count, since an Agent
    that retries a rejected reference three times produces three identical
    entries.
    """
    if not failures:
        return ""
    counts: dict = {}
    for f in failures:
        key = (f.get("tool_hint") or f.get("tool") or "tool",
               f.get("code") or "TOOL_FAILED",
               (f.get("message") or "").strip())
        counts[key] = counts.get(key, 0) + 1
    parts = []
    for (tool, code, msg), n in counts.items():
        times = f" (x{n})" if n > 1 else ""
        parts.append(f"{tool} was rejected{times}: [{code}] {msg}")
    head = "1 tool call was rejected. " if len(failures) == 1 else \
           f"{len(failures)} tool calls were rejected. "
    return head + " | ".join(parts)


class AgentSkillError(Exception):
    def __init__(self, message: str, code: int = 0):
        self.message = message
        self.code = code
        super().__init__(message)


# One hour. The CLI default is 180 seconds and batch passes 300. A longer wait is capped here.
MAX_CHAT_SECONDS = 3600


class AgentSkill:
    """Lovart Agent OpenAPI client."""

    def __init__(
        self,
        base_url: str,
        access_key: str,
        secret_key: str,
        timeout: int = 120,
        poll_interval: int = 3,
        path_prefix: str = "/v1/openapi",
    ):
        self.base_url = base_url.rstrip("/")
        self.access_key = access_key
        self.secret_key = secret_key
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.prefix = path_prefix


    # ── HTTP ─────────────────────────────────────────────────────────

    def _sign(self, method: str, path: str) -> dict:
        ts = str(int(time.time()))
        sig = hmac.new(
            self.secret_key.encode(),
            f"{method}\n{path}\n{ts}".encode(),
            hashlib.sha256,
        ).hexdigest()
        return {
            "X-Access-Key": self.access_key,
            "X-Timestamp": ts,
            "X-Signature": sig,
            "X-Signed-Method": method,
            "X-Signed-Path": path,
        }

    def _request(self, method: str, path: str, body=None, params=None, retries: int = None) -> dict:
        if retries is None:
            retries = 3 if method == "GET" else 1

        url = f"{self.base_url}{path}"
        if params:
            url += "?" + urllib.parse.urlencode(params)

        data = json.dumps(body).encode() if body is not None else None
        last_err = None
        idempotency_key = uuid.uuid4().hex if method == "POST" else None

        for attempt in range(retries):
            # Re-sign on each attempt (timestamp freshness)
            headers = self._sign(method, path)
            headers["Content-Type"] = "application/json"
            headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) LovartAgentSkill/1.0"
            if idempotency_key:
                headers["Idempotency-Key"] = idempotency_key
            req = urllib.request.Request(url, data=data, headers=headers, method=method)

            try:
                with urllib.request.urlopen(req, timeout=self.timeout, context=_ssl_ctx) as resp:
                    result = json.loads(resp.read().decode())
                    break
            except urllib.error.HTTPError as e:
                err = e.read().decode()
                # Retry on gateway errors (404 route mismatch, 502, 503, 429)
                if e.code in (404, 429, 502, 503) and attempt < retries - 1:
                    last_err = e
                    time.sleep(2 * (attempt + 1))
                    continue
                try:
                    d = json.loads(err)
                    msg = d.get("message", d.get("error", str(e)))
                    details = d.get("details", "")
                    if details:
                        msg = f"{msg}: {details}"
                    raise AgentSkillError(msg, e.code)
                except (json.JSONDecodeError, KeyError):
                    raise AgentSkillError(f"HTTP {e.code}: {err}", e.code)
            except (urllib.error.URLError, ssl.SSLError, ConnectionError, OSError) as e:
                last_err = e
                if attempt < retries - 1:
                    time.sleep(2 * (attempt + 1))
                    continue
                raise AgentSkillError(f"Connection failed after {retries} attempts: {e}")
        else:
            raise AgentSkillError(f"Connection failed: {last_err}")

        if isinstance(result, dict) and result.get("code", 0) != 0:
            raise AgentSkillError(result.get("message", "Unknown error"), result.get("code", -1))

        return result.get("data", result) if isinstance(result, dict) else result

    # ── Project ──────────────────────────────────────────────────────

    def save_project(self, project_id: str = "", canvas: str = "",
                     project_name: str = "", project_type: int = 3) -> dict:
        """Create (empty project_id) or replace an existing project's canvas.

        Updating replaces the whole canvas with the one given, so it needs a
        canvas; to rename a project use rename_project. An existing project
        keeps its own type, so project_type only applies on create.
        """
        if project_id and not canvas:
            raise ValueError("save_project with a project_id replaces its canvas and needs one; "
                             "use rename_project to change the name")
        body = {
            "project_id": project_id,
            "canvas": canvas,
            "project_cover_list": [],
            "pic_count": 0,
        }
        if not project_id:
            body["project_type"] = project_type
        if project_name:
            body["project_name"] = project_name
        return self._request("POST", f"{self.prefix}/project/save", body=body)

    def rename_project(self, project_id: str, name: str) -> dict:
        """Rename an existing project (server-side)."""
        return self._request("POST", f"{self.prefix}/project/save", body={
            "action": "rename",
            "project_id": project_id,
            "project_name": name,
        })

    def create_project(self, project_type: int = 3) -> str:
        """Create a new project. Returns project_id."""
        result = self.save_project(project_type=project_type)
        return result.get("project_id", "")

    # ── Mode (unlimited/fast) ───────────────────────────────────────

    def set_mode(self, unlimited: bool) -> dict:
        """Set generation mode. unlimited=True (queue, no credits), unlimited=False (fast, costs credits)."""
        return self._request("POST", f"{self.prefix}/mode/set", body={"unlimited": unlimited})

    def query_mode(self) -> dict:
        """Query current mode and available models."""
        return self._request("POST", f"{self.prefix}/mode/query", body={})

    # ── Confirm (high-cost tool) ────────────────────────────────────

    def confirm(self, thread_id: str) -> dict:
        """Confirm a high-cost tool operation (e.g. video generation in fast mode)."""
        return self._request("POST", f"{self.prefix}/chat/confirm", body={"thread_id": thread_id})

    # ── File Upload ─────────────────────────────────────────────────

    def upload_file(self, local_path: str) -> str:
        """Upload a local file via openapi proxy. Returns the CDN URL.
        The server handles OSS credentials internally — no tokens exposed.
        """
        import os
        with open(local_path, "rb") as f:
            file_data = f.read()

        filename = os.path.basename(local_path)
        boundary = uuid.uuid4().hex

        # Build multipart body
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
            f"Content-Type: application/octet-stream\r\n\r\n"
        ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()

        path = f"{self.prefix}/file/upload"
        headers = self._sign("POST", path)
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        headers["User-Agent"] = "LovartAgentSkill/1.0"

        url = f"{self.base_url}{path}"
        req = urllib.request.Request(url, data=body, method="POST", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=self.timeout, context=_ssl_ctx) as resp:
                result = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise AgentSkillError(f"Upload failed ({e.code}): {err_body}")

        if result.get("code") != 0:
            raise AgentSkillError(f"Upload failed: {result.get('message', 'unknown error')}")

        return result["data"]["url"]

    # ── Artifact ─────────────────────────────────────────────────────

    def upload_artifact(self, project_id: str, artifact_url: str, artifact_type: str = "image") -> dict:
        """Upload a link artifact. Returns {"artifact_id", "artifact_content", ...}."""
        return self._request("POST", f"{self.prefix}/artifact/upload", body={
            "project_id": project_id,
            "artifact_type": artifact_type,
            "artifact_content": artifact_url,
        })

    # ── Download ─────────────────────────────────────────────────────

    @staticmethod
    def download_artifacts(result: dict, output_dir: str = "/tmp/lovart", prefix: str = "lovart") -> list:
        """Download all artifacts from a result dict to local files.
        Idempotent: file names are derived from URL hash, and existing files are skipped.
        Returns list of {"type", "url", "local_path", "new": bool}."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        downloaded = []
        seen_urls = set()
        for item in result.get("items", []):
            for artifact in item.get("artifacts", []):
                url = artifact.get("content", "")
                atype = artifact.get("type", "unknown")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                ext = os.path.splitext(url.split("?")[0])[-1] or (
                    ".mp4" if atype == "video" else ".png"
                )
                url_hash = hashlib.sha1(url.encode()).hexdigest()[:12]
                local_path = os.path.join(output_dir, f"{prefix}_{url_hash}{ext}")
                if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                    downloaded.append({"type": atype, "url": url, "local_path": local_path, "new": False})
                    continue
                try:
                    req = urllib.request.Request(url, headers={
                        "User-Agent": "Mozilla/5.0",
                        "Referer": "https://www.lovart.ai/",
                    })
                    with urllib.request.urlopen(req, timeout=60, context=_ssl_ctx) as resp:
                        with open(local_path, "wb") as f:
                            f.write(resp.read())
                    downloaded.append({"type": atype, "url": url, "local_path": local_path, "new": True})
                except Exception:
                    downloaded.append({"type": atype, "url": url, "local_path": None, "error": "download failed", "new": False})
        return downloaded

    # ── Chat ─────────────────────────────────────────────────────────

    def send(self, prompt: str, project_id: str, attachments=None, thread_id=None,
             prefer_models=None, include_tools=None, exclude_tools=None,
             mode: Optional[str] = None, subjects=None, kits=None) -> str:
        """Send a chat message. Returns thread_id.

        prefer_models: dict mapping category to list of tool names (soft preference)
        include_tools: list of tool names the Agent is told to prioritize.
              This is a strong instruction in the prompt, not an enforced
              whitelist — the Agent may still pick another tool.
        exclude_tools: accepted for forward compatibility; it currently has
              no effect on tool selection. To steer away from a tool, name
              the one you do want via include_tools instead.
        mode: 'thinking' for deep structured reasoning, or 'fast' for
              lightweight single-pass. Default is 'fast' (matches the web
              UI). Mode is locked to the thread on the first message — to
              switch, start a new thread.
        subjects: list of already-approved asset-library subjects to use as
              references. Each entry is a dict with 'url' (required, the
              library's own URL) and optional 'type' (subject_image /
              subject_audio / subject_video, default subject_image),
              'asset_id', 'display_name', 'channel'. Passing the library URL
              reuses the asset's existing review, whereas re-uploading the
              same file creates a new copy that gets reviewed again.
        kits: list of brand kit IDs. The project's active kit is attached
              automatically, so only pass this to reference a different kit.
        """
        body = {"prompt": prompt, "project_id": project_id}
        if attachments:
            body["attachments"] = attachments
        if subjects:
            body["subjects"] = subjects
        if kits:
            body["kits"] = kits
        if thread_id:
            body["thread_id"] = thread_id
        if mode:
            body["mode"] = mode
        tc = {}
        if prefer_models:
            tc["prefer_tool_categories"] = prefer_models
        if include_tools:
            tc["include_tools"] = include_tools
        if exclude_tools:
            tc["exclude_tools"] = exclude_tools
        if tc:
            body["tool_config"] = tc
        return self._request("POST", f"{self.prefix}/chat", body=body)["thread_id"]

    def get_status(self, thread_id: str) -> dict:
        return self._request("GET", f"{self.prefix}/chat/status", params={"thread_id": thread_id})

    def get_result(self, thread_id: str) -> dict:
        return self._request("GET", f"{self.prefix}/chat/result", params={"thread_id": thread_id})

    def poll(self, thread_id: str, timeout: Optional[int] = None, verbose: bool = False) -> str:
        """Poll until done/abort/pending_confirmation. Returns final status.

        When status first becomes "done", waits a few seconds and re-checks
        to guard against a race where sub-agents (e.g. video generation)
        haven't started yet and the thread briefly appears done.

        Returns "pending_confirmation" if a high-cost tool needs user approval.
        """
        import sys
        deadline = time.time() + (timeout or self.timeout)
        confirm_delay = 5  # seconds to wait before confirming "done"
        poll_count = 0
        self._pending_confirmation = None  # reset per-call
        while time.time() < deadline:
            s = self.get_status(thread_id)
            poll_count += 1
            if verbose:
                elapsed = int(time.time() + (timeout or self.timeout) - deadline)
                print(f"[{elapsed}s] status={s['status']}", file=sys.stderr)
            if s["status"] == "abort":
                return "abort"
            if s["status"] == "done":
                time.sleep(confirm_delay)
                s2 = self.get_status(thread_id)
                if s2["status"] in ("done", "abort"):
                    # Check if there's a pending confirmation hidden in the result
                    try:
                        result = self.get_result(thread_id)
                        pc = result.get("pending_confirmation")
                        if pc:
                            self._pending_confirmation = pc
                            return "pending_confirmation"
                    except Exception:
                        pass
                    return s2["status"]
                if verbose:
                    print("[poll] sub-agent still running, continuing...", file=sys.stderr)
            # After 20s of running, periodically check for pending_confirmation
            if poll_count >= 7 and s["status"] == "running" and poll_count % 3 == 0:
                try:
                    result = self.get_result(thread_id)
                    pc = result.get("pending_confirmation")
                    if pc:
                        self._pending_confirmation = pc
                        return "pending_confirmation"
                except Exception:
                    pass
            time.sleep(self.poll_interval)
        return "timeout"

    def validate_project(self, project_id: str) -> bool:
        """Check if a project ID exists (read-only)."""
        try:
            result = self._request("GET", f"{self.prefix}/project/validate",
                                   params={"project_id": project_id})
            return result.get("valid", False)
        except AgentSkillError:
            return False

    def get_project_name(self, project_id: str) -> str:
        """Get project name. Returns empty string if not found."""
        try:
            result = self._request("GET", f"{self.prefix}/project/validate",
                                   params={"project_id": project_id})
            return result.get("project_name", "")
        except AgentSkillError:
            return ""

    def chat(self, prompt: str, project_id: Optional[str] = None,
             attachments=None, thread_id=None,
             timeout: Optional[int] = None, auto_create_project=True,
             prefer_models=None, include_tools=None, exclude_tools=None,
             mode: Optional[str] = None, subjects=None, kits=None) -> dict:
        """Send → poll → get result. One-shot convenience method.

        mode: 'thinking' for deep reasoning, 'fast' for lightweight single-pass.
              Locked to the thread after the first message.
        """
        auto_created = False
        if not project_id:
            if auto_create_project:
                project_id = self.create_project()
                auto_created = True
            else:
                raise AgentSkillError("project_id is required")
        else:
            # Validate with retry — newly created projects may need a moment to sync
            if not self.validate_project(project_id):
                time.sleep(2)
                if not self.validate_project(project_id):
                    raise AgentSkillError(f"Project '{project_id}' does not exist")

        tid = self.send(prompt=prompt, project_id=project_id,
                        attachments=attachments, thread_id=thread_id,
                        prefer_models=prefer_models,
                        include_tools=include_tools, exclude_tools=exclude_tools,
                        mode=mode, subjects=subjects, kits=kits)
        # None or a non-positive value keeps this client's timeout. Never wait past one hour.
        requested = self.timeout if timeout is None or timeout <= 0 else timeout
        status = self.poll(tid, timeout=min(int(requested), MAX_CHAT_SECONDS))

        if status == "pending_confirmation":
            pc = getattr(self, '_pending_confirmation', {})
            return {
                "thread_id": tid,
                "project_id": project_id,
                "final_status": "pending_confirmation",
                "pending_confirmation": pc,
                "items": [],
            }

        result = self.get_result(tid)
        result["final_status"] = status
        result["project_id"] = project_id

        # Detect "done but no artifact" — usually means the agent answered
        # with text (e.g. the upstream image model refused the prompt via
        # content moderation, timed out, or the LLM decided not to call any
        # tool). Surface the assistant text under a clear field so callers
        # don't silently mistake it for a successful generation.
        failures = result.get("failures") or []

        if status == "done":
            has_artifact = any(
                (it.get("artifacts") or [])
                for it in (result.get("items") or [])
            )
            if not has_artifact:
                assistant_texts = [
                    (it.get("text") or "").strip()
                    for it in (result.get("items") or [])
                    if it.get("text")
                ]
                result["generation_succeeded"] = False
                if failures:
                    result["warning"] = (
                        "Thread ended without producing any artifact. "
                        + summarize_failures(failures)
                    )
                else:
                    result["warning"] = (
                        "Thread ended without producing any artifact. The agent "
                        "responded with text only — the upstream model may have "
                        "refused the prompt (content moderation), timed out, or "
                        "the LLM chose not to call a generation tool."
                    )
                if assistant_texts:
                    result["agent_message"] = "\n\n".join(assistant_texts)
            else:
                result["generation_succeeded"] = True
                # Artifacts exist, but some tool calls were still rejected. The
                # Agent is free to drop a reference or switch models and carry
                # on, so the delivered result can quietly differ from the
                # request. Say so instead of reporting a clean success.
                if failures:
                    result["warning"] = (
                        summarize_failures(failures)
                        + " The Agent may have dropped an input or switched models "
                        "to finish, so check the result matches what you asked for."
                    )

        # Auto-name project if it's still "Untitled", empty, or looks like a truncated ID
        if project_id:
            try:
                current_name = self.get_project_name(project_id)
                needs_rename = (
                    not current_name
                    or current_name.lower() in ("untitled", "")
                    or (len(current_name) <= 12 and project_id.startswith(current_name))
                )
                if needs_rename:
                    project_name = prompt[:30].strip()
                    self.rename_project(project_id, project_name)
                    result["project_name"] = project_name
            except Exception:
                pass

        return result

