import json
import time
import uuid
from typing import Any, Optional

import requests


class FastGPTError(RuntimeError):
    pass


class FastGPTClient:
    def __init__(
        self, api_url: str, api_key: str, agent_id: str = "", timeout: int = 60
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.agent_id = agent_id
        self.timeout = timeout
        self.headers = {
            "Authorization": self._normalize_bearer(api_key),
            "Content-Type": "application/json",
        }

    def call(
        self,
        content: str,
        variables: Optional[dict[str, Any]] = None,
        chat_id: Optional[str] = None,
    ) -> str:
        payload_variables = dict(variables or {})
        if self.agent_id:
            payload_variables.setdefault("agent_id", self.agent_id)

        payload: dict[str, Any] = {
            "chatId": chat_id or f"goodsclassify-{int(time.time() * 1000)}",
            "stream": False,
            "detail": False,
            "responseChatItemId": str(uuid.uuid4()),
            "variables": payload_variables,
            "messages": [{"role": "user", "content": content}],
        }
        if self.agent_id:
            payload["appId"] = self.agent_id

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.Timeout as exc:
            raise FastGPTError("FastGPT request timed out") from exc
        except requests.RequestException as exc:
            raise FastGPTError(f"FastGPT request failed: {exc}") from exc

        try:
            result = response.json()
        except ValueError as exc:
            raise FastGPTError(f"FastGPT returned invalid JSON: {response.text}") from exc

        content_text = self._extract_content(result)
        if content_text is None:
            if isinstance(result, (dict, list)):
                return json.dumps(result, ensure_ascii=False)
            raise FastGPTError(f"Unable to parse FastGPT response: {result}")
        return content_text

    def check_phone_exists(self, phone: str, session_id: str) -> bool:
        response = self.call(
            phone,
            variables={},
            chat_id=f"{session_id}-agent-a",
        )
        parsed = self._try_parse_json(response)
        if isinstance(parsed, list):
            return len(parsed) > 0
        if isinstance(parsed, dict):
            if "exists" in parsed:
                return bool(parsed["exists"])
            data = parsed.get("data")
            if isinstance(data, list):
                return len(data) > 0

        normalized = response.strip().lower()
        return (
            "\u4e0d\u5b58\u5728" not in response
            and ("\u5b58\u5728" in response or "exists" in normalized)
        )

    def save_phone(self, phone: str, session_id: str) -> bool:
        response = self.call(
            phone,
            variables={},
            chat_id=f"{session_id}-agent-b",
        )
        parsed = self._try_parse_json(response)
        if isinstance(parsed, dict):
            affected_rows = parsed.get("affectedRows")
            changed_rows = parsed.get("changedRows")
            if isinstance(affected_rows, int) and affected_rows >= 1:
                return True
            if isinstance(changed_rows, int) and changed_rows >= 1:
                return True
            if "error" in parsed or "errors" in parsed:
                return False
            if "choices" in parsed and "id" in parsed:
                return True

        normalized = response.strip().lower()
        return (
            "\u5931\u8d25" not in response
            and ("\u6210\u529f" in response or "success" in normalized)
        )

    def query_product(self, question: str, session_id: str, phone: str) -> str:
        return self.call(
            question,
            variables={"phone": phone, "session_id": session_id},
            chat_id=f"{session_id}-agent-c",
        )

    @staticmethod
    def _extract_content(result: Any) -> Optional[str]:
        if isinstance(result, dict):
            choices = result.get("choices")
            if isinstance(choices, list) and choices:
                message = choices[0].get("message")
                if isinstance(message, dict):
                    content = message.get("content")
                    if isinstance(content, str) and content.strip():
                        return content.strip()

            for key in ("text", "content", "data", "message"):
                value = result.get(key)
                if isinstance(value, str) and value.strip():
                    return value.strip()

        if isinstance(result, str) and result.strip():
            return result.strip()
        return None

    @staticmethod
    def _normalize_bearer(token: str) -> str:
        cleaned = token.strip()
        if cleaned.lower().startswith("bearer "):
            return cleaned
        return f"Bearer {cleaned}"

    @staticmethod
    def _try_parse_json(text: str) -> Optional[Any]:
        try:
            return json.loads(text)
        except Exception:
            return None
