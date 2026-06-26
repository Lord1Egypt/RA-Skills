# 模块说明：RAG检索层-工具
# - skill 内部共享的检索文本构造和 retriever 工具。
# - 给 retrieve_cases.py 和 pipeline 共用。

from __future__ import annotations

import json
import os
import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import httpx
except Exception:  # pragma: no cover
    httpx = None

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None

from _skill_time_utils import build_time_feature_payload


UNKNOWN_VALUES = {"", "未知", "未提供", "null", "none", "None"}


@dataclass
class RetrievalResult:
    sample_id: str
    score: float
    conversation: List[Dict[str, Any]]
    is_minor: bool
    icbo_features: Dict[str, Any]
    user_persona: Dict[str, Any]
    source: str


def _normalize_text(text: Any) -> str:
    if not isinstance(text, str):
        return ""
    return " ".join(text.split()).strip()


def conversation_to_user_only_text(conversation: List[Dict[str, Any]]) -> str:
    user_parts: List[str] = []
    fallback_parts: List[str] = []
    for turn in conversation:
        content = _normalize_text(turn.get("content", ""))
        if not content:
            continue
        fallback_parts.append(content)
        if turn.get("role", "user") == "user":
            user_parts.append(content)
    return "\n".join(user_parts or fallback_parts)


def safe_build_time_features(raw_time_hint: str) -> Dict[str, Any]:
    hint = str(raw_time_hint or "").strip()
    if not hint:
        return {}
    try:
        return build_time_feature_payload(hint)
    except Exception:
        return {}


def build_time_tags(
    *,
    raw_time_hint: str = "",
    time_features: Optional[Dict[str, Any]] = None,
) -> List[str]:
    features = dict(time_features or {})
    if not features and raw_time_hint:
        features = safe_build_time_features(raw_time_hint)
    if not features:
        return []

    ordered_fields = [
        "weekday",
        "is_weekend",
        "is_late_night",
        "time_bucket",
        "holiday_label",
        "school_holiday_hint",
    ]
    tags: List[str] = []
    for field_name in ordered_fields:
        value = features.get(field_name)
        if isinstance(value, bool):
            tags.append(f"{field_name}={'true' if value else 'false'}")
            continue
        if value is None:
            continue
        value_text = str(value).strip()
        if not value_text or value_text in UNKNOWN_VALUES:
            continue
        tags.append(f"{field_name}={value_text}")
    return tags


def build_query_retrieval_text(
    conversation: List[Dict[str, Any]],
    *,
    raw_time_hint: str = "",
    time_features: Optional[Dict[str, Any]] = None,
) -> str:
    parts: List[str] = []
    conversation_text = conversation_to_user_only_text(conversation)
    if conversation_text:
        parts.append(conversation_text)

    time_tags = build_time_tags(raw_time_hint=raw_time_hint, time_features=time_features)
    if time_tags:
        parts.append("\n".join(time_tags))

    return "\n".join(part for part in parts if part).strip()


class SkillSemanticRetriever:
    def __init__(
        self,
        *,
        index_path: str,
        corpus_path: str,
        manifest_path: str,
        embedding_model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.index_path = Path(index_path)
        self.corpus_path = Path(corpus_path)
        self.manifest_path = Path(manifest_path)
        self.embedding_model = embedding_model or os.getenv("SKILL_EMBEDDING_MODEL") or "text-embedding-3-small"
        self.api_key = (
            api_key
            or os.getenv("SKILL_EMBEDDING_API_KEY")
            or ""
        )
        self.base_url = (
            base_url
            or os.getenv("SKILL_EMBEDDING_BASE_URL")
            or ""
        ).rstrip("/")
        self.embeddings = None
        self.samples: List[Dict[str, Any]] = []
        self.manifest: Dict[str, Any] = {}
        self.load_index()

    def load_index(self) -> None:
        if not self.index_path.exists():
            raise FileNotFoundError(f"Missing retrieval index: {self.index_path}")

        with open(self.index_path, "rb") as handle:
            index_data = pickle.load(handle)

        self.embeddings = index_data.get("embeddings")
        self.samples = list(index_data.get("samples", []))
        self.manifest = dict(index_data.get("manifest", {}))
        saved_model = index_data.get("embedding_model")
        if saved_model:
            self.embedding_model = str(saved_model)

        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, "r", encoding="utf-8") as handle:
                    self.manifest = json.load(handle)
                source_manifest = self.manifest.get("source_manifest")
                if isinstance(source_manifest, dict) and source_manifest.get("embedding_model"):
                    self.embedding_model = str(source_manifest["embedding_model"])
                elif self.manifest.get("embedding_model"):
                    self.embedding_model = str(self.manifest["embedding_model"])
            except Exception:
                pass

    def _conversation_to_text(self, conversation: List[Dict[str, Any]]) -> str:
        return conversation_to_user_only_text(conversation)

    def _get_embedding(self, text: str):
        if np is None or httpx is None:
            raise RuntimeError("embedding dependencies unavailable")
        if not self.api_key:
            raise RuntimeError("missing embedding api key")
        if not self.base_url:
            raise RuntimeError("missing embedding base url")

        url = f"{self.base_url}/embeddings"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.embedding_model,
            "input": text,
        }

        with httpx.Client(timeout=30.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        embedding = data["data"][0]["embedding"]
        return np.array(embedding, dtype=np.float32)

    def retrieve(
        self,
        conversation: List[Dict[str, Any]],
        *,
        top_k: int = 3,
        threshold: float = 0.0,
        raw_time_hint: str = "",
        time_features: Optional[Dict[str, Any]] = None,
    ) -> List[RetrievalResult]:
        if np is None:
            raise RuntimeError("numpy unavailable")
        if self.embeddings is None or len(self.samples) == 0:
            return []

        query_text = build_query_retrieval_text(
            conversation,
            raw_time_hint=raw_time_hint,
            time_features=time_features,
        )
        if not query_text:
            return []

        query_embedding = self._get_embedding(query_text)
        query_norm = query_embedding / (np.linalg.norm(query_embedding) + 1e-8)
        index_norms = self.embeddings / (np.linalg.norm(self.embeddings, axis=1, keepdims=True) + 1e-8)
        similarities = np.dot(index_norms, query_norm)
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results: List[RetrievalResult] = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score < threshold:
                continue
            sample = self.samples[idx]
            results.append(
                RetrievalResult(
                    sample_id=sample.get("sample_id", f"sample_{idx}"),
                    score=score,
                    conversation=sample.get("conversation", []),
                    is_minor=bool(sample.get("is_minor", True)),
                    icbo_features=sample.get("icbo_features", {}),
                    user_persona=sample.get("user_persona", {}),
                    source=sample.get("source", "unknown"),
                )
            )
        return results

