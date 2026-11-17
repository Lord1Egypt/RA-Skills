"""Scenario analysis — declared-scenario stress runs.

Given a set of declared scenarios (failed assumptions, metric overrides),
re-run the deterministic engine and report the outcome.
"""

from __future__ import annotations

import copy

from ..models.enums import ScenarioOutcomeStatus
from ..models.hub import ScenarioResult
from ..models.schemas import DecisionRequest, DecisionResult, ScenarioDefinition


def analyze_scenarios(
    engine: object,
    request: DecisionRequest,
    baseline: DecisionResult,
    scenarios: list[ScenarioDefinition],
) -> list[ScenarioResult]:
    """Run each declared scenario against the engine.

    For each scenario:
      - If failed_assumption_ids are declared, remove alternatives that depend
        on those assumptions and re-evaluate.
      - If metric_overrides are declared, apply them and re-evaluate.
    """
    results: list[ScenarioResult] = []

    for scenario in scenarios:
        try:
            patched = _apply_scenario(request, scenario)
            if patched is None:
                results.append(
                    ScenarioResult(
                        scenario=scenario,
                        outcome_status=ScenarioOutcomeStatus.NO_VIABLE_ALTERNATIVE,
                        evaluation_result=None,
                        issues=["No viable alternatives remain after applying scenario."],
                    )
                )
                continue

            # Re-evaluate
            scenario_result = engine.evaluate(patched)
            results.append(
                ScenarioResult(
                    scenario=scenario,
                    outcome_status=ScenarioOutcomeStatus.EVALUATED,
                    evaluation_result=scenario_result.model_dump(mode="json"),
                    issues=[],
                )
            )
        except Exception as exc:
            results.append(
                ScenarioResult(
                    scenario=scenario,
                    outcome_status=ScenarioOutcomeStatus.BLOCKED,
                    evaluation_result=None,
                    issues=[str(exc)],
                )
            )

    return results


def _apply_scenario(
    request: DecisionRequest,
    scenario: ScenarioDefinition,
) -> DecisionRequest | None:
    """Apply a scenario to a decision request.

    Returns None if no viable alternatives remain.
    """
    patched = request.model_copy(deep=True)

    # Apply failed assumption IDs
    if scenario.failed_assumption_ids:
        invalidated = set(scenario.failed_assumption_ids)
        patched.alternatives = [
            alt
            for alt in patched.alternatives
            if not (set(alt.required_assumptions) & invalidated)
        ]

    # Apply metric overrides
    if scenario.metric_overrides:
        for alt_id, overrides in scenario.metric_overrides.items():
            for alt in patched.alternatives:
                if alt.id == alt_id:
                    metrics = dict(alt.metrics)
                    metrics.update(overrides)
                    alt.metrics = metrics

    if not patched.alternatives:
        return None

    return patched