#!/usr/bin/env python3
"""Assurance policy gates for pipeline verification behavior."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssurancePolicy:
    """Controls fail-open vs fail-closed behavior for file workflows."""

    level: str = "best_effort"
    fail_on_coverage_mismatch: bool = False
    fail_on_residual_findings: bool = False

    @classmethod
    def best_effort(cls) -> "AssurancePolicy":
        return cls(level="best_effort")

    @classmethod
    def verified(cls) -> "AssurancePolicy":
        return cls(
            level="verified",
            fail_on_coverage_mismatch=True,
            fail_on_residual_findings=True,
        )

    @classmethod
    def strict(cls) -> "AssurancePolicy":
        return cls(
            level="strict",
            fail_on_coverage_mismatch=True,
            fail_on_residual_findings=True,
        )

    def with_coverage_enforced(self) -> "AssurancePolicy":
        return AssurancePolicy(
            level=self.level,
            fail_on_coverage_mismatch=True,
            fail_on_residual_findings=self.fail_on_residual_findings,
        )

    def should_verify(self) -> bool:
        return self.level in ("verified", "strict")
