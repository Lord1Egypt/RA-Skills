#!/usr/bin/env python3
"""
XML Protocol for Multi-Agent communication.

Implements the task notification protocol from Claude Code Coordinator Mode:
- XML-based messages for Coordinator <-> Worker communication
- Structured status reporting
- Usage tracking
"""

import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, Optional, Any


@dataclass
class TaskNotification:
    """Structured task notification"""
    task_id: str
    status: str  # completed, failed, killed, running
    summary: str
    result: str = ""
    total_tokens: int = 0
    tool_uses: int = 0
    duration_ms: int = 0
    
    def to_xml(self) -> str:
        """Convert to XML format"""
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<task-notification>
  <task-id>{self.task_id}</task-id>
  <status>{self.status}</status>
  <summary>{self.escape_xml(self.summary)}</summary>
  <result>{self.escape_xml(self.result)}</result>
  <usage>
    <total-tokens>{self.total_tokens}</total-tokens>
    <tool-uses>{self.tool_uses}</tool-uses>
    <duration-ms>{self.duration_ms}</duration-ms>
  </usage>
</task-notification>"""
    
    @staticmethod
    def from_xml(xml_text: str) -> Optional["TaskNotification"]:
        """Parse from XML format"""
        try:
            root = ET.fromstring(xml_text)
            if root.tag != "task-notification":
                return None
            
            usage_elem = root.find("usage")
            if usage_elem is not None:
                total_tokens = int(usage_elem.findtext("total-tokens", "0"))
                tool_uses = int(usage_elem.findtext("tool-uses", "0"))
                duration_ms = int(usage_elem.findtext("duration-ms", "0"))
            else:
                total_tokens = tool_uses = duration_ms = 0
            
            return TaskNotification(
                task_id=root.findtext("task-id", ""),
                status=root.findtext("status", ""),
                summary=root.findtext("summary", ""),
                result=root.findtext("result", ""),
                total_tokens=total_tokens,
                tool_uses=tool_uses,
                duration_ms=duration_ms
            )
        except ET.ParseError:
            return None
    
    @staticmethod
    def escape_xml(text: str) -> str:
        """Escape XML special characters"""
        return (text
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&apos;"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "task_id": self.task_id,
            "status": self.status,
            "summary": self.summary,
            "result": self.result,
            "usage": {
                "total_tokens": self.total_tokens,
                "tool_uses": self.tool_uses,
                "duration_ms": self.duration_ms
            }
        }


class MessageRouter:
    """
    Routes messages between Coordinator and Workers.
    
    Supports:
    - Point-to-point: Coordinator -> specific Worker
    - Broadcast: Coordinator -> all Workers
    - Peer-to-peer: Worker -> Worker (via Coordinator relay)
    """
    
    def __init__(self):
        self.pending_messages: Dict[str, list] = {}  # worker_id -> messages
    
    def send_to(self, worker_id: str, message: str, from_id: str = "coordinator"):
        """Send message to specific worker"""
        if worker_id not in self.pending_messages:
            self.pending_messages[worker_id] = []
        
        self.pending_messages[worker_id].append({
            "from": from_id,
            "content": message,
            "timestamp": "2024-01-01T00:00:00Z"  # Would use actual timestamp
        })
    
    def broadcast(self, message: str, from_id: str = "coordinator", exclude: Optional[list] = None):
        """Broadcast message to all workers"""
        exclude = exclude or []
        for worker_id in self.pending_messages:
            if worker_id not in exclude:
                self.send_to(worker_id, message, from_id)
    
    def get_messages(self, worker_id: str) -> list:
        """Get pending messages for a worker"""
        messages = self.pending_messages.get(worker_id, [])
        self.pending_messages[worker_id] = []  # Clear after reading
        return messages
    
    def format_message_xml(self, from_id: str, content: str) -> str:
        """Format a message as XML"""
        return f"""<message>
  <from>{from_id}</from>
  <content>{TaskNotification.escape_xml(content)}</content>
</message>"""


# Message type constants
MESSAGE_TYPES = {
    "NOTIFICATION": "task-notification",
    "MESSAGE": "message",
    "SHUTDOWN_REQUEST": "shutdown-request",
    "SHUTDOWN_RESPONSE": "shutdown-response",
    "PLAN_APPROVAL_REQUEST": "plan-approval-request",
    "PLAN_APPROVAL_RESPONSE": "plan-approval-response"
}


def main():
    """Demo of protocol usage"""
    # Create a notification
    notification = TaskNotification(
        task_id="researcher-abc123",
        status="completed",
        summary="Found 15 relevant files",
        result="Key files: src/main.py, src/utils.py",
        total_tokens=2048,
        tool_uses=5,
        duration_ms=15000
    )
    
    # Convert to XML
    xml = notification.to_xml()
    print("XML Notification:")
    print(xml)
    print()
    
    # Parse back
    parsed = TaskNotification.from_xml(xml)
    if parsed:
        print("Parsed notification:")
        print(f"  Task ID: {parsed.task_id}")
        print(f"  Status: {parsed.status}")
        print(f"  Summary: {parsed.summary}")
        print(f"  Tool uses: {parsed.tool_uses}")


if __name__ == "__main__":
    main()
