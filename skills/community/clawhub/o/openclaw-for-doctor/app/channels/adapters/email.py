import os
import smtplib
from email.message import EmailMessage

from app.channels.base import ChannelAdapter
from app.channels.formatter import format_task_result_message
from app.config import get_settings
from app.core.models import ChannelType, DeliveryReceipt, TaskResult


class EmailAdapter(ChannelAdapter):
    channel = ChannelType.email

    def send_result(self, result: TaskResult) -> DeliveryReceipt:
        settings = get_settings()
        smtp_host = os.getenv("EMAIL_SMTP_HOST", "").strip()
        smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587").strip())
        sender = os.getenv("EMAIL_FROM", "").strip()
        recipient = os.getenv("EMAIL_TO_DEFAULT", "").strip()
        username = os.getenv("EMAIL_USERNAME", "").strip()
        password = os.getenv("EMAIL_PASSWORD", "").strip()

        if not smtp_host or not sender:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail="EMAIL_SMTP_HOST or EMAIL_FROM not configured.",
            )
        if not recipient:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail="EMAIL_TO_DEFAULT is not configured.",
            )
        if not settings.enable_outbound_send:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=True,
                detail="Prepared email payload (outbound send disabled).",
            )

        message = EmailMessage()
        message["From"] = sender
        message["To"] = recipient
        message["Subject"] = f"OpenClaw Doctor Task {result.task_id[:8]}"
        message.set_content(format_task_result_message(result))

        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=settings.webhook_timeout_seconds) as smtp:
                smtp.starttls()
                if username and password:
                    smtp.login(username, password)
                smtp.send_message(message)
        except Exception as exc:
            return DeliveryReceipt(
                channel=self.channel,
                delivered=False,
                detail=f"Email delivery exception: {exc}",
            )

        return DeliveryReceipt(
            channel=self.channel,
            delivered=True,
            detail="Email delivered through configured SMTP relay.",
        )
