"""Lightweight quality benchmarks for Portfolio Risk Desk."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from datetime import date
import tempfile
from typing import Any

from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_demo_request_payload, load_mock_evidence
from intelligence_desk_brief.orchestrator import PortfolioRiskDesk
from intelligence_desk_brief.providers.base import RetrievalAdapter


@dataclass(frozen=True)
class BenchmarkResult:
    name: str
    score: int
    max_score: int
    checks: dict[str, bool]


class _DegradedRetrievalAdapter(RetrievalAdapter):
    def collect(self, request: CreateBriefRequest) -> list[dict[str, Any]]:
        del request
        payload = deepcopy(load_mock_evidence())
        return [
            payload[-1],
            {
                "id": "retrieval-notice-degraded",
                "item_type": "retrieval_notice",
                "category": "retrieval_status",
                "source_title": "Benchmark degraded retrieval notice",
                "url": "https://openclaw.local/degraded-benchmark",
                "published_at": "2026-03-25T12:30:00+00:00",
                "fact": "Most primary retrieval lanes failed during this degraded benchmark run.",
                "interpretation": "This run should score worse than a healthy build.",
                "confidence_level": "low",
                "signal_strength": "low",
                "retrieval_status": "failed",
                "provider": "apify",
                "source_type": "primary_web",
                "raw_reference": {"benchmark": "degraded"},
            },
        ]


def run_quality_benchmarks() -> list[BenchmarkResult]:
    good_result = _run_case("good_build_fixture", degraded=False)
    degraded_result = _run_case("degraded_build_sparse", degraded=True)
    return [good_result, degraded_result]


def _run_case(name: str, *, degraded: bool) -> BenchmarkResult:
    request = CreateBriefRequest.from_dict(load_demo_request_payload())
    if degraded:
        runtime = PortfolioRiskDesk(AppConfig(), retrieval_adapter=_DegradedRetrievalAdapter())
        brief, _ = runtime.create_brief(request, as_of_date=date(2026, 3, 25))
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            runtime = PortfolioRiskDesk(AppConfig(local_state_dir=temp_dir))
            runtime.create_brief(request, as_of_date=date(2026, 3, 24))
            brief, _ = runtime.create_brief(request, as_of_date=date(2026, 3, 25))

    checks = {
        "source_quality": _check_source_quality(brief.to_dict()),
        "factor_relevance": _check_factor_relevance(brief.to_dict()),
        "scenario_coherence": _check_scenario_coherence(brief.to_dict()),
        "signal_vs_noise_quality": _check_signal_noise(brief.to_dict()),
        "delta_usefulness": _check_delta_usefulness(brief.to_dict()),
    }
    return BenchmarkResult(
        name=name,
        score=sum(1 for passed in checks.values() if passed),
        max_score=len(checks),
        checks=checks,
    )


def _check_source_quality(payload: dict[str, Any]) -> bool:
    evidence = payload.get("evidence_and_sources", [])
    return bool(evidence) and all(
        item.get("url_or_publisher") and item.get("why_it_mattered") for item in evidence[:3]
    )


def _check_factor_relevance(payload: dict[str, Any]) -> bool:
    factors = payload.get("dominant_factors", [])
    return len(factors) >= 4 and any(item.get("stance") in {"strengthened", "improving"} for item in factors)


def _check_scenario_coherence(payload: dict[str, Any]) -> bool:
    scenarios = payload.get("scenario_analysis", [])
    return bool(scenarios) and all(
        scenario.get("confidence_level") in {"low", "medium", "high"}
        and scenario.get("supporting_evidence")
        and scenario.get("falsifiers")
        for scenario in scenarios
    )


def _check_signal_noise(payload: dict[str, Any]) -> bool:
    items = payload.get("signal_vs_noise", [])
    buckets = {item.get("bucket") for item in items}
    return ("high_signal" in buckets or "monitor" in buckets) and "noise" in buckets


def _check_delta_usefulness(payload: dict[str, Any]) -> bool:
    uncertainty_notes = payload.get("uncertainty_notes", [])
    comparison_baseline = payload.get("user_focus", {}).get("comparison_baseline") or ""
    return (
        bool(payload.get("risk_map_changes"))
        and comparison_baseline not in {"", "Prior brief comparison not configured"}
        and all("first-run baseline" not in note.lower() for note in uncertainty_notes)
        and "most recent brief" in comparison_baseline.lower()
    )
