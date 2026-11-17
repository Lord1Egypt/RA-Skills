"""Versioned evaluation corpora with deterministic sampling (v0.6).

A :class:`Corpus` is a versioned, hash-addressed collection of evaluation items
(prompts, probes, questions). Determinism is the whole point: :meth:`Corpus.sample`
is seeded, so a given ``(corpus, seed, n)`` always yields the exact same subset —
the reproducibility property the audit report (dimension 9) demands.

Corpora are loaded from plain JSON so they can be versioned in the repository
and re-hashed by a third party.
"""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class CorpusError(ValueError):
    """Raised for malformed corpus payloads or schema violations."""


def _canonical(obj: Any) -> str:
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str
    )


@dataclass(frozen=True)
class CorpusItem:
    id: str
    payload: dict[str, Any] = field(default_factory=dict)
    labels: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "payload": dict(self.payload), "labels": dict(self.labels)}


@dataclass
class Corpus:
    """A versioned, hash-addressed evaluation corpus."""

    id: str
    version: str
    items: list[CorpusItem]
    lang: str = "en"

    def __post_init__(self) -> None:
        if not self.id:
            raise CorpusError("corpus id is required")
        if not self.version:
            raise CorpusError("corpus version is required")
        seen: set[str] = set()
        for item in self.items:
            if item.id in seen:
                raise CorpusError(f"duplicate item id: {item.id}")
            seen.add(item.id)

    def __len__(self) -> int:
        return len(self.items)

    def digest(self) -> str:
        """SHA-256 over the canonical corpus payload — a version fingerprint."""
        blob = _canonical(
            {
                "id": self.id,
                "version": self.version,
                "lang": self.lang,
                "items": [item.to_dict() for item in self.items],
            }
        )
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def sample(self, n: int, seed: int = 0) -> list[CorpusItem]:
        """Deterministically sample ``n`` items (same seed -> same subset)."""
        if n <= 0:
            raise CorpusError("sample size must be > 0")
        if n >= len(self.items):
            return list(self.items)
        rng = random.Random(seed)
        idxs = sorted(rng.sample(range(len(self.items)), n))
        return [self.items[i] for i in idxs]

    def filter(self, **labels: Any) -> "Corpus":
        """Return a sub-corpus whose items match all given label key/values."""
        kept = [
            it for it in self.items
            if all(it.labels.get(k) == v for k, v in labels.items())
        ]
        return Corpus(
            id=f"{self.id}:filtered", version=self.version, items=kept, lang=self.lang
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "lang": self.lang,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Corpus":
        if not isinstance(data, dict):
            raise CorpusError("corpus payload must be a mapping")
        try:
            raw_items = data.get("items", [])
            items = [
                CorpusItem(
                    id=str(d["id"]),
                    payload=dict(d.get("payload", {})),
                    labels=dict(d.get("labels", {})),
                )
                for d in raw_items
            ]
            return cls(
                id=str(data["id"]),
                version=str(data["version"]),
                items=items,
                lang=str(data.get("lang", "en")),
            )
        except (KeyError, TypeError) as exc:
            raise CorpusError(f"malformed corpus payload: {exc}") from exc

    @classmethod
    def from_json(cls, text: str) -> "Corpus":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise CorpusError(f"invalid corpus JSON: {exc}") from exc
        return cls.from_dict(data)

    @classmethod
    def load(cls, path: str | Path) -> "Corpus":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))


__all__ = ["Corpus", "CorpusError", "CorpusItem"]
