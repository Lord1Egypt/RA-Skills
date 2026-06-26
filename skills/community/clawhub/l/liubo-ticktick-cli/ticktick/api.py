import re
import sys
import time

import requests as _requests

from .auth import get_valid_token

API_BASE = "https://api.dida365.com/open/v1"

PRIORITY_MAP = {"none": 0, "low": 1, "medium": 3, "high": 5}
PRIORITY_REVERSE = {0: "none", 1: "low", 3: "medium", 5: "high"}

_RETRY_DELAYS = [5, 15, 30, 60]  # seconds
_MAX_RETRIES = 4


class TickTickAPI:
    def _request(self, method: str, endpoint: str, retry_count: int = 0, **kwargs) -> dict | list:
        token = get_valid_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            **kwargs.pop("headers", {}),
        }
        resp = _requests.request(
            method, f"{API_BASE}{endpoint}", headers=headers, **kwargs
        )

        if not resp.ok:
            error_text = resp.text

            is_rate_limit = resp.status_code == 429 or (
                resp.status_code == 500 and "exceed_query_limit" in error_text
            )
            if is_rate_limit:
                if retry_count < _MAX_RETRIES:
                    wait = _RETRY_DELAYS[retry_count]
                    print(
                        f"Rate limited, waiting {wait}s before retry "
                        f"{retry_count + 1}/{_MAX_RETRIES}...",
                        file=sys.stderr,
                    )
                    time.sleep(wait)
                    return self._request(method, endpoint, retry_count + 1, **kwargs)
                raise RuntimeError(
                    "Rate limit exceeded. Maximum retries reached. "
                    "Please wait a few minutes and try again."
                )

            if resp.status_code == 401:
                raise RuntimeError(
                    "Authentication expired. Please run 'ticktick auth' to re-authenticate."
                )
            if resp.status_code == 404:
                raise RuntimeError(f"Not found: {endpoint}")
            raise RuntimeError(
                f"API error {resp.status_code}: {error_text or resp.reason}"
            )

        text = resp.text
        if not text:
            return {}
        return resp.json()

    # ── Projects ──────────────────────────────────────────────────────────────

    def list_projects(self) -> list[dict]:
        return self._request("GET", "/project")

    def create_project(self, name: str, color: str | None = None) -> dict:
        body: dict = {"name": name}
        if color:
            body["color"] = color
        return self._request("POST", "/project", json=body)

    def update_project(self, project_id: str, name: str | None = None, color: str | None = None) -> dict:
        body: dict = {}
        if name:
            body["name"] = name
        if color:
            body["color"] = color
        return self._request("POST", f"/project/{project_id}", json=body)

    def get_project_data(self, project_id: str) -> dict:
        return self._request("GET", f"/project/{project_id}/data")

    # ── Tasks ─────────────────────────────────────────────────────────────────

    def create_task(self, payload: dict) -> dict:
        return self._request("POST", "/task", json=payload)

    def update_task(self, payload: dict) -> dict:
        return self._request("POST", f"/task/{payload['id']}", json=payload)

    def complete_task(self, project_id: str, task_id: str) -> None:
        self._request("POST", f"/project/{project_id}/task/{task_id}/complete")

    def delete_task(self, project_id: str, task_id: str) -> None:
        self._request("DELETE", f"/project/{project_id}/task/{task_id}")

    def batch_tasks(self, batch: dict) -> dict:
        return self._request("POST", "/batch/task", json=batch)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def find_project_by_name(self, name: str) -> dict | None:
        projects = self.list_projects()
        lower = name.lower()
        return next(
            (p for p in projects if p["name"].lower() == lower or p["id"] == name),
            None,
        )

    def find_task_by_id(self, task_id: str) -> dict | None:
        """Search all projects for a task with the given ID.
        Returns {"task": {...}, "projectId": str} or None.
        """
        for project in self.list_projects():
            try:
                data = self.get_project_data(project["id"])
                for task in data.get("tasks") or []:
                    if task["id"] == task_id:
                        return {"task": task, "projectId": project["id"]}
            except RuntimeError:
                continue
        return None

    def find_task_by_title(self, title: str, project_name: str | None = None) -> dict | None:
        """Search projects for a task matching title (case-insensitive) or ID.
        Returns {"task": {...}, "projectId": str} or None.
        Raises RuntimeError if multiple matches found.
        """
        projects = self.list_projects()
        if project_name:
            projects = [
                p for p in projects
                if p["name"].lower() == project_name.lower() or p["id"] == project_name
            ]

        is_id_search = bool(re.fullmatch(r"[a-f0-9]{24}", title, re.IGNORECASE))
        matches: list[dict] = []

        for project in projects:
            try:
                data = self.get_project_data(project["id"])
                for task in data.get("tasks") or []:
                    if task["title"].lower() == title.lower() or task["id"] == title:
                        matches.append({"task": task, "projectId": project["id"], "projectName": project["name"]})
            except RuntimeError:
                continue

        if not matches:
            return None
        if is_id_search or len(matches) == 1:
            return {"task": matches[0]["task"], "projectId": matches[0]["projectId"]}

        match_list = "\n".join(
            f"  [{m['task']['id'][:8]}] \"{m['task']['title']}\" in project \"{m['projectName']}\""
            for m in matches
        )
        raise RuntimeError(
            f"Multiple tasks found with name \"{title}\":\n{match_list}\n\n"
            "Please use the task ID instead of the name to specify which task."
        )

    def get_all_tasks(self, project_name: str | None = None) -> list[dict]:
        projects = self.list_projects()
        if project_name:
            projects = [
                p for p in projects
                if p["name"].lower() == project_name.lower() or p["id"] == project_name
            ]
        all_tasks: list[dict] = []
        for project in projects:
            try:
                data = self.get_project_data(project["id"])
                all_tasks.extend(data.get("tasks") or [])
            except RuntimeError:
                continue
        return all_tasks


api = TickTickAPI()
