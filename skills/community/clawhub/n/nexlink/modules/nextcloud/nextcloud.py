#!/usr/bin/env python3
"""Nextcloud WebDAV file management client."""

from __future__ import annotations

import io
import json
import os
import re
import sys
import urllib.parse
from defusedxml import ElementTree as ET
import zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import requests
    from requests.auth import HTTPBasicAuth
    from requests.exceptions import RequestException
except ImportError as exc:
    raise ImportError(
        "'requests' library required. Install with: pip install requests"
    ) from exc


LIST_PROPFIND_BODY = """<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:">
    <d:prop>
        <d:displayname/>
        <d:resourcetype/>
        <d:getcontentlength/>
        <d:getlastmodified/>
        <d:getcontenttype/>
    </d:prop>
</d:propfind>"""

INFO_PROPFIND_BODY = """<?xml version="1.0" encoding="utf-8"?>
<d:propfind xmlns:d="DAV:" xmlns:oc="http://owncloud.org/ns" xmlns:nc="http://nextcloud.org/ns">
    <d:prop>
        <d:displayname/>
        <d:resourcetype/>
        <d:getcontentlength/>
        <d:getlastmodified/>
        <d:getcontenttype/>
        <d:getetag/>
        <oc:fileid/>
        <oc:size/>
    </d:prop>
</d:propfind>"""

DEFAULT_TIMEOUT = 60
TRANSFER_TIMEOUT = 300
WEBDAV_SUCCESS_CODES = {200, 201, 204, 207}
PUBLIC_LINK_SHARE_TYPE = "3"


