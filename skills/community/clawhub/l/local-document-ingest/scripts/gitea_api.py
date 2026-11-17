import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from utils import sha256_text


class GiteaClient:
    def __init__(self, payload=None):
        payload = payload or {}
        platform = payload.get("platform") or {}
        team = payload.get("team") or {}
        self.url = (platform.get("giteaUrl") or os.getenv("GITEA_URL") or "").rstrip("/")
        self.token = os.getenv("GITEA_BOT_TOKEN") or ""
        self.owner = platform.get("giteaOwner") or os.getenv("GITEA_ORG") or os.getenv("GITEA_BOT_USERNAME") or ""
        self.repo = team.get("kbRepo") or os.getenv("TEAM_KB_REPO") or ""
        self.dry_run = bool(payload.get("dryRun")) or not (self.url and self.token and self.owner and self.repo)
        self.last_commit = "dry-run"

    def read_text(self, path):
        data = self.read_bytes(path)
        return data.decode("utf-8", errors="replace") if data else ""

    def read_bytes(self, path):
        if self.dry_run:
            return b""
        try:
            response = self._request("GET", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return b""
            raise
        content = response.get("content") or ""
        return base64.b64decode(content) if content else b""

    def exists(self, path):
        if self.dry_run:
            return False
        return self._existing_sha(path) is not None

    def upsert_text(self, path, content, message):
        return self.upsert_bytes(path, content.encode("utf-8"), message)

    def upsert_bytes(self, path, content, message):
        if self.dry_run:
            digest = sha256_text(path + "\n" + base64.b64encode(content).decode("ascii"))[:12]
            self.last_commit = "dry-run-" + digest
            return {"path": path, "commit": self.last_commit}
        sha = self._existing_sha(path)
        body = {
            "message": message,
            "content": base64.b64encode(content).decode("ascii"),
        }
        if sha:
            body["sha"] = sha
        response = self._request("PUT", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}", body)
        commit = response.get("commit") or {}
        self.last_commit = commit.get("id") or commit.get("sha") or "unknown"
        return {"path": path, "commit": self.last_commit}

    def _existing_sha(self, path):
        try:
            response = self._request("GET", f"/repos/{self._q(self.owner)}/{self._q(self.repo)}/contents/{self._path(path)}")
            return response.get("sha")
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise

    def _request(self, method, endpoint, body=None):
        data = None
        headers = {"Authorization": f"token {self.token}", "Accept": "application/json"}
        if body is not None:
            data = json.dumps(body).encode("utf-8")
            headers["Content-Type"] = "application/json"
        request = urllib.request.Request(self.url + "/api/v1" + endpoint, data=data, headers=headers, method=method)
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            return json.loads(raw) if raw else {}

    @staticmethod
    def _q(value):
        return urllib.parse.quote(str(value), safe="")

    @staticmethod
    def _path(value):
        return urllib.parse.quote(str(value).replace("\\", "/"), safe="/")