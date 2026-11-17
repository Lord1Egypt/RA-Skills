"""Expert-score set I/O (module B, v0.6).

Mirrors the measurement layer's corpus design: a versioned, hash-addressed set
of human expert scores, loadable from plain JSON so it can be versioned in the
repository and re-hashed by a third party.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .base import ExpertScore, PanelAgreement, aggregate_panel_agreement


class ScoreSetError(ValueError):
    """Raised for malformed expert-score payloads."""


def _canonical(obj: Any) -> str:
    return json.dumps(
        obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str
    )


@dataclass(frozen=True)
class ExpertScoreSet:
    """A versioned collection of expert scores."""

    id: str
    version: str
    scores: list[ExpertScore]
    lang: str = "en"

    def __post_init__(self) -> None:
        if not self.id:
            raise ScoreSetError("score set id is required")
        if not self.version:
            raise ScoreSetError("score set version is required")

    def __len__(self) -> int:
        return len(self.scores)

    def digest(self) -> str:
        """SHA-256 over the canonical payload — a version fingerprint."""
        blob = _canonical(
            {
                "id": self.id,
                "version": self.version,
                "lang": self.lang,
                "scores": [asdict(s) for s in self.scores],
            }
        )
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    def agreement(self, threshold: float = 0.70) -> PanelAgreement:
        return aggregate_panel_agreement(self.scores, threshold)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "lang": self.lang,
            "scores": [asdict(s) for s in self.scores],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExpertScoreSet":
        if not isinstance(data, dict):
            raise ScoreSetError("score set payload must be a mapping")
        try:
            scores = [
                ExpertScore(
                    item_id=str(d["item_id"]),
                    expert_id=str(d["expert_id"]),
                    dimension=str(d["dimension"]),
                    score=int(d["score"]),
                    rationale=str(d.get("rationale", "")),
                )
                for d in data.get("scores", [])
            ]
            return cls(
                id=str(data["id"]),
                version=str(data["version"]),
                scores=scores,
                lang=str(data.get("lang", "en")),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ScoreSetError(f"malformed score set payload: {exc}") from exc

    @classmethod
    def from_json(cls, text: str) -> "ExpertScoreSet":
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ScoreSetError(f"invalid score set JSON: {exc}") from exc
        return cls.from_dict(data)

    @classmethod
    def load(cls, path: str | Path) -> "ExpertScoreSet":
        return cls.from_json(Path(path).read_text(encoding="utf-8"))

    def dump(self, path: str | Path) -> None:
        Path(path).write_text(
            json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )


__all__ = ["ExpertScoreSet", "ScoreSetError"]