def _confirm_or_die(action_desc: str, auto_approved: bool = False) -> None:
    """Prompt for confirmation before a destructive operation.

    Bypassed when auto_approved is True (e.g., via per-command --yes).
    There is no session-wide or environment bypass.
    Exits with code 2 on non-confirmation.
    """
    if auto_approved or _AUTO_APPROVED:
        return

    if not sys.stdin.isatty():
        print(json.dumps({
            "ok": False,
            "error": f"Confirmation required: {action_desc}. "
                      "Re-run with --yes to confirm this single operation.",
        }), file=sys.stderr)
        sys.exit(2)

    try:
        answer = input(f"⚠️  {action_desc} [y/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("", file=sys.stderr)
        sys.exit(2)

    if answer not in ("y", "yes"):
        print("Aborted.", file=sys.stderr)
        sys.exit(2)


TEXT_FILE_EXTENSIONS = {
    ".txt",
    ".md",
    ".markdown",
    ".csv",
    ".json",
    ".yaml",
    ".yml",
    ".py",
    ".js",
    ".ts",
    ".html",
    ".xml",
}
STOPWORDS = {
    "the", "and", "for", "that", "with", "this", "from", "have", "are", "was",
    "but", "not", "you", "your", "into", "about", "will", "they", "them", "their",
    "din", "pentru", "care", "este", "sunt", "sau", "ceva", "asta", "acest", "aceasta",
    "prin", "fara", "după", "dupa", "când", "cand", "care", "iar", "mai", "foarte",
}
ACTION_KEYWORDS = (
    "send",
    "confirm",
    "create",
    "review",
    "approve",
    "follow up",
    "follow-up",
    "schedule",
    "call",
    "prepare",
    "reply",
)
MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


_JSON_OUTPUT = False
_AUTO_APPROVED = False

def get_exchange_account(mailbox: str | None = None) -> Any:
    """Get an Exchange account for task creation."""
    from modules.exchange.connection import get_account, get_account_for

    return get_account_for(mailbox) if mailbox else get_account()



def build_exchange_task(account: Any, subject: str, body: str) -> Any:
    """Build a new Exchange task instance."""
    from exchangelib.items import Task

    return Task(account=account, folder=account.tasks, subject=subject, body=body)



def build_ews_date(date_value: str) -> Any:
    """Convert an ISO date string into an EWSDate."""
    from exchangelib import EWSDate

    parsed = datetime.strptime(date_value, "%Y-%m-%d")
    return EWSDate(parsed.year, parsed.month, parsed.day)


class NextcloudClient:
    """Client for Nextcloud WebDAV and OCS operations."""

    def __init__(self) -> None:
        """Initialize client from environment variables."""
        self.url = os.environ.get("NEXTCLOUD_URL", "").rstrip("/")
        self.username = os.environ.get("NEXTCLOUD_USERNAME", "")
        self.app_password = os.environ.get("NEXTCLOUD_APP_PASSWORD", "")

        if not all([self.url, self.username, self.app_password]):
            raise EnvironmentError(
                "Missing required environment variables: "
                "NEXTCLOUD_URL, NEXTCLOUD_USERNAME, NEXTCLOUD_APP_PASSWORD"
            )

        self.auth = HTTPBasicAuth(self.username, self.app_password)
        self.user_id: str | None = None
        self._resolve_user_id()

    def _resolve_user_id(self) -> None:
        """Resolve the effective user ID from Nextcloud OCS API."""
        ocs_url = f"{self.url}/ocs/v1.php/cloud/user"
        headers = {"OCS-APIRequest": "true"}

        try:
            response = requests.get(
                ocs_url,
                auth=self.auth,
                headers=headers,
                timeout=30,
            )
            if response.status_code != 200:
                self.user_id = self.username
                return

            root = ET.fromstring(response.content)
            id_elem = root.find(".//id")
            self.user_id = id_elem.text if id_elem is not None and id_elem.text else self.username
        except (ET.ParseError, RequestException):
            self.user_id = self.username

    def _ocs_url(self, endpoint: str) -> str:
        """Build a full OCS URL for an API endpoint."""
        return f"{self.url}/ocs/v1.php{endpoint}"

    def _request(
        self,
        method: str,
        url: str,
        *,
        operation: str,
        timeout: int = DEFAULT_TIMEOUT,
        expected_statuses: set[int] | None = None,
        **kwargs: Any,
    ) -> requests.Response | None:
        """Send an HTTP request and normalize transport errors."""
        expected = expected_statuses or {200}

        try:
            response = requests.request(
                method,
                url,
                auth=self.auth,
                timeout=timeout,
                **kwargs,
            )
        except RequestException as exc:
            print(f"Error {operation}: connection failed ({exc})")
            return None

        if response.status_code not in expected:
            print(
                f"Error {operation}: HTTP {response.status_code}"
                f"{self._describe_status(response.status_code)}"
            )
            return None

        return response

    def _ocs_request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        operation: str,
        expected_statuses: set[int] | None = None,
    ) -> ET.Element | None:
        """Make an OCS API request and return parsed XML on success."""
        headers = {"OCS-APIRequest": "true"}
        response = self._request(
            method,
            self._ocs_url(endpoint),
            operation=operation,
            timeout=DEFAULT_TIMEOUT,
            expected_statuses=expected_statuses or {200, 201},
            headers=headers,
            params=params,
            data=data,
        )
        if response is None:
            return None

        try:
            root = ET.fromstring(response.content)
        except ET.ParseError as exc:
            print(f"Error {operation}: invalid OCS XML response ({exc})")
            return None

        meta = root.find(".//meta")
        status_code = meta.findtext("statuscode", default="") if meta is not None else ""
        message = meta.findtext("message", default="") if meta is not None else ""

        if status_code and status_code != "100":
            friendly = f": {message}" if message else ""
            print(f"Error {operation}: OCS status {status_code}{friendly}")
            return None

        return root

    def _describe_status(self, status_code: int) -> str:
        """Return a short status description for common HTTP codes."""
        descriptions = {
            401: " (authentication failed)",
            403: " (forbidden)",
            404: " (not found)",
            409: " (conflict)",
            423: " (resource locked)",
            507: " (insufficient storage)",
        }
        return descriptions.get(status_code, "")

    def _parse_permissions(self, perm_value: str | None) -> str:
        """Parse a permission bitmask into a readable string."""
        try:
            perm = int(perm_value or "")
        except (TypeError, ValueError):
            return "unknown"

        labels = []
        if perm & 1:
            labels.append("read")
        if perm & 2:
            labels.append("write")
        if perm & 4:
            labels.append("create")
        if perm & 8:
            labels.append("delete")
        if perm & 16:
            labels.append("share")
        return "/".join(labels) if labels else "none"

    def _get_webdav_base_url(self) -> str:
        """Get the WebDAV base URL using the resolved user ID."""
        user_id = self.user_id or self.username
        return f"{self.url}/remote.php/dav/files/{urllib.parse.quote(user_id, safe='')}"

    def _normalize_remote_path(self, remote_path: str) -> str:
        """Normalize a remote path to a canonical absolute path."""
        if not remote_path or remote_path == "/":
            return "/"

        cleaned = "/" + "/".join(part for part in remote_path.split("/") if part)
        return cleaned or "/"

    def _get_full_url(self, remote_path: str) -> str:
        """Build the full WebDAV URL for a remote path."""
        normalized_path = self._normalize_remote_path(remote_path)
        return f"{self._get_webdav_base_url()}{urllib.parse.quote(normalized_path, safe='/')}"

    def _href_to_remote_path(self, href: str) -> str:
        """Convert a WebDAV href into a canonical remote path."""
        parsed = urllib.parse.urlparse(urllib.parse.unquote(href))
        remote_prefix = urllib.parse.urlparse(self._get_webdav_base_url()).path
        raw_path = parsed.path if parsed.scheme else urllib.parse.unquote(href)

        if remote_prefix and raw_path.startswith(remote_prefix):
            suffix = raw_path[len(remote_prefix) :]
            return self._normalize_remote_path(suffix)

        return self._normalize_remote_path(raw_path)

    def _list_directory(self, remote_path: str) -> list[dict[str, Any]] | None:
        """List a single directory level."""
        normalized_path = self._normalize_remote_path(remote_path)
        response = self._request(
            "PROPFIND",
            self._get_full_url(normalized_path),
            operation=f"listing directory '{normalized_path}'",
            timeout=DEFAULT_TIMEOUT,
            expected_statuses={200, 207},
            headers={"Depth": "1", "Content-Type": "application/xml"},
            data=LIST_PROPFIND_BODY,
        )
        if response is None:
            return None
        return self._parse_list_response(response.content, normalized_path)

    def list(self, remote_path: str = "/", recursive: bool = False) -> list[dict[str, Any]] | None:
        """List files and folders in a directory."""
        normalized_path = self._normalize_remote_path(remote_path)
        if not recursive:
            return self._list_directory(normalized_path)

        queue = [normalized_path]
        visited: set[str] = set()
        results: list[dict[str, Any]] = []

        while queue:
            current_path = queue.pop(0)
            if current_path in visited:
                continue
            visited.add(current_path)

            current_results = self._list_directory(current_path)
            if current_results is None:
                return None

            results.extend(current_results)
            for item in current_results:
                if item["type"] == "folder":
                    queue.append(item["path"])

        return results

    def _parse_list_response(
        self,
        content: bytes,
        base_path: str,
    ) -> list[dict[str, Any]]:
        """Parse a WebDAV PROPFIND response."""
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            return []

        normalized_base = self._normalize_remote_path(base_path)
        results: list[dict[str, Any]] = []

        for response_elem in root.findall(".//{DAV:}response"):
            href_elem = response_elem.find(".//{DAV:}href")
            if href_elem is None or not href_elem.text:
                continue

            item_path = self._href_to_remote_path(href_elem.text)
            if item_path == normalized_base:
                continue

            name = item_path.rstrip("/").split("/")[-1] if item_path != "/" else "/"
            resourcetype = response_elem.find(".//{DAV:}resourcetype")
            is_folder = (
                resourcetype is not None
                and resourcetype.find("{DAV:}collection") is not None
            )
            content_length = response_elem.find(".//{DAV:}getcontentlength")
            last_modified = response_elem.find(".//{DAV:}getlastmodified")
            content_type = response_elem.find(".//{DAV:}getcontenttype")

            results.append(
                {
                    "name": name,
                    "type": "folder" if is_folder else "file",
                    "size": int(content_length.text) if content_length is not None and content_length.text else 0,
                    "modified": last_modified.text if last_modified is not None and last_modified.text else "Unknown",
                    "mime_type": content_type.text if content_type is not None and content_type.text else "",
                    "path": item_path,
                }
            )

        return results

    def search(self, query: str, remote_path: str = "/") -> list[dict[str, Any]] | None:
        """Search for files or folders by name."""
        normalized_query = query.strip().lower()
        if not normalized_query:
            print("Error search: query cannot be empty")
            return None

        results = self.list(remote_path, recursive=True)
        if results is None:
            return None

        return [
            item
            for item in results
            if normalized_query in item["name"].lower() or normalized_query in item["path"].lower()
        ]

    def upload(self, local_path: str, remote_path: str) -> bool:
        """Upload a local file to Nextcloud."""
        source_path = Path(local_path)
        if not source_path.exists() or not source_path.is_file():
            print(f"Error upload: local file not found: {source_path}")
            return False

        target_path = remote_path
        if remote_path.endswith("/"):
            target_path = f"{remote_path}{source_path.name}"

        try:
            with source_path.open("rb") as handle:
                response = self._request(
                    "PUT",
                    self._get_full_url(target_path),
                    operation=f"uploading '{source_path.name}'",
                    timeout=TRANSFER_TIMEOUT,
                    expected_statuses={200, 201, 204},
                    data=handle,
                )
        except OSError as exc:
            print(f"Error upload: failed to read local file ({exc})")
            return False

        if response is None:
            return False

        print(f"Uploaded: {source_path} -> {self._normalize_remote_path(target_path)}")
        return True

    def download(self, remote_path: str, local_path: str) -> bool:
        """Download a file from Nextcloud."""
        response = self._request(
            "GET",
            self._get_full_url(remote_path),
            operation=f"downloading '{self._normalize_remote_path(remote_path)}'",
            timeout=TRANSFER_TIMEOUT,
            expected_statuses={200},
            stream=True,
        )
        if response is None:
            return False

        destination = Path(local_path)
        if destination.is_dir():
            destination = destination / Path(self._normalize_remote_path(remote_path)).name

        destination.parent.mkdir(parents=True, exist_ok=True)
        try:
            with destination.open("wb") as handle:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        handle.write(chunk)
        except OSError as exc:
            print(f"Error download: failed to write local file ({exc})")
            return False

        print(f"Downloaded: {self._normalize_remote_path(remote_path)} -> {destination}")
        return True

    def mkdir(self, remote_path: str) -> bool:
        """Create a directory on Nextcloud."""
        target_url = self._get_full_url(remote_path)
        if not target_url.endswith("/"):
            target_url += "/"

        response = self._request(
            "MKCOL",
            target_url,
            operation=f"creating directory '{self._normalize_remote_path(remote_path)}'",
            timeout=DEFAULT_TIMEOUT,
            expected_statuses={200, 201},
        )
        if response is None:
            return False

        print(f"Created directory: {self._normalize_remote_path(remote_path)}")
        return True

    def delete(self, remote_path: str) -> bool:
        """Delete a file or directory on Nextcloud."""
        response = self._request(
            "DELETE",
            self._get_full_url(remote_path),
            operation=f"deleting '{self._normalize_remote_path(remote_path)}'",
            timeout=DEFAULT_TIMEOUT,
            expected_statuses={200, 204},
        )
        if response is None:
            return False

        print(f"Deleted: {self._normalize_remote_path(remote_path)}")
        return True

    def move(self, source_path: str, dest_path: str) -> bool:
        """Move or rename a file or directory."""
        response = self._request(
            "MOVE",
            self._get_full_url(source_path),
            operation=f"moving '{self._normalize_remote_path(source_path)}'",
            timeout=DEFAULT_TIMEOUT,
            expected_statuses={200, 201, 204},
            headers={"Destination": self._get_full_url(dest_path)},
        )
        if response is None:
            return False

        print(
            f"Moved: {self._normalize_remote_path(source_path)}"
            f" -> {self._normalize_remote_path(dest_path)}"
        )
        return True

    def copy(self, source_path: str, dest_path: str) -> bool:
        """Copy a file or directory."""
        response = self._request(
            "COPY",
            self._get_full_url(source_path),
            operation=f"copying '{self._normalize_remote_path(source_path)}'",
            timeout=DEFAULT_TIMEOUT,
            expected_statuses={200, 201, 204},
            headers={"Destination": self._get_full_url(dest_path)},
        )
        if response is None:
            return False

        print(
            f"Copied: {self._normalize_remote_path(source_path)}"
            f" -> {self._normalize_remote_path(dest_path)}"
        )
        return True

    def info(self, remote_path: str) -> dict[str, Any] | None:
        """Get detailed information about a file or directory."""
        response = self._request(
            "PROPFIND",
            self._get_full_url(remote_path),
            operation=f"getting info for '{self._normalize_remote_path(remote_path)}'",
            timeout=DEFAULT_TIMEOUT,
            expected_statuses={200, 207},
            headers={"Depth": "0", "Content-Type": "application/xml"},
            data=INFO_PROPFIND_BODY,
        )
        if response is None:
            return None

        return self._parse_info_response(response.content)

    def _parse_info_response(self, content: bytes) -> dict[str, Any] | None:
        """Parse WebDAV PROPFIND response for a single item."""
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            return None

        response_elem = root.find(".//{DAV:}response")
        if response_elem is None:
            return None

        resourcetype = response_elem.find(".//{DAV:}resourcetype")
        content_length = response_elem.find(".//{DAV:}getcontentlength")
        oc_size = response_elem.find(".//{http://owncloud.org/ns}size")
        last_modified = response_elem.find(".//{DAV:}getlastmodified")
        content_type = response_elem.find(".//{DAV:}getcontenttype")
        etag = response_elem.find(".//{DAV:}getetag")
        file_id = response_elem.find(".//{http://owncloud.org/ns}fileid")
        displayname = response_elem.find(".//{DAV:}displayname")

        size = int(content_length.text) if content_length is not None and content_length.text else 0
        if oc_size is not None and oc_size.text:
            size = int(oc_size.text)

        return {
            "name": displayname.text if displayname is not None and displayname.text else "Unknown",
            "type": "folder" if resourcetype is not None and resourcetype.find("{DAV:}collection") is not None else "file",
            "size": size,
            "modified": last_modified.text if last_modified is not None and last_modified.text else "Unknown",
            "mime_type": content_type.text if content_type is not None and content_type.text else "",
            "etag": etag.text if etag is not None and etag.text else "",
            "file_id": file_id.text if file_id is not None and file_id.text else "",
        }

    def get_shared_with_me(self) -> list[dict[str, Any]]:
        """Get folders or files shared with the current user."""
        root = self._ocs_request(
            "GET",
            "/apps/files_sharing/api/v1/shares",
            params={"shared_with_me": "true"},
            operation="listing items shared with me",
        )
        if root is None:
            return []

        shares: list[dict[str, Any]] = []
        data = root.find(".//data")
        if data is None:
            return shares

        for elem in data.findall(".//element"):
            path = elem.findtext("file_target", default="")
            owner = elem.findtext("uid_owner", default="Unknown")
            shares.append(
                {
                    "id": elem.findtext("id", default=""),
                    "path": self._normalize_remote_path(path),
                    "share_type": elem.findtext("share_type", default="0"),
                    "owner": owner,
                    "owner_display": elem.findtext("displayname_owner", default=owner),
                    "permissions": self._parse_permissions(elem.findtext("permissions", default="1")),
                    "name": elem.findtext("name", default=Path(path).name or "/"),
                    "shared_at": elem.findtext("stime", default=""),
                }
            )

        return shares

    def create_share_link(
        self,
        remote_path: str,
        *,
        password: str | None = None,
        expire_date: str | None = None,
        public_upload: bool = False,
    ) -> dict[str, Any] | None:
        """Create a public share link for a file or folder."""
        payload: dict[str, Any] = {
            "path": self._normalize_remote_path(remote_path),
            "shareType": PUBLIC_LINK_SHARE_TYPE,
            "permissions": "15" if public_upload else "1",
        }
        if password:
            payload["password"] = password
        if expire_date:
            payload["expireDate"] = expire_date

        root = self._ocs_request(
            "POST",
            "/apps/files_sharing/api/v1/shares",
            data=payload,
            operation=f"creating share link for '{payload['path']}'",
        )
        if root is None:
            return None

        data = root.find(".//data")
        if data is None:
            print("Error creating share link: missing OCS data payload")
            return None

        return {
            "id": data.findtext("id", default=""),
            "path": self._normalize_remote_path(data.findtext("path", default=payload["path"])),
            "url": data.findtext("url", default=""),
            "token": data.findtext("token", default=""),
            "permissions": self._parse_permissions(data.findtext("permissions", default=payload["permissions"])),
            "password_protected": bool(password),
            "expire_date": expire_date or data.findtext("expiration", default=""),
        }

    def list_share_links(self, remote_path: str | None = None) -> list[dict[str, Any]]:
        """List public share links, optionally filtered by remote path."""
        params: dict[str, Any] | None = None
        if remote_path:
            params = {"path": self._normalize_remote_path(remote_path)}

        root = self._ocs_request(
            "GET",
            "/apps/files_sharing/api/v1/shares",
            params=params,
            operation="listing share links",
        )
        if root is None:
            return []

        data = root.find(".//data")
        if data is None:
            return []

        links: list[dict[str, Any]] = []
        for elem in data.findall(".//element"):
            if elem.findtext("share_type", default="") != PUBLIC_LINK_SHARE_TYPE:
                continue
            links.append(
                {
                    "id": elem.findtext("id", default=""),
                    "path": self._normalize_remote_path(elem.findtext("path", default="/")),
                    "url": elem.findtext("url", default=""),
                    "permissions": self._parse_permissions(elem.findtext("permissions", default="1")),
                    "password_protected": elem.findtext("share_with", default="") != "",
                    "expire_date": elem.findtext("expiration", default=""),
                }
            )

        return links

    def revoke_share_link(self, share_id: str) -> bool:
        """Revoke an existing public share link by ID."""
        root = self._ocs_request(
            "DELETE",
            f"/apps/files_sharing/api/v1/shares/{share_id}",
            operation=f"revoking share link '{share_id}'",
            expected_statuses={200},
        )
        if root is None:
            return False

        print(f"Revoked share link: {share_id}")
        return True

    def _download_file_bytes(self, remote_path: str) -> bytes | None:
        """Download raw file bytes for document analysis commands."""
        normalized_path = self._normalize_remote_path(remote_path)
        response = self._request(
            "GET",
            self._get_full_url(normalized_path),
            operation=f"reading file '{normalized_path}'",
            timeout=TRANSFER_TIMEOUT,
            expected_statuses={200},
        )
        if response is None:
            return None
        return response.content

    def _decode_text_bytes(self, content: bytes) -> str:
        """Decode common text payloads using a small encoding fallback chain."""
        for encoding in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                return content.decode(encoding)
            except UnicodeDecodeError:
                continue
        return content.decode("utf-8", errors="replace")

    def _extract_docx_text(self, content: bytes) -> str:
        """Extract visible text from a DOCX document."""
        try:
            with zipfile.ZipFile(io.BytesIO(content)) as archive:
                document_xml = archive.read("word/document.xml")
        except (KeyError, zipfile.BadZipFile):
            return ""

        try:
            root = ET.fromstring(document_xml)
        except ET.ParseError:
            return ""

        parts = [segment.strip() for segment in root.itertext() if segment and segment.strip()]
        return " ".join(parts)

    def _extract_pdf_text(self, content: bytes) -> str:
        """Extract text from a PDF, preferring pdfplumber for better table/layout handling.

        Falls back to pypdf when pdfplumber is not installed.
        Returns empty string if no parser is available.
        """
        # Primary: pdfplumber — best table + layout extraction, MIT license
        try:
            import pdfplumber

            with pdfplumber.open(io.BytesIO(content)) as pdf:
                parts: list[str] = []
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    if text.strip():
                        parts.append(text.strip())
                return "\n".join(parts)
        except ImportError:
            pass
        except Exception:
            pass

        # Fallback: pypdf — pure-Python, zero C deps, decent text extraction
        try:
            from pypdf import PdfReader

            reader = PdfReader(io.BytesIO(content))
            pages = [(page.extract_text() or "").strip() for page in reader.pages]
            return "\n".join(page for page in pages if page)
        except ImportError:
            return ""
        except Exception:
            return ""

    def _normalize_analysis_text(self, text: str) -> str:
        """Normalize extracted text for summarization / Q&A flows."""
        return re.sub(r"\s+", " ", text).strip()

    def _tokenize(self, text: str) -> list[str]:
        """Tokenize text for lightweight scoring."""
        tokens = re.findall(r"[A-Za-z0-9ăâîșşțţ-]+", text.lower())
        return [token for token in tokens if len(token) > 2 and token not in STOPWORDS]

    def _split_sentences(self, text: str) -> list[str]:
        """Split text into coarse sentence-like chunks."""
        return [chunk.strip() for chunk in re.split(r"(?<=[.!?])\s+", text) if chunk.strip()]

    def extract_text(self, remote_path: str, max_chars: int = 12000) -> dict[str, Any] | None:
        """Extract readable text from a supported file type."""
        normalized_path = self._normalize_remote_path(remote_path)
        extension = Path(normalized_path).suffix.lower()
        content = self._download_file_bytes(normalized_path)
        if content is None:
            return None

        if extension in TEXT_FILE_EXTENSIONS:
            raw_text = self._decode_text_bytes(content)
        elif extension == ".docx":
            raw_text = self._extract_docx_text(content)
        elif extension == ".pdf":
            raw_text = self._extract_pdf_text(content)
        else:
            print(f"Error extract-text: unsupported file type '{extension or 'unknown'}'")
            return None

        normalized_text = self._normalize_analysis_text(raw_text)
        if not normalized_text:
            print(f"Error extract-text: no readable text extracted from '{normalized_path}'")
            return None

        truncated = len(normalized_text) > max_chars
        final_text = normalized_text[:max_chars].rstrip()
        return {
            "path": normalized_path,
            "extension": extension,
            "text": final_text,
            "char_count": len(normalized_text),
            "truncated": truncated,
        }

    def _build_grounded_summary(self, text: str) -> tuple[str, list[str]]:
        """Build a lightweight grounded summary and highlight list from extracted text."""
        sentences = self._split_sentences(text)
        if not sentences:
            return "", []

        token_counts = Counter(self._tokenize(text))
        ranked: list[tuple[float, int, str]] = []
        for index, sentence in enumerate(sentences):
            sentence_tokens = self._tokenize(sentence)
            if not sentence_tokens:
                score = 0.0
            else:
                score = sum(token_counts[token] for token in sentence_tokens) / len(sentence_tokens)
            ranked.append((score, index, sentence))

        top_sentences = sorted(ranked, key=lambda item: (-item[0], item[1]))[:3]
        ordered_sentences = [item[2] for item in sorted(top_sentences, key=lambda item: item[1])]
        summary = " ".join(ordered_sentences) or " ".join(sentences[:3])
        highlights = [token for token, _count in token_counts.most_common(5)]
        return summary, highlights

    def summarize(self, remote_path: str, max_chars: int = 12000) -> dict[str, Any] | None:
        """Produce a grounded summary for a single file."""
        extracted = self.extract_text(remote_path, max_chars=max_chars)
        if extracted is None:
            return None

        summary, highlights = self._build_grounded_summary(extracted["text"])
        if not summary:
            print("Error summarize: no sentences available after extraction")
            return None

        return {
            "path": extracted["path"],
            "extension": extracted["extension"],
            "summary": summary,
            "highlights": highlights,
            "char_count": extracted["char_count"],
            "truncated": extracted["truncated"],
        }

    def ask_file(
        self,
        remote_path: str,
        question: str,
        max_chars: int = 12000,
    ) -> dict[str, Any] | None:
        """Answer a question using extractive matching over a single file."""
        normalized_question = question.strip()
        if not normalized_question:
            print("Error ask-file: question cannot be empty")
            return None

        extracted = self.extract_text(remote_path, max_chars=max_chars)
        if extracted is None:
            return None

        question_tokens = set(self._tokenize(normalized_question))
        segments = self._split_sentences(extracted["text"])
        if not segments:
            print("Error ask-file: no usable segments extracted from file")
            return None

        scored_segments: list[tuple[float, str]] = []
        for segment in segments:
            segment_tokens = set(self._tokenize(segment))
            overlap = len(question_tokens & segment_tokens)
            score = overlap / max(len(question_tokens), 1)
            scored_segments.append((score, segment))

        scored_segments.sort(key=lambda item: (-item[0], -len(item[1])))
        best_score, best_segment = scored_segments[0]
        supporting_excerpts = [segment for score, segment in scored_segments if score > 0][:3]
        if not supporting_excerpts:
            supporting_excerpts = [best_segment]

        confidence = "low"
        if best_score >= 0.6:
            confidence = "high"
        elif best_score >= 0.3:
            confidence = "medium"

        return {
            "path": extracted["path"],
            "question": normalized_question,
            "answer": best_segment,
            "confidence": confidence,
            "supporting_excerpts": supporting_excerpts,
            "truncated": extracted["truncated"],
        }

    def _extract_due_hint(self, sentence: str) -> str | None:
        """Extract a simple ISO due-date hint from a sentence."""
        match = re.search(r"\b(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})\b", sentence)
        if not match:
            return None

        day = int(match.group(1))
        month_token = match.group(2).lower()
        year = int(match.group(3))
        month = MONTHS.get(month_token)
        if month is None:
            return None

        try:
            return datetime(year, month, day).strftime("%Y-%m-%d")
        except ValueError:
            return None

    def _extract_owner_hint(self, sentence: str) -> str | None:
        """Extract a lightweight owner hint from a sentence."""
        match = re.search(r"\b([A-ZĂÂÎȘȚ][a-zăâîșț]+)\s+(?:should|will|must|owns)\b", sentence)
        return match.group(1) if match else None

    def _infer_priority_hint(self, sentence: str) -> str:
        """Infer a lightweight task priority from urgency language."""
        lowered = sentence.lower()
        if any(token in lowered for token in ("urgent", "immediately", "asap", "today")):
            return "high"
        if self._extract_due_hint(sentence) or "this week" in lowered or "follow up" in lowered or "follow-up" in lowered:
            return "medium"
        return "normal"

    def _estimate_action_confidence(
        self,
        sentence: str,
        due_hint: str | None,
        owner_hint: str | None,
    ) -> str:
        """Estimate confidence for an extracted action using lightweight heuristics."""
        lowered = sentence.lower()
        score = 0.45
        if any(keyword in lowered for keyword in ACTION_KEYWORDS):
            score += 0.2
        if due_hint:
            score += 0.2
        if owner_hint:
            score += 0.1
        if re.match(r"^(please\s+)?(send|review|create|prepare|reply|schedule|confirm|approve)\b", lowered):
            score += 0.1

        if score >= 0.8:
            return "high"
        if score >= 0.55:
            return "medium"
        return "low"

    def _classify_document_type(self, remote_path: str, text: str) -> str:
        """Classify a document into a coarse workflow-relevant type."""
        haystack = f"{Path(remote_path).name.lower()}\n{text.lower()}"
        if any(token in haystack for token in ("meeting", "minutes", "meeting notes", "proces verbal", "process-verbal")):
            return "meeting-notes"
        if any(token in haystack for token in ("contract", "agreement", "renewal", "clause")):
            return "contract"
        if any(token in haystack for token in ("offer", "proposal", "quote", "pricing")):
            return "offer"
        if any(token in haystack for token in ("brief", "instruction", "memo")):
            return "brief"
        return "unknown"

    def _make_action_title(self, sentence: str) -> str:
        """Turn a sentence into a short task title."""
        title = sentence.strip().rstrip(".?!")
        title = re.sub(r"^please\s+", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s+by\s+\d{1,2}\s+[A-Za-z]+\s+\d{4}$", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s+this\s+week$", "", title, flags=re.IGNORECASE)
        title = re.sub(r"\s+for\s+approval$", "", title, flags=re.IGNORECASE)
        if title:
            title = title[0].upper() + title[1:]
        return title

    def _build_action_payload(self, index: int, sentence: str) -> dict[str, Any]:
        """Convert a source sentence into a structured action proposal."""
        due_hint = self._extract_due_hint(sentence)
        owner_hint = self._extract_owner_hint(sentence)
        priority_hint = self._infer_priority_hint(sentence)
        confidence = self._estimate_action_confidence(sentence, due_hint, owner_hint)

        return {
            "index": index,
            "title": self._make_action_title(sentence),
            "reason": "Explicit action phrase found in source sentence.",
            "details": sentence,
            "due_hint": due_hint,
            "owner_hint": owner_hint,
            "source_excerpt": sentence,
            "evidence": [sentence],
            "due_date": {
                "value": due_hint,
                "source": "inferred" if due_hint else "missing",
            },
            "owner": {
                "value": owner_hint,
                "source": "inferred" if owner_hint else "missing",
            },
            "priority": {
                "value": priority_hint,
                "source": "inferred",
            },
            "confidence": confidence,
        }

    def extract_actions(self, remote_path: str, max_chars: int = 12000) -> dict[str, Any] | None:
        """Extract grounded action suggestions from one file."""
        extracted = self.extract_text(remote_path, max_chars=max_chars)
        if extracted is None:
            return None

        summary, highlights = self._build_grounded_summary(extracted["text"])
        actions: list[dict[str, Any]] = []
        for sentence in self._split_sentences(extracted["text"]):
            lowered = sentence.lower()
            if not any(keyword in lowered for keyword in ACTION_KEYWORDS):
                continue

            payload = self._build_action_payload(len(actions) + 1, sentence)
            if not payload["title"]:
                continue
            actions.append(payload)

        return {
            "path": extracted["path"],
            "document_type": self._classify_document_type(extracted["path"], extracted["text"]),
            "summary": summary,
            "highlights": highlights,
            "count": len(actions),
            "actions": actions,
            "preview_required": True,
            "truncated": extracted["truncated"],
        }

    def _select_actions(
        self,
        actions: list[dict[str, Any]],
        selected_indexes: list[int] | None,
    ) -> tuple[list[dict[str, Any]], list[int]]:
        """Select approved action proposals by 1-based index."""
        if not selected_indexes:
            return actions, []

        selected = {index for index in selected_indexes if index > 0}
        chosen = [action for action in actions if action.get("index") in selected]
        invalid = sorted(index for index in selected if index not in {action.get("index") for action in actions})
        return chosen, invalid

    def create_tasks_from_file(
        self,
        remote_path: str,
        mailbox: str | None = None,
        priority: str = "normal",
        dry_run: bool | None = None,
        execute: bool = False,
        selected_indexes: list[int] | None = None,
    ) -> dict[str, Any] | None:
        """Preview or create Exchange tasks from actions extracted from one file."""
        if dry_run is not None:
            execute = not dry_run

        extracted = self.extract_actions(remote_path)
        if extracted is None:
            return None

        selected_actions, invalid_indexes = self._select_actions(extracted["actions"], selected_indexes)
        default_mailbox = mailbox or "default-mailbox"
        task_proposals: list[dict[str, Any]] = []
        for action in selected_actions:
            effective_priority = priority if priority != "normal" else action["priority"]["value"]
            task_proposals.append(
                {
                    "index": action["index"],
                    "subject": action["title"],
                    "reason": action["reason"],
                    "source_excerpt": action["source_excerpt"],
                    "evidence": action["evidence"],
                    "due_date": action["due_date"],
                    "owner": action["owner"],
                    "priority": {
                        "value": effective_priority,
                        "source": "override" if priority != "normal" else action["priority"]["source"],
                    },
                    "confidence": action["confidence"],
                    "selected": True,
                }
            )

        if not execute:
            return {
                "path": extracted["path"],
                "document_type": extracted["document_type"],
                "summary": extracted["summary"],
                "highlights": extracted["highlights"],
                "preview_required": True,
                "mode": "preview",
                "mailbox": default_mailbox,
                "dry_run": True,
                "execute": False,
                "proposal_count": len(task_proposals),
                "selected_indexes": [proposal["index"] for proposal in task_proposals],
                "invalid_indexes": invalid_indexes,
                "tasks": task_proposals,
            }

        account = get_exchange_account(mailbox)
        created_tasks: list[dict[str, Any]] = []
        priority_map = {"low": "Low", "normal": "Normal", "high": "High"}

        for proposal in task_proposals:
            body_lines = [
                f"Source file: {extracted['path']}",
                f"Reason: {proposal['reason']}",
                f"Source excerpt: {proposal['source_excerpt']}",
                f"Confidence: {proposal['confidence']}",
            ]
            if proposal["owner"]["value"]:
                body_lines.append(f"Owner hint ({proposal['owner']['source']}): {proposal['owner']['value']}")
            if proposal["due_date"]["value"]:
                body_lines.append(f"Due date ({proposal['due_date']['source']}): {proposal['due_date']['value']}")

            task = build_exchange_task(account, proposal["subject"], "\n".join(body_lines))
            task.importance = priority_map.get(proposal["priority"]["value"], "Normal")
            if proposal["due_date"]["value"]:
                task.due_date = build_ews_date(proposal["due_date"]["value"])
            task.save()

            created_tasks.append(
                {
                    "index": proposal["index"],
                    "subject": proposal["subject"],
                    "due_date": proposal["due_date"],
                    "owner": proposal["owner"],
                    "priority": proposal["priority"],
                    "mailbox": str(getattr(account, "primary_smtp_address", mailbox or "")),
                    "id": getattr(task, "id", None),
                }
            )

        return {
            "path": extracted["path"],
            "document_type": extracted["document_type"],
            "summary": extracted["summary"],
            "highlights": extracted["highlights"],
            "mode": "execute",
            "mailbox": str(getattr(account, "primary_smtp_address", mailbox or "")),
            "dry_run": False,
            "execute": True,
            "created_count": len(created_tasks),
            "selected_indexes": [proposal["index"] for proposal in task_proposals],
            "invalid_indexes": invalid_indexes,
            "tasks": created_tasks,
        }


