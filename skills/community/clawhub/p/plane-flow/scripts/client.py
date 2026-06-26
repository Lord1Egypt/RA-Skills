from __future__ import annotations

from typing import Any

import requests


class PlaneAPIError(RuntimeError):
    pass


class PlaneClient:
    def __init__(
        self,
        base_url: str,
        api_token: str,
        workspace_id: str,
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_token = api_token
        self.workspace_id = workspace_id
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-API-Key": self.api_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _handle_response(self, response: requests.Response) -> Any:
        if not response.ok:
            text = response.text[:1000]
            raise PlaneAPIError(
                f"Plane API error: status={response.status_code}, body={text}"
            )

        if not response.text.strip():
            return None

        try:
            return response.json()
        except ValueError as e:
            raise PlaneAPIError(f"Invalid JSON response: {e}") from e

    def _get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> Any:
        resp = self.session.get(
            self._url(path), params=params, timeout=self.timeout
        )
        return self._handle_response(resp)

    def _post(self, path: str, payload: dict[str, Any]) -> Any:
        resp = self.session.post(
            self._url(path), json=payload, timeout=self.timeout
        )
        return self._handle_response(resp)

    def _patch(self, path: str, payload: dict[str, Any]) -> Any:
        resp = self.session.patch(
            self._url(path), json=payload, timeout=self.timeout
        )
        return self._handle_response(resp)

    def _delete(self, path: str) -> Any:
        resp = self.session.delete(self._url(path), timeout=self.timeout)
        return self._handle_response(resp)

    # ---------- Projects ----------

    def list_projects(self) -> list[dict[str, Any]]:
        path = f"/api/v1/workspaces/{self.workspace_id}/projects/"
        data = self._get(path)

        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    # ---------- Issues ----------

    def list_issues(
        self,
        project_id: str | None = None,
        state_id: str | None = None,
        assignee_id: str | None = None,
        priority: str | None = None,
        label_id: str | None = None,
        cycle_id: str | None = None,
    ) -> list[dict[str, Any]]:
        if not project_id:
            raise PlaneAPIError("list_issues currently requires project_id")

        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/"
        )
        params: dict[str, Any] = {}

        if project_id:
            params["project_id"] = project_id
        if state_id:
            params["state_id"] = state_id
        if assignee_id:
            params["assignee_id"] = assignee_id
        if priority:
            params["priority"] = priority
        if label_id:
            params["label_id"] = label_id
        if cycle_id:
            params["cycle_id"] = cycle_id

        data = self._get(path, params=params)

        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    def get_issue(self, project_id: str, issue_id: str) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/"
        )
        data = self._get(path)

        if not isinstance(data, dict):
            raise PlaneAPIError(f"Unexpected issue response for issue_id={issue_id}")
        return data

    def create_issue(
        self,
        project_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/"
        )
        data = self._post(path, payload)

        if not isinstance(data, dict):
            raise PlaneAPIError("Unexpected create_issue response")
        return data

    def update_issue(
        self,
        project_id: str,
        issue_id: str,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/"
        )
        data = self._patch(path, payload)

        if not isinstance(data, dict):
            raise PlaneAPIError("Unexpected update_issue response")
        return data

    # ---------- Attachments ----------

    def _get_presigned_url_for_attachment(
        self,
        project_id: str,
        issue_id: str,
        name: str,
        size: int,
        file_type: str,
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/issue-attachments/"
        )
        payload = {
            "name": name,
            "size": size,
            "type": file_type,
        }
        # Use raw POST without JSON wrapping for this endpoint
        import requests
        resp = requests.post(
            f"{self.base_url}{path}",
            headers={"X-API-Key": self.api_token, "Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise PlaneAPIError(
                f"Presigned URL error {resp.status_code}: {resp.text}"
            )
        return resp.json()

    def upload_attachment(
        self,
        project_id: str,
        issue_id: str,
        file_path: str,
    ) -> dict[str, Any]:
        """Upload a file as an issue attachment.

        Works in 3 steps:
        1. POST metadata to get a presigned upload URL
        2. POST the file content directly to that URL
        3. PATCH the attachment record to mark it as uploaded
        """
        import os
        import requests

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # Detect MIME type from file extension
        import mimetypes
        mime_type, _ = mimetypes.guess_type(file_path)
        file_type = mime_type or "application/octet-stream"

        # Step 1: Get presigned URL
        presigned_data = self._get_presigned_url_for_attachment(
            project_id, issue_id, filename, file_size, file_type
        )
        upload_info = presigned_data.get("upload_data", {})
        asset_id = presigned_data.get("asset_id")
        upload_url = upload_info.get("url")
        upload_fields = upload_info.get("fields", {})

        if not upload_url or not asset_id:
            raise PlaneAPIError(
                f"Invalid presigned response: {presigned_data}"
            )

        # Step 2: Upload file directly to presigned URL (S3/MinIO)
        with open(file_path, "rb") as f:
            files = {"file": (filename, f, file_type)}
            upload_resp = requests.post(
                upload_url,
                data=upload_fields,
                files=files,
                timeout=max(60, file_size // 1024),
            )
        if upload_resp.status_code not in (200, 201, 204):
            raise PlaneAPIError(
                f"File upload failed {upload_resp.status_code}: {upload_resp.text}"
            )

        # Step 3: Mark attachment as uploaded
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/issue-attachments/{asset_id}/"
        )
        self._patch(path, {})

        attachment = presigned_data.get("attachment", {"id": asset_id, "name": filename})
        asset_url = presigned_data.get("asset_url")
        result = {
            "id": asset_id,
            "name": filename,
            "attachment": attachment,
        }
        if asset_url:
            result["asset_url"] = asset_url
            result["embed_url"] = asset_url
        return result

    # ---------- Cycles ----------

    def get_cycle(self, project_id: str, cycle_id: str) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/cycles/{cycle_id}/"
        )
        return self._get(path)

    def create_cycle(
        self,
        project_id: str,
        name: str,
        description: str = "",
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/cycles/"
        )
        payload: dict[str, Any] = {
            "project_id": project_id,
            "name": name,
        }
        if description:
            payload["description"] = description
        if start_date:
            payload["start_date"] = start_date
        if end_date:
            payload["end_date"] = end_date
        return self._post(path, payload)

    def add_issues_to_cycle(
        self,
        project_id: str,
        cycle_id: str,
        issue_ids: list[str],
    ) -> list[dict[str, Any]]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/cycles/{cycle_id}/cycle-issues/"
        )
        data = self._post(path, {"issues": issue_ids})
        if isinstance(data, list):
            return data
        return []

    def remove_issue_from_cycle(
        self,
        project_id: str,
        cycle_id: str,
        issue_id: str,
    ) -> None:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/"
        )
        self._delete(path)

    def get_cycle_issues(
        self,
        project_id: str,
        cycle_id: str,
    ) -> list[dict[str, Any]]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/cycles/{cycle_id}/cycle-issues/"
        )
        data = self._get(path)
        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    # ---------- Comments ----------

    def list_comments(
        self,
        project_id: str,
        issue_id: str,
    ) -> list[dict[str, Any]]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/comments/"
        )
        data = self._get(path)
        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    def create_comment(
        self,
        project_id: str,
        issue_id: str,
        comment_html: str,
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/comments/"
        )
        return self._post(path, {"comment_html": comment_html})

    def update_comment(
        self,
        project_id: str,
        issue_id: str,
        comment_id: str,
        content_html: str,
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/comments/{comment_id}/"
        )
        return self._patch(path, {"content_html": content_html})

    def delete_comment(
        self,
        project_id: str,
        issue_id: str,
        comment_id: str,
    ) -> None:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/comments/{comment_id}/"
        )
        self._delete(path)

    # ---------- Issue External Links ----------

    def list_issue_links(
        self,
        project_id: str,
        issue_id: str,
    ) -> list[dict[str, Any]]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/links/"
        )
        data = self._get(path)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        return []

    def create_issue_link(
        self,
        project_id: str,
        issue_id: str,
        url: str,
        title: str = "",
    ) -> dict[str, Any]:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/links/"
        )
        return self._post(path, {"url": url, "title": title})

    def delete_issue_link(
        self,
        project_id: str,
        issue_id: str,
        link_id: str,
    ) -> None:
        path = (
            f"/api/v1/workspaces/{self.workspace_id}/projects/"
            f"{project_id}/issues/{issue_id}/links/{link_id}/"
        )
        self._delete(path)

    # ---------- Projects ----------

    def create_project(
        self,
        name: str,
        identifier: str,
        description: str = "",
    ) -> dict[str, Any]:
        path = f"/api/v1/workspaces/{self.workspace_id}/projects/"
        payload: dict[str, Any] = {"name": name, "identifier": identifier}
        if description:
            payload["description"] = description
        return self._post(path, payload)

    # ---------- Metadata ----------

    def list_states(
        self, project_id: str | None = None
    ) -> list[dict[str, Any]]:
        if project_id:
            path = (
                f"/api/v1/workspaces/{self.workspace_id}/projects/"
                f"{project_id}/states/"
            )
        else:
            path = f"/api/v1/workspaces/{self.workspace_id}/states/"

        data = self._get(path)

        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    def list_labels(
        self, project_id: str | None = None
    ) -> list[dict[str, Any]]:
        if project_id:
            path = (
                f"/api/v1/workspaces/{self.workspace_id}/projects/"
                f"{project_id}/labels/"
            )
        else:
            path = f"/api/v1/workspaces/{self.workspace_id}/labels/"

        data = self._get(path)

        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    def list_members(self) -> list[dict[str, Any]]:
        path = f"/api/v1/workspaces/{self.workspace_id}/members/"
        data = self._get(path)

        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []

    def list_cycles(
        self, project_id: str | None = None
    ) -> list[dict[str, Any]]:
        if project_id:
            path = (
                f"/api/v1/workspaces/{self.workspace_id}/projects/"
                f"{project_id}/cycles/"
            )
        else:
            path = f"/api/v1/workspaces/{self.workspace_id}/cycles/"

        data = self._get(path)

        if isinstance(data, dict) and "results" in data:
            return data["results"] or []
        if isinstance(data, list):
            return data
        return []
