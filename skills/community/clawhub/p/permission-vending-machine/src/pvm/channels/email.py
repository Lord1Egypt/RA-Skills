"""SMTP email notification channel."""

import email.mime.multipart
import email.mime.text
import email.utils
import logging
import smtplib
import ssl
from typing import Optional

from .base import NotificationChannel, NotificationResult

logger = logging.getLogger(__name__)


class EmailChannel(NotificationChannel):
    name = "email"

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_addr: str,
        approver_emails: list[str],
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.approver_emails = approver_emails

    def send(
        self,
        message: str,
        approval_token: str,
        *,
        agent_id: Optional[str] = None,
        scope: Optional[str] = None,
        reason: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
        approver_name: Optional[str] = None,
    ) -> NotificationResult:
        full_message = self._format_message(
            message,
            agent_id=agent_id,
            scope=scope,
            reason=reason,
            ttl_minutes=ttl_minutes,
            approval_token=approval_token,
        )
        html_message = self._format_html(
            message,
            agent_id=agent_id,
            scope=scope,
            reason=reason,
            ttl_minutes=ttl_minutes,
            approval_token=approval_token,
        )

        try:
            msg = email.mime.multipart.MIMEMultipart("alternative")
            msg["Subject"] = f"🤖 Agent Permission Request — {agent_id or 'unknown'}"
            msg["From"] = email.utils.formataddr(("PVM Agent", self.from_addr))
            msg["To"] = ", ".join(self.approver_emails)
            msg.attach(email.mime.text.MIMEText(full_message, "plain"))
            msg.attach(email.mime.text.MIMEText(html_message, "html"))

            ctx = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=ctx) as srv:
                srv.login(self.username, self.password)
                srv.sendmail(self.from_addr, self.approver_emails, msg.as_string())

            return NotificationResult(
                channel=self.name,
                success=True,
                message=full_message,
            )
        except Exception as exc:
            logger.exception("Email send failed")
            return NotificationResult(
                channel=self.name,
                success=False,
                message=full_message,
                error=str(exc),
            )

    def _format_html(
        self,
        message: str,
        *,
        agent_id: Optional[str],
        scope: Optional[str],
        reason: Optional[str],
        ttl_minutes: Optional[int],
        approval_token: str,
    ) -> str:
        return f"""<!DOCTYPE html>
<html>
<head><style>
body {{ font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 600px; margin: auto; padding: 20px; }}
.status {{ background: #f0f0f0; padding: 16px; border-radius: 8px; margin: 16px 0; }}
.key {{ font-weight: bold; width: 100px; display: inline-block; }}
.token {{ font-family: monospace; background: #e8e8e8; padding: 4px 8px; border-radius: 4px; }}
.buttons {{ margin-top: 20px; }}
.btn {{ display: inline-block; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; margin-right: 10px; }}
.btn-approve {{ background: #34d399; color: white; }}
.btn-deny {{ background: #f87171; color: white; }}
</style></head>
<body>
<h2>🤖 Agent Permission Request</h2>
<div class="status">
  <div><span class="key">Agent:</span> {agent_id or 'unknown'}</div>
  <div><span class="key">Scope:</span> {scope or 'N/A'}</div>
  <div><span class="key">Reason:</span> {reason or 'N/A'}</div>
  <div><span class="key">Duration:</span> {ttl_minutes}min</div>
</div>
<p>{message}</p>
<p><strong>Approval Token:</strong> <span class="token">{approval_token}</span></p>
<div class="buttons">
  <a href="#" class="btn btn-approve">APPROVE</a>
  <a href="#" class="btn btn-deny">DENY</a>
</div>
<p style="color:#888;font-size:12px;margin-top:30px;">Reply to this email with APPROVE or DENY in the subject or body.</p>
</body>
</html>"""
