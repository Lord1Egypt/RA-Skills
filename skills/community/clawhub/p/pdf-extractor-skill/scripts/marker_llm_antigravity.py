"""Marker LLM service for Antigravity Tools (OpenAI-compatible proxy).

Why this exists:
- marker.services.openai.OpenAIService uses OpenAI's beta 'parse' API
  (client.beta.chat.completions.parse + response_format schema).
- Antigravity Tools' OpenAI-compatible proxy may not fully support that,
  causing non-JSON responses and schema validation failures.

This service forces JSON-only responses and validates them with the
provided Pydantic schema.

Endpoint expected: http://127.0.0.1:8045/v1
"""

from __future__ import annotations

import json
import time
from typing import Annotated, List

import openai
import PIL
from pydantic import BaseModel

from marker.schema.blocks import Block
from marker.services import BaseService


class AntigravityOpenAIService(BaseService):
    openai_base_url: Annotated[
        str, "The base url to use for OpenAI-like models. No trailing slash."
    ] = "http://127.0.0.1:8045/v1"

    openai_model: Annotated[str, "The model name to use for OpenAI-like model."] = (
        "gemini-3-flash"
    )

    openai_api_key: Annotated[str, "The API key to use for the OpenAI-like service."] = ""

    openai_image_format: Annotated[
        str,
        "The image format to use for the OpenAI-like service. Use 'png' for better compatibility.",
    ] = "png"

    def process_images(self, images: List[PIL.Image.Image]) -> List[dict]:
        if isinstance(images, PIL.Image.Image):
            images = [images]

        img_fmt = self.openai_image_format
        return [
            {
                "type": "image_url",
                "image_url": {
                    "url": "data:image/{};base64,{}".format(
                        img_fmt, self.img_to_base64(img, format=img_fmt)
                    ),
                },
            }
            for img in images
        ]

    def __call__(
        self,
        prompt: str,
        image: PIL.Image.Image | List[PIL.Image.Image] | None,
        block: Block | None,
        response_schema: type[BaseModel],
        max_retries: int | None = None,
        timeout: int | None = None,
    ):
        if max_retries is None:
            max_retries = self.max_retries

        if timeout is None:
            timeout = self.timeout

        client = openai.OpenAI(
            api_key=self.openai_api_key,
            base_url=self.openai_base_url,
        )

        image_data = self.format_image_for_llm(image)
        schema_json = response_schema.model_json_schema()

        strict_prompt = (
            prompt
            + "\n\n"
            + "You MUST respond with ONLY valid JSON (no markdown, no code fences, no extra text).\n"
            + "The JSON MUST conform to this JSON Schema:\n"
            + json.dumps(schema_json, ensure_ascii=False)
        )

        messages = [
            {
                "role": "user",
                "content": [
                    *image_data,
                    {"type": "text", "text": strict_prompt},
                ],
            }
        ]

        total_tries = max_retries + 1
        for tries in range(1, total_tries + 1):
            try:
                response = client.chat.completions.create(
                    extra_headers={
                        "X-Title": "Marker",
                        "HTTP-Referer": "https://github.com/datalab-to/marker",
                    },
                    model=self.openai_model,
                    messages=messages,
                    timeout=timeout,
                    response_format={"type": "json_object"},
                    max_tokens=self.max_output_tokens,
                )

                response_text = response.choices[0].message.content or "{}"
                data = json.loads(response_text)

                # Validate with the schema Marker requested.
                validated = response_schema.model_validate(data)

                if block and getattr(response, "usage", None):
                    block.update_metadata(
                        llm_tokens_used=response.usage.total_tokens,
                        llm_request_count=1,
                    )

                return validated.model_dump()

            except Exception:
                if tries == total_tries:
                    break
                time.sleep(tries * self.retry_wait_time)

        return {}
