"""Lovart local project and thread list.

The directory exists only after setup. If it is missing, state is not
saved and this module leaves the directory absent.
"""
import json
import time
from typing import Optional

class LocalState:
    """Persistent local state with multi-project support.

    State structure:
    {
      "active_project": "project_id_1",
      "projects": {
        "project_id_1": {"name": "My Design", "created_at": "..."},
        "project_id_2": {"name": "Brand Kit", "created_at": "..."}
      },
      "threads": [
        {"id": "xxx", "project_id": "project_id_1", "topic": "...", "updated_at": "..."}
      ]
    }
    """

    def __init__(self, path: Optional[str] = None):
        import os
        self.path = path or os.path.expanduser("~/.lovart/state.json")

    def _ensure_dir(self):
        import os
        parent = os.path.dirname(self.path)
        if os.path.isdir(parent):
            return
        raise FileNotFoundError(
            f"{parent} does not exist. Create it during Lovart setup. "
            "Generation does not create this directory."
        )

    def load(self) -> dict:
        import os
        if not os.path.exists(self.path):
            return {}
        try:
            with open(self.path, "r") as f:
                data = json.load(f)
            # Migrate old format (flat project_id → multi-project)
            if "project_id" in data and "projects" not in data:
                old_pid = data.pop("project_id")
                data["active_project"] = old_pid
                data["projects"] = {old_pid: {"name": "default", "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())}}
                self.save(data)
            return data
        except (json.JSONDecodeError, IOError):
            return {}

    def save(self, data: dict):
        import sys
        try:
            self._ensure_dir()
        except FileNotFoundError as error:
            print(f"Warning: {error}", file=sys.stderr)
            return
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ── Project management ──

    def get_project_id(self) -> Optional[str]:
        return self.load().get("active_project")

    def get_projects(self) -> dict:
        return self.load().get("projects", {})

    def add_project(self, project_id: str, name: str = ""):
        data = self.load()
        projects = data.setdefault("projects", {})
        if project_id not in projects:
            projects[project_id] = {
                "name": name or project_id[:8],
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()),
            }
        elif name:
            projects[project_id]["name"] = name
        data["active_project"] = project_id
        self.save(data)

    def switch_project(self, project_id: str) -> bool:
        data = self.load()
        projects = data.get("projects", {})
        if project_id not in projects:
            # Allow switching to a new project by partial match
            matches = [pid for pid in projects if pid.startswith(project_id)]
            if len(matches) == 1:
                project_id = matches[0]
            else:
                return False
        data["active_project"] = project_id
        self.save(data)
        return True

    def rename_project(self, project_id: str, name: str):
        data = self.load()
        projects = data.get("projects", {})
        if project_id in projects:
            projects[project_id]["name"] = name
            self.save(data)

    def remove_project(self, project_id: str):
        data = self.load()
        projects = data.get("projects", {})
        projects.pop(project_id, None)
        if data.get("active_project") == project_id:
            data["active_project"] = next(iter(projects), None)
        # Remove associated threads
        data["threads"] = [t for t in data.get("threads", []) if t.get("project_id") != project_id]
        self.save(data)

    # ── Thread management ──

    def get_threads(self, project_id: Optional[str] = None) -> list:
        threads = self.load().get("threads", [])
        if project_id:
            threads = [t for t in threads if t.get("project_id") == project_id]
        return threads

    def remove_thread(self, thread_id: str):
        data = self.load()
        data["threads"] = [t for t in data.get("threads", []) if t["id"] != thread_id]
        self.save(data)

    def upsert_thread(self, thread_id: str, topic: str, project_id: Optional[str] = None):
        data = self.load()
        threads = data.get("threads", [])
        pid = project_id or data.get("active_project")
        found = False
        for t in threads:
            if t["id"] == thread_id:
                t["topic"] = topic
                t["project_id"] = pid
                t["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime())
                found = True
                break
        if not found:
            threads.insert(0, {
                "id": thread_id,
                "project_id": pid,
                "topic": topic,
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z", time.localtime()),
            })
        data["threads"] = threads[:50]
        self.save(data)

