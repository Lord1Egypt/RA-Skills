#!/usr/bin/env python3
"""Dataclass definitions for health check data models."""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class DimResult:
    """Result for a single health dimension."""
    score: int                        # 0-100
    status: str                      # "healthy" | "warning" | "critical"
    value: Any                       # Dimension-specific raw value
    details: dict = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)
    
    def __post_init__(self):
        valid_statuses = {"healthy", "warning", "critical"}
        if self.status not in valid_statuses:
            self.status = "critical"


@dataclass
class Recommendation:
    """An actionable recommendation for improving health."""
    dimension: str                   # Which dimension this relates to
    severity: str                    # "critical" | "warning" | "info"
    action: str                      # Human-readable action description
    auto_repairable: bool            # Can this be auto-repaired?
    cli_command: Optional[str] = None # Optional fix command
    effort: str = "unknown"          # "low" | "medium" | "high"


@dataclass
class ReportMetadata:
    """Metadata about the health report itself."""
    generated_at: str                # ISO timestamp
    openclaw_version: Optional[str] = None
    agent_name: str = "main"
    scan_duration_seconds: float = 0.0
    db_count: int = 0
    file_count: int = 0


@dataclass
class HealthReport:
    """Complete health report across all dimensions."""
    ts: str                           # ISO timestamp
    overall_score: float             # 0-100
    status: str                      # "healthy" | "warning" | "critical"
    dimensions: dict[str, DimResult] = field(default_factory=dict)
    recommendations: list[Recommendation] = field(default_factory=list)
    auto_repair_plan: list[str] = field(default_factory=list)
    metadata: ReportMetadata = None
    
    def to_dict(self) -> dict:
        """Convert to serializable dict."""
        return {
            "ts": self.ts,
            "overall_score": self.overall_score,
            "status": self.status,
            "dimensions": {
                k: {
                    "score": v.score,
                    "status": v.status,
                    "value": v.value,
                    "details": v.details,
                    "issues": v.issues,
                }
                for k, v in self.dimensions.items()
            },
            "recommendations": [
                {
                    "dimension": r.dimension,
                    "severity": r.severity,
                    "action": r.action,
                    "auto_repairable": r.auto_repairable,
                    "cli_command": r.cli_command,
                }
                for r in self.recommendations
            ],
            "auto_repair_plan": self.auto_repair_plan,
            "metadata": {
                "generated_at": self.metadata.generated_at if self.metadata else self.ts,
                "agent_name": self.metadata.agent_name if self.metadata else "main",
                "scan_duration_seconds": self.metadata.scan_duration_seconds if self.metadata else 0.0,
            } if self.metadata else {},
        }


@dataclass
class GrowthRate:
    """Growth rate analysis result."""
    growth_rate_mb_per_week: float
    trend: str                       # "increasing" | "stable" | "decreasing"
    projected_90d_mb: float
    historical_points: int = 0
    method: str = "linear"           # "linear" | "exponential" | "unknown"
