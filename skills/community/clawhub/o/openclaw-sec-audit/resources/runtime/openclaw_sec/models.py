from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


SEVERITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
    "info": 4,
}

CATEGORY_ORDER = {
    "secrets": 0,
    "network": 1,
    "host": 2,
    "filesystem": 3,
    "config": 4,
    "hygiene": 5,
}


@dataclass(slots=True)
class Finding:
    id: str
    title: str
    category: str
    severity: str
    confidence: str
    heuristic: bool
    evidence: list[str]
    risk: str
    recommendation: str
    masked_examples: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class AuditContext:
    config_path: Path
    workspace_path: Path | None
    output_dir: Path
    output_format: str
    enable_git: bool
    enable_host: bool
    strict: bool
    debug: bool
    current_dir: Path


@dataclass(slots=True)
class AuditReport:
    tool: str
    version: str
    mode: str
    generated_at: str
    host: dict[str, Any]
    target: dict[str, Any]
    summary: dict[str, Any]
    findings: list[Finding]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["findings"] = [finding.to_dict() for finding in self.findings]
        return payload