def print_json(data: Any) -> None:
    """Print data as formatted JSON."""
    print(json.dumps(data, indent=2))


def print_list(results: list[dict[str, Any]]) -> None:
    """Print list results in a readable table or JSON."""
    if _JSON_OUTPUT:
        print_json({"ok": True, "count": len(results), "items": results})
        return

    if not results:
        print("(empty)")
        return

    max_name = max(len(item["name"]) for item in results)
    max_type = 6
    max_size = 10
    print(f"{'Name':<{max_name}} {'Type':<{max_type}} {'Size':>{max_size}} {'Modified'}")
    print("-" * (max_name + max_type + max_size + 30))

    folders = sorted((item for item in results if item["type"] == "folder"), key=lambda item: item["name"])
    files = sorted((item for item in results if item["type"] == "file"), key=lambda item: item["name"])

    for item in [*folders, *files]:
        size = str(item["size"]) if item["type"] == "file" else "-"
        modified = item["modified"][:19] if len(item["modified"]) > 19 else item["modified"]
        print(f"{item['name']:<{max_name}} {item['type']:<{max_type}} {size:>{max_size}} {modified}")


def print_info(info: dict[str, Any] | None) -> None:
    """Print a single-item info payload."""
    if _JSON_OUTPUT:
        print_json({"ok": True, "info": info} if info else {"ok": False, "error": "No info available"})
        return

    if not info:
        print("No info available")
        return

    print(f"Name:      {info.get('name', 'Unknown')}")
    print(f"Type:      {info.get('type', 'Unknown')}")
    print(f"Size:      {info.get('size', 0)} bytes")
    print(f"Modified:  {info.get('modified', 'Unknown')}")
    print(f"MIME:      {info.get('mime_type', 'N/A')}")
    print(f"ETag:      {info.get('etag', 'N/A')}")
    print(f"File ID:   {info.get('file_id', 'N/A')}")


