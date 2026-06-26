#!/usr/bin/env python3
"""
Manus API Session Tracker

Manages multi-turn conversations with the Manus AI agent API.
Prevents accidental task duplication by tracking task IDs per session
in a local JSON registry with active/archived separation.

Requires: export MANUS_API_KEY="your-api-key"

Usage as library:
    from manus_session import ManusSession
    s = ManusSession()
    s.send("Analyze this code", session_name="review", tags=["code"])
    s.send("Now check for bugs", session_name="review")
    matches = s.search("code")
    s.poll_until_done("review")

Usage as CLI:
    python manus_session.py send "Analyze this" -s review --tags code,security
    python manus_session.py search "auth"
    python manus_session.py sessions [--archived]
    python manus_session.py status -s review
    python manus_session.py poll -s review
    python manus_session.py unarchive -s old-review
    python manus_session.py import-task TASK_ID --name imported
    python manus_session.py upload file.pdf
    python manus_session.py create-project "Name" --instruction "..."
    python manus_session.py projects
    python manus_session.py cleanup
"""

import json
import os
import sys
import tempfile
import time
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: 'requests' required. Install: pip install requests", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.manus.ai"
DEFAULT_SESSION_FILE = ".manus_sessions.json"
DEFAULT_AGENT_PROFILE = "manus-1.6"
EMPTY_REGISTRY = {"active": {}, "archived": {}}


def _resolve_api_key(api_key: Optional[str] = None) -> str:
    """Resolve API key: explicit arg > MANUS_API_KEY environment variable."""
    if api_key:
        return api_key
    from_env = os.environ.get("MANUS_API_KEY")
    if from_env:
        return from_env
    raise ValueError(
        "API key not found. Set it with: export MANUS_API_KEY=\"your-api-key\""
    )


