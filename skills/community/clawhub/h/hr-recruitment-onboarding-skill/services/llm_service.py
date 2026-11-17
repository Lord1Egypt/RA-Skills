"""OpenAI-compatible requirement generation with bounded retries."""

import json
import os
from collections.abc import Callable
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from hr_recruitment_onboarding_skill.services.rule_based_extractor import (
    sanitize_requirements,
)


REQUIREMENT_KEYS = (
    "education",
    "experience_years",
    "required_skills",
    "preferred_skills",
    "responsibilities",
    "other_requirements",
)
_LIST_REQUIREMENT_KEYS = REQUIREMENT_KEYS[2:]


class ModelGenerationError(Exception):
    """Raised when the configured model cannot produce valid requirements."""


def validate_requirements(requirements: object) -> dict:
    """Return a validated requirement object with the required six-key shape."""
    if not isinstance(requirements, dict) or set(requirements) != set(REQUIREMENT_KEYS):
        raise ValueError("Model response must contain exactly the required fields")

    education = requirements["education"]
    if education is not None and not isinstance(education, str):
        raise ValueError("education must be a string or null")

    experience_years = requirements["experience_years"]
    if experience_years is not None and (
        not isinstance(experience_years, int) or isinstance(experience_years, bool) or experience_years < 0
    ):
        raise ValueError("experience_years must be a non-negative integer or null")

    for key in _LIST_REQUIREMENT_KEYS:
        value = requirements[key]
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"{key} must be a list of strings")

    return sanitize_requirements(
        {key: requirements[key] for key in REQUIREMENT_KEYS}
    )


class LLMService:
    """Generate structured job requirements through an OpenAI-compatible API."""

    def __init__(
        self,
        base_url: str | None,
        model: str | None,
        api_key: str | None,
        transport: Callable[[dict], str] | None = None,
    ) -> None:
        self.base_url = (base_url or "").rstrip("/")
        self.model = model or ""
        self.api_key = api_key or ""
        self.transport = transport or self._default_transport

    @classmethod
    def from_environment(cls) -> "LLMService":
        """Build a service from the optional LLM_* environment variables."""
        return cls(
            os.environ.get("LLM_BASE_URL"),
            os.environ.get("LLM_MODEL"),
            os.environ.get("LLM_API_KEY"),
        )

    def is_configured(self) -> bool:
        """Return whether all connection settings have been supplied."""
        return bool(self.base_url and self.model and self.api_key)

    def _request_body(self, job: dict, system_prompt: str) -> dict:
        return {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(job, ensure_ascii=False)},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

    def _default_transport(self, body: dict) -> str:
        request = Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json; charset=utf-8",
            },
            method="POST",
        )
        with urlopen(request, timeout=30) as response:
            payload: dict[str, Any] = json.loads(response.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"]

    def generate_requirements(self, job: dict, system_prompt: str) -> dict:
        """Generate a validated requirements object, retrying one invalid response."""
        for _ in range(2):
            try:
                content = self.transport(self._request_body(job, system_prompt))
                return validate_requirements(json.loads(content))
            except (
                HTTPError,
                URLError,
                TimeoutError,
                KeyError,
                IndexError,
                TypeError,
                json.JSONDecodeError,
                ValueError,
            ):
                continue
        raise ModelGenerationError("模型未能生成符合要求的职位要求，请稍后重试。")