def print_shared(shares: list[dict[str, Any]]) -> None:
    """Print items shared with the current user."""
    if _JSON_OUTPUT:
        print_json({"ok": True, "count": len(shares), "shares": shares})
        return

    if not shares:
        print("No shared folders found.")
        return

    max_name = max(max(len(share.get("name", "")) for share in shares), 10)
    max_owner = max(
        max(len(share.get("owner_display", share.get("owner", "Unknown"))) for share in shares),
        10,
    )
    max_perms = max(max(len(share.get("permissions", "")) for share in shares), 10)

    print("\n📁 Shared with me:")
    print(f"{'Name':<{max_name}}  {'Owner':<{max_owner}}  {'Permissions':<{max_perms}}  {'Path'}")
    print("-" * (max_name + max_owner + max_perms + 50))

    for share in sorted(shares, key=lambda item: item.get("name", "")):
        owner = share.get("owner_display", share.get("owner", "Unknown"))
        permissions = share.get("permissions", "unknown")
        print(
            f"{share.get('name', 'Unknown'):<{max_name}}  "
            f"{owner:<{max_owner}}  "
            f"{permissions:<{max_perms}}  "
            f"{share.get('path', '/')}"
        )


def print_share_links(links: list[dict[str, Any]]) -> None:
    """Print public share links."""
    if _JSON_OUTPUT:
        print_json({"ok": True, "count": len(links), "links": links})
        return

    if not links:
        print("No public share links found.")
        return

    max_id = max(max(len(link.get("id", "")) for link in links), 2)
    max_path = max(max(len(link.get("path", "")) for link in links), 4)
    print(f"{'ID':<{max_id}}  {'Path':<{max_path}}  {'Permissions':<18}  {'URL'}")
    print("-" * (max_id + max_path + 60))

    for link in links:
        print(
            f"{link.get('id', ''):<{max_id}}  "
            f"{link.get('path', ''):<{max_path}}  "
            f"{link.get('permissions', 'unknown'):<18}  "
            f"{link.get('url', '')}"
        )


