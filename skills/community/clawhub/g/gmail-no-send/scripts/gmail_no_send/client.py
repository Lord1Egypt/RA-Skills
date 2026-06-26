from __future__ import annotations

import base64
from email.mime.text import MIMEText
from typing import Any, Dict, List, Optional

from googleapiclient.discovery import build

from .auth import authenticate, load_credentials
from .utils import audit_log


class GmailNoSend:
    def __init__(self, account: str, client_secret: Optional[str] = None, force_auth: bool = False):
        self.account = account
        self.client_secret = client_secret
        self.force_auth = force_auth
        self.service = None

    def _service(self):
        if self.service is None:
            creds = load_credentials()
            if not creds or self.force_auth:
                if not self.client_secret:
                    raise ValueError("client_secret is required for first-time auth")
                creds = authenticate(self.client_secret, self.account, force=self.force_auth)
            self.service = build("gmail", "v1", credentials=creds)
        return self.service

    def search(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        audit_log("search", {"account": self.account, "query": query, "max_results": max_results})
        service = self._service()
        resp = service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
        return resp.get("messages", [])

    def read(self, message_id: str) -> Dict[str, Any]:
        audit_log("read", {"account": self.account, "message_id": message_id})
        service = self._service()
        return service.users().messages().get(userId="me", id=message_id, format="full").execute()

    def create_draft(self, to: str, subject: str, body: str) -> Dict[str, Any]:
        audit_log("draft.create", {"account": self.account, "to": to, "subject": subject})
        service = self._service()
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft_body = {"message": {"raw": encoded_message}}
        return service.users().drafts().create(userId="me", body=draft_body).execute()

    def update_draft(self, draft_id: str, to: str, subject: str, body: str) -> Dict[str, Any]:
        audit_log("draft.update", {"account": self.account, "draft_id": draft_id, "to": to, "subject": subject})
        service = self._service()
        message = MIMEText(body)
        message["to"] = to
        message["subject"] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        draft_body = {"id": draft_id, "message": {"raw": encoded_message}}
        return service.users().drafts().update(userId="me", id=draft_id, body=draft_body).execute()

    def archive(self, message_id: str) -> Dict[str, Any]:
        audit_log("archive", {"account": self.account, "message_id": message_id})
        service = self._service()
        body = {"removeLabelIds": ["INBOX"]}
        return service.users().messages().modify(userId="me", id=message_id, body=body).execute()
