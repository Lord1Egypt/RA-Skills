from __future__ import annotations
import os
import re
from typing import Any
import httpx

def scrub_sensitive_data(obj: Any) -> Any:
    """
    Recursively scrub common API key patterns, personal data, and system paths.
    Uses an expanded list of regexes for improved reliability.
    """
    if isinstance(obj, str):
        # 1. API Keys & Tokens
        # Generic high-entropy strings looking like keys
        obj = re.sub(r'([a-zA-Z0-9]{32,})', '[REDACTED_HIGH_ENTROPY_STRING]', obj)
        # Specific formats
        obj = re.sub(r'(sk-[a-zA-Z0-9]{20,})', '[REDACTED_OPENAI_KEY]', obj)
        obj = re.sub(r'(mk_[a-zA-Z0-9]{20,})', '[REDACTED_MYCELIUM_KEY]', obj)
        obj = re.sub(r'(gh[pousr]_[a-zA-Z0-9]{20,})', '[REDACTED_GITHUB_TOKEN]', obj)
        
        # 2. Personal Information
        # Emails
        obj = re.sub(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', '[REDACTED_EMAIL]', obj)
        # IPv4 Addresses
        obj = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[REDACTED_IP]', obj)
        
        # 3. System Paths
        # Local home paths
        user_home = os.path.expanduser("~")
        obj = obj.replace(user_home, "~")
        # Generic absolute paths
        obj = re.sub(r'/[a-zA-Z0-9._/-]+', lambda m: m.group(0) if m.group(0).startswith('/usr/bin') or m.group(0).startswith('/tmp') else '[REDACTED_PATH]', obj)
        
        return obj
    elif isinstance(obj, dict):
        return {k: scrub_sensitive_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [scrub_sensitive_data(x) for x in obj]
    return obj

class MyceliumClient:
    """
    Python SDK for the Mycelium API.
    
    WARNING: The publish() method is restricted and requires human review 
    confirmation to prevent accidental data leakage.
    """

    def __init__(
        self,
        api_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
        agent_id: str | None = None,
    ) -> None:
        self.api_url = (api_url or os.getenv("MYCELIUM_API_URL", "https://mycelium-platform.onrender.com")).rstrip("/")
        self.api_key = api_key or os.getenv("MYCELIUM_API_KEY", "")
        self.timeout = timeout
        self.agent_id = agent_id or os.getenv("OPENCLAW_AGENT_ID", "openclaw_user")
        self._headers = {"X-API-Key": self.api_key, "Content-Type": "application/json"}

    def seek(
        self,
        goal: str,
        scope: str = "task",
        context: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        limit: int = 5,
    ) -> list[dict[str, Any]]:
        payload = {
            "fingerprint": {
                "goal": goal,
                "scope": scope,
                "context": context or {},
                "tags": tags or [],
            },
            "limit": limit,
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(
                f"{self.api_url}/pheromones/match",
                json=payload,
                headers=self._headers,
            )
            resp.raise_for_status()
        return resp.json()["matches"]

    def publish(
        self,
        goal: str,
        path: dict[str, Any],
        scope: str = "task",
        context: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        publisher_handle: str | None = None,
        confirmed: bool = False,
    ) -> str:
        """
        INTERNAL POLICY: This method forces a 'confirmed' check.
        In an autonomous agent context, the agent SHOULD NOT set confirmed=True 
        unless it has received an explicit 'Y' from the user in the current session.
        """
        if not confirmed:
            raise ValueError(
                "SAFETY BREACH: publish() called without 'confirmed=True'. "
                "This method requires human-in-the-loop validation of the data preview."
            )

        # Implementation of the promised scrubbing
        scrubbed_goal = scrub_sensitive_data(goal)
        scrubbed_path = scrub_sensitive_data(path)
        scrubbed_tags = scrub_sensitive_data(tags or [])

        payload = {
            "fingerprint": {
                "goal": scrubbed_goal,
                "scope": scope,
                "context": context or {},
                "tags": scrubbed_tags,
            },
            "path": scrubbed_path,
            "publisher_agent_id": self.agent_id,
            "publisher_handle": publisher_handle,
        }
        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(
                f"{self.api_url}/pheromones",
                json=payload,
                headers=self._headers,
            )
            resp.raise_for_status()
        return resp.json()["id"]

    def feedback(
        self,
        pheromone_id: str,
        result: str,
        source: str = "agent",
    ) -> dict[str, Any]:
        if result not in ("success", "fail", "unknown"):
            raise ValueError(f"result must be 'success', 'fail', or 'unknown', got: {result!r}")
        
        payload: dict[str, Any] = {
            "result": result,
            "source": source,
        }
        if self.agent_id:
            payload["agent_id"] = self.agent_id

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(
                f"{self.api_url}/pheromones/{pheromone_id}/feedback",
                json=payload,
                headers=self._headers,
            )
            resp.raise_for_status()
        return resp.json()