def _parse_share_create_args(args: list[str]) -> tuple[str | None, dict[str, Any]]:
    """Parse `share-create` arguments from a simple argv list."""
    if not args:
        return None, {}

    remote_path = args[0]
    options: dict[str, Any] = {
        "password": None,
        "expire_date": None,
        "public_upload": False,
    }

    index = 1
    while index < len(args):
        token = args[index]
        if token == "--password" and index + 1 < len(args):
            options["password"] = args[index + 1]
            index += 2
            continue
        if token == "--expire-date" and index + 1 < len(args):
            options["expire_date"] = args[index + 1]
            index += 2
            continue
        if token == "--public-upload":
            options["public_upload"] = True
            index += 1
            continue
        print(f"Unknown share-create option: {token}")
        return None, {}

    return remote_path, options


def print_usage() -> None:
    """Print usage information for the standalone Nextcloud module CLI."""
    if _JSON_OUTPUT:
        print(json.dumps({"error": "No command specified", "usage": "nextcloud <command> [options] [--json]", "code": 1}))
        return
    print("Nextcloud WebDAV Client")
    print()
    print("Usage: nextcloud.py <command> [arguments]")
    print()
    print("Commands:")
    print("  list [remote_path] [--recursive]      List files in directory")
    print("  search <query> [remote_path]          Search files/folders by name")
    print("  upload <local> <remote>               Upload file")
    print("  download <remote> <local>             Download file")
    print("  extract-text <remote_path>            Extract readable text")
    print("  summarize <remote_path>               Summarize one file")
    print("  ask-file <remote_path> <question>     Answer a question from one file")
    print("  extract-actions <remote_path>         Extract workflow actions from one file")
    print("  create-tasks-from-file <path> [options]  Preview or create Exchange tasks from one file")
    print("  mkdir <remote_path>                   Create directory")
    print("  delete <remote_path>                  Delete file or directory")
    print("  move <source> <dest>                  Move/rename")
    print("  copy <source> <dest>                  Copy file or directory")
    print("  info <remote_path>                    Get file/directory info")
    print("  shared                                List items shared with me")
    print("  share-create <path> [options]         Create public share link")
    print("  share-list [remote_path]              List public share links")
    print("  share-revoke <share_id>               Revoke public share link")
    print()
    print("Options for share-create:")
    print("  --password <value>                    Protect link with password")
    print("  --expire-date YYYY-MM-DD              Set link expiry date")
    print("  --public-upload                       Allow public upload on folder shares")
    print()
    print("Options for create-tasks-from-file:")
    print("  --mailbox <email>                     Target delegate mailbox for created tasks")
    print("  --priority <low|normal|high>          Override task priority (default: inferred/normal)")
    print("  --select <1,2,...>                    Only create selected proposal indexes")
    print("  --execute                             Actually create tasks after preview")
    print("  --dry-run                             Alias for preview-only mode")
    print()
    print(
        "Set environment variables: NEXTCLOUD_URL, NEXTCLOUD_USERNAME, "
        "NEXTCLOUD_APP_PASSWORD"
    )


