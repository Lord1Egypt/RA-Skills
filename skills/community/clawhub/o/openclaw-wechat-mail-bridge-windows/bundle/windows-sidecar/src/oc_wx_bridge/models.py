from __future__ import annotations

from pydantic import BaseModel, Field


class IncomingMessage(BaseModel):
    event_id: str
    source: str = "windows-sidecar"
    sidecar_id: str
    platform: str = "wechat-desktop"
    chat_type: str = "group"
    chat_id: str
    chat_name: str
    sender_display_name: str | None = None
    message_id: str
    message_text: str
    message_time: str
    observed_at: str

    def to_bridge_payload(self) -> dict:
        return {
            "eventId": self.event_id,
            "source": self.source,
            "sidecarId": self.sidecar_id,
            "platform": self.platform,
            "chatType": self.chat_type,
            "chatId": self.chat_id,
            "chatName": self.chat_name,
            "senderDisplayName": self.sender_display_name,
            "messageId": self.message_id,
            "messageText": self.message_text,
            "messageTime": self.message_time,
            "observedAt": self.observed_at,
        }


class OutboundCommand(BaseModel):
    command_id: str = Field(alias="commandId")
    chat_id: str = Field(alias="chatId")
    chat_name: str | None = Field(default=None, alias="chatName")
    reply_to_message_id: str | None = Field(default=None, alias="replyToMessageId")
    text: str
    created_at: str = Field(alias="createdAt")


class AdapterHealth(BaseModel):
    ok: bool
    name: str
    detail: str | None = None

