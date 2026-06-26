#!/usr/bin/env python3
from __future__ import annotations

import time
import urllib.parse

from common import GEMINI_API_BASE, http_json_request, is_retryable_error


def embed_texts(
    *,
    api_key: str,
    texts: list[str],
    model: str = "gemini-embedding-001",
    dimensions: int = 384,
) -> list[list[float]]:
    if not texts:
        return []

    clean_model = model.removeprefix("models/")
    url = (
        f"{GEMINI_API_BASE}/models/{urllib.parse.quote(clean_model)}:embedContent"
        f"?key={urllib.parse.quote(api_key)}"
    )

    embeddings: list[list[float]] = []
    for text in texts:
        payload = {
            "model": f"models/{clean_model}",
            "content": {"parts": [{"text": text}]},
            "outputDimensionality": dimensions,
        }
        attempt = 0
        while True:
            attempt += 1
            try:
                response = http_json_request(url, method="POST", json_body=payload, timeout=120)
                embedding = response.get("embedding", {}).get("values") or []
                if not embedding:
                    raise RuntimeError(f"No embedding returned for model {clean_model}")
                embeddings.append(embedding)
                break
            except Exception as exc:
                if attempt > 3 or not is_retryable_error(str(exc)):
                    raise
                time.sleep(min(20, attempt * 2))

    return embeddings


def embed_single(
    *,
    api_key: str,
    text: str,
    model: str = "gemini-embedding-001",
    dimensions: int = 384,
) -> list[float]:
    results = embed_texts(api_key=api_key, texts=[text], model=model, dimensions=dimensions)
    return results[0]