def run_cli(argv: list[str] | None = None) -> int:
    """Run the standalone Nextcloud CLI and return an exit code."""
    global _JSON_OUTPUT
    args = argv if argv is not None else sys.argv[1:]

    # Strip --json from args
    if "--json" in args:
        _JSON_OUTPUT = True
        args = [a for a in args if a != "--json"]

    # Strip global --yes and set module-level auto-approval
    if "--yes" in args or "-y" in args:
        global _AUTO_APPROVED
        _AUTO_APPROVED = True
        args = [a for a in args if a not in ("--yes", "-y")]

    if not args:
        print_usage()
        return 1

    command = args[0].lower()

    try:
        client = NextcloudClient()
    except EnvironmentError as exc:
        if _JSON_OUTPUT:
            print(json.dumps({"error": str(exc), "code": 1}))
        else:
            print(str(exc))
        return 1

    command_args = args[1:]

    if command == "list":
        recursive = "--recursive" in command_args
        clean_args = [arg for arg in command_args if arg != "--recursive"]
        remote_path = clean_args[0] if clean_args else "/"
        results = client.list(remote_path, recursive=recursive)
        if results is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to list directory", "code": 3}))
            return 3
        print_list(results)
        return 0

    if command == "search":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py search <query> [remote_path]", "code": 1}))
            else:
                print("Usage: nextcloud.py search <query> [remote_path]")
            return 1
        query = command_args[0]
        remote_path = command_args[1] if len(command_args) > 1 else "/"
        results = client.search(query, remote_path)
        if results is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Search failed", "code": 3}))
            return 3
        print_list(results)
        return 0

    if command == "upload":
        if len(command_args) < 2:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py upload <local_path> <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py upload <local_path> <remote_path>")
            return 1
        result = client.upload(command_args[0], command_args[1])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "local_path": command_args[0], "remote_path": command_args[1]}))
            else:
                print(json.dumps({"error": "Upload failed", "code": 3}))
        return 0 if result else 3

    if command == "download":
        if len(command_args) < 2:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py download <remote_path> <local_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py download <remote_path> <local_path>")
            return 1
        result = client.download(command_args[0], command_args[1])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "remote_path": command_args[0], "local_path": command_args[1]}))
            else:
                print(json.dumps({"error": "Download failed", "code": 3}))
        return 0 if result else 3

    if command == "extract-text":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py extract-text <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py extract-text <remote_path>")
            return 1
        result = client.extract_text(command_args[0])
        if result is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to extract text", "code": 3}))
            return 3
        print_json(result)
        return 0

    if command == "summarize":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py summarize <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py summarize <remote_path>")
            return 1
        result = client.summarize(command_args[0])
        if result is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to summarize", "code": 3}))
            return 3
        print_json(result)
        return 0

    if command == "ask-file":
        if len(command_args) < 2:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py ask-file <remote_path> <question>", "code": 1}))
            else:
                print("Usage: nextcloud.py ask-file <remote_path> <question>")
            return 1
        result = client.ask_file(command_args[0], " ".join(command_args[1:]))
        if result is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to answer question", "code": 3}))
            return 3
        print_json(result)
        return 0

    if command == "extract-actions":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py extract-actions <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py extract-actions <remote_path>")
            return 1
        result = client.extract_actions(command_args[0])
        if result is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to extract actions", "code": 3}))
            return 3
        print_json(result)
        return 0

    if command == "create-tasks-from-file":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py create-tasks-from-file <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py create-tasks-from-file <remote_path>")
            return 1
        remote_path = command_args[0]
        mailbox = None
        priority = "normal"
        execute = False
        selected_indexes: list[int] | None = None
        index = 1
        while index < len(command_args):
            token = command_args[index]
            if token == "--mailbox" and index + 1 < len(command_args):
                mailbox = command_args[index + 1]
                index += 2
                continue
            if token == "--priority" and index + 1 < len(command_args):
                priority = command_args[index + 1]
                index += 2
                continue
            if token == "--select" and index + 1 < len(command_args):
                raw_indexes = [part.strip() for part in command_args[index + 1].split(",") if part.strip()]
                try:
                    selected_indexes = [int(part) for part in raw_indexes]
                except ValueError:
                    msg = "Invalid --select value. Use a comma-separated list like: 1,2,3"
                    if _JSON_OUTPUT:
                        print(json.dumps({"error": msg, "code": 1}))
                    else:
                        print(msg)
                    return 1
                index += 2
                continue
            if token == "--execute":
                execute = True
                index += 1
                _confirm_or_die(f"Execute task creation from {remote_path}")
                continue
            if token == "--dry-run":
                execute = False
                index += 1
                continue
            msg = f"Unknown create-tasks-from-file option: {token}"
            if _JSON_OUTPUT:
                print(json.dumps({"error": msg, "code": 1}))
            else:
                print(msg)
            return 1
        result = client.create_tasks_from_file(
            remote_path,
            mailbox=mailbox,
            priority=priority,
            execute=execute,
            selected_indexes=selected_indexes,
        )
        if result is None:
            return 3
        print_json(result)
        return 0

    if command == "mkdir":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py mkdir <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py mkdir <remote_path>")
            return 1
        result = client.mkdir(command_args[0])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "path": command_args[0]}))
            else:
                print(json.dumps({"error": "Failed to create directory", "code": 3}))
        return 0 if result else 3

    if command == "delete":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py delete <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py delete <remote_path>")
            return 1
        _confirm_or_die(f"Delete Nextcloud file/dir {command_args[0]}")
        result = client.delete(command_args[0])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "path": command_args[0]}))
            else:
                print(json.dumps({"error": "Failed to delete", "code": 3}))
        return 0 if result else 3

    if command == "move":
        if len(command_args) < 2:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py move <source_path> <dest_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py move <source_path> <dest_path>")
            return 1
        _confirm_or_die(f"Move/rename Nextcloud file {command_args[0]} -> {command_args[1]}")
        result = client.move(command_args[0], command_args[1])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "source": command_args[0], "dest": command_args[1]}))
            else:
                print(json.dumps({"error": "Failed to move", "code": 3}))
        return 0 if result else 3

    if command == "copy":
        if len(command_args) < 2:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py copy <source_path> <dest_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py copy <source_path> <dest_path>")
            return 1
        _confirm_or_die(f"Copy Nextcloud file {command_args[0]} -> {command_args[1]}")
        result = client.copy(command_args[0], command_args[1])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "source": command_args[0], "dest": command_args[1]}))
            else:
                print(json.dumps({"error": "Failed to copy", "code": 3}))
        return 0 if result else 3

    if command == "info":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py info <remote_path>", "code": 1}))
            else:
                print("Usage: nextcloud.py info <remote_path>")
            return 1
        info = client.info(command_args[0])
        if info is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to get info", "code": 4}))
            return 4
        print_info(info)
        return 0

    if command == "shared":
        print_shared(client.get_shared_with_me())
        return 0

    if command == "share-create":
        remote_path, options = _parse_share_create_args(command_args)
        if remote_path is None:
            msg = "Usage: nextcloud.py share-create <remote_path> [--password VALUE] [--expire-date YYYY-MM-DD] [--public-upload]"
            if _JSON_OUTPUT:
                print(json.dumps({"error": msg, "code": 1}))
            else:
                print(msg)
            return 1
        result = client.create_share_link(remote_path, **options)
        if result is None:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Failed to create share link", "code": 3}))
            return 3
        print_json(result)
        return 0

    if command == "share-list":
        remote_path = command_args[0] if command_args else None
        print_share_links(client.list_share_links(remote_path))
        return 0

    if command == "share-revoke":
        if not command_args:
            if _JSON_OUTPUT:
                print(json.dumps({"error": "Usage: nextcloud.py share-revoke <share_id>", "code": 1}))
            else:
                print("Usage: nextcloud.py share-revoke <share_id>")
            return 1
        _confirm_or_die(f"Revoke Nextcloud share link {command_args[0]}")
        result = client.revoke_share_link(command_args[0])
        if _JSON_OUTPUT:
            if result:
                print(json.dumps({"ok": True, "share_id": command_args[0]}))
            else:
                print(json.dumps({"error": "Failed to revoke share link", "code": 3}))
        return 0 if result else 3

    msg = f"Unknown command: {command}"
    if _JSON_OUTPUT:
        print(json.dumps({"error": msg, "code": 1}))
    else:
        print(msg)
    return 1


def main() -> None:
    """Main entry point."""
    sys.exit(run_cli())


if __name__ == "__main__":
    main()