class ManusSession:
    """Manages Manus API sessions with automatic task ID tracking and archival."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        session_file: str = DEFAULT_SESSION_FILE,
    ):
        self.api_key = _resolve_api_key(api_key)
        self.session_file = Path(session_file)
        self._registry = self._load_registry()

    @property
    def _headers(self) -> dict:
        return {
            "API_KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # ── Registry I/O ─────────────────────────────────────────────────

    def _load_registry(self) -> dict:
        if self.session_file.exists():
            try:
                data = json.loads(self.session_file.read_text())
                if "active" not in data and "archived" not in data:
                    return {"active": data, "archived": {}}
                data.setdefault("active", {})
                data.setdefault("archived", {})
                return data
            except (json.JSONDecodeError, OSError):
                return dict(EMPTY_REGISTRY)
        return dict(EMPTY_REGISTRY)

    def _save_registry(self):
        """Atomic write: temp file then rename to prevent corruption."""
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(
                dir=str(self.session_file.parent or "."), suffix=".tmp"
            )
            with os.fdopen(fd, "w") as f:
                json.dump(self._registry, f, indent=2)
            os.replace(tmp, str(self.session_file))
        except Exception:
            if tmp and os.path.exists(tmp):
                os.unlink(tmp)
            raise

    # ── Session lookup ───────────────────────────────────────────────

    def get_entry(self, session_name: str) -> Optional[dict]:
        """Get a session entry from active or archived. Returns None if not found."""
        entry = self._registry["active"].get(session_name)
        if entry:
            return {**entry, "_section": "active"}
        entry = self._registry["archived"].get(session_name)
        if entry:
            return {**entry, "_section": "archived"}
        return None

    def get_task_id(self, session_name: str) -> Optional[str]:
        """Get the task ID for a named session."""
        entry = self.get_entry(session_name)
        return entry.get("task_id") if entry else None

    def list_sessions(self, include_archived: bool = False) -> dict:
        """Return active sessions. Optionally include archived."""
        result = {"active": dict(self._registry["active"])}
        if include_archived:
            result["archived"] = dict(self._registry["archived"])
        return result

    def search(self, query: str) -> list:
        """
        Search all sessions (active + archived) by keyword.
        Returns matches sorted by relevance score (highest first).
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        query_terms = query_lower.split()
        results = []

        for section in ("active", "archived"):
            for name, entry in self._registry[section].items():
                score = 0.0

                if query_lower == name.lower():
                    score += 100
                elif query_lower in name.lower():
                    score += 50

                if query_lower == entry.get("task_id", "").lower():
                    score += 100

                tags = [t.lower() for t in entry.get("tags", [])]
                score += sum(
                    20 for term in query_terms if any(term in tag for tag in tags)
                )

                desc = entry.get("description", "").lower()
                if any(term in desc for term in query_terms):
                    score += 15

                for field in ("first_prompt", "last_prompt"):
                    val = entry.get(field, "").lower()
                    if any(term in val for term in query_terms):
                        score += 10

                title = entry.get("task_title", "").lower()
                if any(term in title for term in query_terms):
                    score += 10

                proj = entry.get("project_name", "").lower()
                if any(term in proj for term in query_terms):
                    score += 10

                age_days = (time.time() - entry.get("last_used", 0)) / 86400
                score += max(0, 10 - age_days)

                if score > 0:
                    results.append(
                        {"name": name, "section": section, "score": round(score, 1), **entry}
                    )

        return sorted(results, key=lambda x: x["score"], reverse=True)

    # ── Archival ─────────────────────────────────────────────────────

    def archive(self, session_name: str, reason: str = "completed"):
        """Move a session from active to archived."""
        entry = self._registry["active"].pop(session_name, None)
        if entry:
            entry["archived_at"] = int(time.time())
            entry["archived_reason"] = reason
            self._registry["archived"][session_name] = entry
            self._save_registry()

    def unarchive(self, session_name: str):
        """Move a session from archived back to active."""
        entry = self._registry["archived"].pop(session_name, None)
        if entry:
            entry.pop("archived_at", None)
            entry.pop("archived_reason", None)
            self._registry["active"][session_name] = entry
            self._save_registry()

    def _maybe_archive(self, session_name: str, status: str):
        """Auto-archive if status is completed or failed."""
        if status in ("completed", "failed") and session_name in self._registry["active"]:
            self.archive(session_name, reason=status)

    # ── Core API: send ───────────────────────────────────────────────

    def send(
        self,
        prompt: str,
        session_name: str = "default",
        agent_profile: str = DEFAULT_AGENT_PROFILE,
        task_mode: Optional[str] = None,
        project_id: Optional[str] = None,
        project_name: Optional[str] = None,
        attachments: Optional[list] = None,
        connectors: Optional[list] = None,
        tags: Optional[list] = None,
        description: Optional[str] = None,
        interactive_mode: bool = False,
        hide_in_task_list: bool = False,
        create_shareable_link: bool = False,
        locale: Optional[str] = None,
    ) -> dict:
        """
        Send a prompt to Manus. Automatically continues existing sessions.
        Creates a new task only if no session with this name exists.
        """
        existing = self.get_entry(session_name)
        existing_task_id = None

        if existing:
            existing_task_id = existing.get("task_id")
            if existing.get("_section") == "archived":
                self.unarchive(session_name)

        body = {"prompt": prompt, "agentProfile": agent_profile}
        if existing_task_id:
            body["taskId"] = existing_task_id
        if task_mode:
            body["taskMode"] = task_mode
        if project_id:
            body["projectId"] = project_id
        if attachments:
            body["attachments"] = attachments
        if connectors:
            body["connectors"] = connectors
        if interactive_mode:
            body["interactiveMode"] = True
        if hide_in_task_list:
            body["hideInTaskList"] = True
        if create_shareable_link:
            body["createShareableLink"] = True
        if locale:
            body["locale"] = locale

        resp = requests.post(f"{BASE_URL}/v1/tasks", headers=self._headers, json=body)
        resp.raise_for_status()
        data = resp.json()

        task_id = data.get("task_id") or existing_task_id
        if task_id:
            prev = self._registry["active"].get(session_name, {})
            self._registry["active"][session_name] = {
                "task_id": task_id,
                "task_title": data.get("task_title") or prev.get("task_title", ""),
                "task_url": data.get("task_url") or prev.get("task_url", ""),
                "description": description or prev.get("description", ""),
                "tags": tags or prev.get("tags", []),
                "project_id": project_id or prev.get("project_id"),
                "project_name": project_name or prev.get("project_name"),
                "agent_profile": agent_profile,
                "task_mode": task_mode or prev.get("task_mode"),
                "created_at": prev.get("created_at", int(time.time())),
                "last_used": int(time.time()),
                "last_status": "running",
                "turn_count": prev.get("turn_count", 0) + 1,
                "first_prompt": prev.get("first_prompt", prompt),
                "last_prompt": prompt,
            }
            self._save_registry()

        return data

    # ── Core API: get / poll ─────────────────────────────────────────

    def get_task(self, task_id: str, convert: Optional[str] = None) -> dict:
        params = {"convert": convert} if convert else {}
        resp = requests.get(
            f"{BASE_URL}/v1/tasks/{task_id}", headers=self._headers, params=params
        )
        resp.raise_for_status()
        return resp.json()

    def get_session_task(self, session_name: str) -> Optional[dict]:
        """Get full task details for a named session. Cleans up 404s."""
        task_id = self.get_task_id(session_name)
        if not task_id:
            return None
        try:
            task = self.get_task(task_id)
        except requests.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                self._registry["active"].pop(session_name, None)
                self._registry["archived"].pop(session_name, None)
                self._save_registry()
                return None
            raise
        status = task.get("status")
        for section in ("active", "archived"):
            if session_name in self._registry[section]:
                self._registry[section][session_name]["last_status"] = status
                self._save_registry()
                if status in ("completed", "failed") and section == "active":
                    self._maybe_archive(session_name, status)
                break
        return task

    def poll_until_done(
        self,
        session_name: str,
        timeout: int = 600,
        initial_delay: float = 2.0,
        max_delay: float = 30.0,
        verbose: bool = True,
    ) -> dict:
        """
        Poll until completed, failed, or pending. Auto-archives on completion.
        """
        task_id = self.get_task_id(session_name)
        if not task_id:
            raise ValueError(f"No task found for session '{session_name}'")

        start = time.time()
        delay = initial_delay

        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")

            task = self.get_task(task_id)
            status = task.get("status", "unknown")
            credits_used = task.get("credit_usage", "?")

            if verbose:
                print(f"  [{elapsed:.0f}s] status={status} credits={credits_used}", file=sys.stderr)

            if status in ("completed", "failed"):
                if session_name in self._registry["active"]:
                    self._registry["active"][session_name]["last_status"] = status
                    self._save_registry()
                    self._maybe_archive(session_name, status)
                return task
            elif status == "pending":
                if session_name in self._registry["active"]:
                    self._registry["active"][session_name]["last_status"] = status
                    self._save_registry()
                return task
            else:
                time.sleep(delay)
                delay = min(delay * 1.5, max_delay)

    # ── Task management ──────────────────────────────────────────────

    def list_tasks(self, limit: int = 100, status: Optional[list] = None,
                   query: Optional[str] = None, project_id: Optional[str] = None,
                   order: str = "desc", order_by: str = "created_at",
                   created_after: Optional[int] = None,
                   created_before: Optional[int] = None) -> dict:
        params = {"limit": limit, "order": order, "orderBy": order_by}
        if status:
            params["status"] = status
        if query:
            params["query"] = query
        if project_id:
            params["project_id"] = project_id
        if created_after:
            params["createdAfter"] = created_after
        if created_before:
            params["createdBefore"] = created_before
        resp = requests.get(f"{BASE_URL}/v1/tasks", headers=self._headers, params=params)
        resp.raise_for_status()
        return resp.json()

    def update_task(self, task_id: str, title: Optional[str] = None,
                    enable_shared: Optional[bool] = None,
                    enable_visible: Optional[bool] = None) -> dict:
        body = {}
        if title is not None:
            body["title"] = title
        if enable_shared is not None:
            body["enable_shared"] = enable_shared
        if enable_visible is not None:
            body["enable_visible_in_task_list"] = enable_visible
        resp = requests.put(f"{BASE_URL}/v1/tasks/{task_id}", headers=self._headers, json=body)
        resp.raise_for_status()
        return resp.json()

    def delete_task(self, task_id: str) -> dict:
        resp = requests.delete(f"{BASE_URL}/v1/tasks/{task_id}", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── Projects ─────────────────────────────────────────────────────

    def create_project(self, name: str, instruction: Optional[str] = None) -> dict:
        body = {"name": name}
        if instruction:
            body["instruction"] = instruction
        resp = requests.post(f"{BASE_URL}/v1/projects", headers=self._headers, json=body)
        resp.raise_for_status()
        return resp.json()

    def list_projects(self, limit: int = 100) -> dict:
        resp = requests.get(
            f"{BASE_URL}/v1/projects", headers=self._headers, params={"limit": limit}
        )
        resp.raise_for_status()
        return resp.json()

    # ── Files ────────────────────────────────────────────────────────

    def upload_file(self, filepath: str) -> dict:
        """Two-step upload: create record then PUT to presigned URL."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        resp = requests.post(
            f"{BASE_URL}/v1/files", headers=self._headers, json={"filename": path.name}
        )
        resp.raise_for_status()
        record = resp.json()
        upload_url = record.get("upload_url")
        if not upload_url:
            raise RuntimeError("No upload_url returned")
        import mimetypes
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        with open(path, "rb") as f:
            requests.put(upload_url, headers={"Content-Type": mime}, data=f).raise_for_status()
        return record

    def list_files(self) -> dict:
        resp = requests.get(f"{BASE_URL}/v1/files", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    def get_file(self, file_id: str) -> dict:
        resp = requests.get(f"{BASE_URL}/v1/files/{file_id}", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    def delete_file(self, file_id: str) -> dict:
        resp = requests.delete(f"{BASE_URL}/v1/files/{file_id}", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    # ── Webhooks ─────────────────────────────────────────────────────

    def create_webhook(self, url: str) -> dict:
        resp = requests.post(
            f"{BASE_URL}/v1/webhooks", headers=self._headers, json={"url": url}
        )
        resp.raise_for_status()
        return resp.json()

    def delete_webhook(self, webhook_id: str) -> dict:
        resp = requests.delete(
            f"{BASE_URL}/v1/webhooks/{webhook_id}", headers=self._headers
        )
        resp.raise_for_status()
        return resp.json()

    # ── Import orphaned tasks ────────────────────────────────────────

    def import_task(self, task_id: str, session_name: str,
                    tags: Optional[list] = None, description: Optional[str] = None):
        """Import an existing Manus task into the session registry."""
        task = self.get_task(task_id)
        status = task.get("status", "unknown")
        meta = task.get("metadata", {})
        section = "archived" if status in ("completed", "failed") else "active"
        entry = {
            "task_id": task_id,
            "task_title": meta.get("task_title", ""),
            "task_url": meta.get("task_url", ""),
            "description": description or "",
            "tags": tags or [],
            "project_id": None,
            "project_name": None,
            "agent_profile": task.get("model", "unknown"),
            "task_mode": None,
            "created_at": task.get("created_at", int(time.time())),
            "last_used": task.get("updated_at", int(time.time())),
            "last_status": status,
            "turn_count": len(task.get("output", [])),
            "first_prompt": "",
            "last_prompt": "",
        }
        if section == "archived":
            entry["archived_at"] = int(time.time())
            entry["archived_reason"] = status
        self._registry[section][session_name] = entry
        self._save_registry()
        return entry


# ── CLI ──────────────────────────────────────────────────────────────

def _format_age(ts: int) -> str:
    if not ts:
        return "never"
    delta = time.time() - ts
    if delta < 60:
        return "just now"
    elif delta < 3600:
        return f"{int(delta / 60)}m ago"
    elif delta < 86400:
        return f"{int(delta / 3600)}h ago"
    else:
        return f"{int(delta / 86400)}d ago"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Manus API Session Manager")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("send", help="Send a prompt (new or continue session)")
    p.add_argument("prompt")
    p.add_argument("-s", "--session", default="default")
    p.add_argument("--profile", default="manus-1.6")
    p.add_argument("--mode", default=None, help="chat|adaptive|agent")
    p.add_argument("--project", default=None)
    p.add_argument("--tags", default=None, help="Comma-separated tags")
    p.add_argument("--description", default=None)
    p.add_argument("--file-id", default=None, help="Attach file by ID")
    p.add_argument("--new", action="store_true", help="Force new session")

    p = sub.add_parser("search", help="Search sessions by keyword")
    p.add_argument("query")
    p.add_argument("-n", "--limit", type=int, default=5)

    p = sub.add_parser("sessions", help="List sessions")
    p.add_argument("--archived", action="store_true")
    p.add_argument("--all", action="store_true")

    p = sub.add_parser("status", help="Get session status from API")
    p.add_argument("-s", "--session", default="default")

    p = sub.add_parser("poll", help="Poll until done")
    p.add_argument("-s", "--session", default="default")
    p.add_argument("-t", "--timeout", type=int, default=600)

    p = sub.add_parser("unarchive", help="Move archived session back to active")
    p.add_argument("-s", "--session", required=True)

    p = sub.add_parser("import-task", help="Import existing Manus task into registry")
    p.add_argument("task_id")
    p.add_argument("--name", required=True)
    p.add_argument("--tags", default=None)
    p.add_argument("--description", default=None)

    p = sub.add_parser("upload", help="Upload a file to Manus")
    p.add_argument("filepath")

    p = sub.add_parser("create-project", help="Create a Manus project")
    p.add_argument("name")
    p.add_argument("--instruction", default=None)

    sub.add_parser("projects", help="List projects")

    p = sub.add_parser("tasks", help="List tasks from Manus API directly")
    p.add_argument("-n", "--limit", type=int, default=10)
    p.add_argument("--status", nargs="+")

    sub.add_parser("cleanup", help="Remove archived sessions older than 7 days")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    s = ManusSession()

    if args.command == "send":
        if args.new:
            s._registry["active"].pop(args.session, None)
            s._save_registry()
        tags = args.tags.split(",") if args.tags else None
        attachments = [{"fileId": args.file_id}] if args.file_id else None
        result = s.send(
            prompt=args.prompt, session_name=args.session,
            agent_profile=args.profile, task_mode=args.mode,
            project_id=args.project, tags=tags,
            description=args.description, attachments=attachments,
        )
        print(json.dumps(result, indent=2))

    elif args.command == "search":
        matches = s.search(args.query)[: args.limit]
        if not matches:
            print(f"No sessions matching '{args.query}'")
            return
        for m in matches:
            icon = {"active": "+", "archived": "-"}.get(m["section"], "?")
            age = _format_age(m.get("last_used", 0))
            desc = m.get("description") or m.get("first_prompt", "")
            desc = desc[:60]
            print(f"  [{icon}] {m['name']} (score:{m['score']}) — {desc} ({m.get('turn_count', 0)} turns, {age})")

    elif args.command == "sessions":
        show_archived = args.archived or args.all
        data = s.list_sessions(include_archived=show_archived)
        if data.get("active"):
            print("Active:")
            for name, e in data["active"].items():
                age = _format_age(e.get("last_used", 0))
                print(f"  {name}: [{e.get('last_status', '?')}] {e.get('turn_count', 0)} turns, {age}")
        else:
            print("Active: (none)")
        if show_archived and data.get("archived"):
            print("Archived:")
            for name, e in data["archived"].items():
                age = _format_age(e.get("archived_at", e.get("last_used", 0)))
                print(f"  {name}: [{e.get('archived_reason', '?')}] {e.get('turn_count', 0)} turns, archived {age}")

    elif args.command == "status":
        task = s.get_session_task(args.session)
        if task:
            meta = task.get("metadata", {})
            print(f"Session:  {args.session}")
            print(f"Status:   {task.get('status')}")
            print(f"Title:    {meta.get('task_title', 'N/A')}")
            print(f"Credits:  {task.get('credit_usage', 'N/A')}")
            print(f"URL:      {meta.get('task_url', 'N/A')}")
        else:
            print(f"No task found for session '{args.session}'")

    elif args.command == "poll":
        try:
            result = s.poll_until_done(args.session, timeout=args.timeout)
            print(json.dumps(result, indent=2))
        except TimeoutError as e:
            print(str(e), file=sys.stderr)
            sys.exit(3)

    elif args.command == "unarchive":
        s.unarchive(args.session)
        print(f"Unarchived '{args.session}' — now active.")

    elif args.command == "import-task":
        tags = args.tags.split(",") if args.tags else None
        entry = s.import_task(args.task_id, args.name, tags=tags, description=args.description)
        section = "archived" if "archived_at" in entry else "active"
        print(f"Imported task {args.task_id} as '{args.name}' ({section})")

    elif args.command == "upload":
        record = s.upload_file(args.filepath)
        print(f"Uploaded: {record.get('filename')} -> file_id: {record.get('id')}")

    elif args.command == "create-project":
        result = s.create_project(args.name, instruction=args.instruction)
        print(f"Created project: {result.get('id')} — {result.get('name')}")

    elif args.command == "projects":
        result = s.list_projects()
        for p_item in result.get("data", []):
            print(f"  {p_item['id']}: {p_item['name']}")

    elif args.command == "tasks":
        result = s.list_tasks(limit=args.limit, status=args.status)
        for t in result.get("data", []):
            title = t.get("metadata", {}).get("task_title", t.get("id", "?"))
            print(f"  [{t.get('status', '?')}] {title} (credits: {t.get('credit_usage', '?')})")

    elif args.command == "cleanup":
        cutoff = time.time() - (7 * 86400)
        removed = 0
        for name in list(s._registry["archived"].keys()):
            entry = s._registry["archived"][name]
            if entry.get("archived_at", 0) < cutoff:
                del s._registry["archived"][name]
                removed += 1
                print(f"  Removed: {name}")
        s._save_registry()
        print(f"Cleaned up {removed} archived session(s).")


if __name__ == "__main__":
    main()