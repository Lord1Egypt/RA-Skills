"""NOMOS Hub CLI — nomos-hub-demo entry point.

Demonstrates the Intelligent Decision Hub with two stress scenarios and the
GCAE-backed cognitive audit pipeline (NS/IAP/LCH/TPG/BFC/CCS/META/STATE).
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone
from decimal import Decimal

from .hub import IntelligentDecisionHub
from .models.enums import (
    AssumptionSource,
    ConstraintKind,
    ConstraintOperator,
    EvaluationMode,
    EvidenceStatus,
    ScoringRule,
)
from .models.hub import HubAnalysisRequest
from .models.schemas import (
    Alternative,
    Assumption,
    Constraint,
    Criterion,
    DecisionRequest,
    Evidence,
    EvidenceQuality,
    ResponsibilityRef,
    ScenarioDefinition,
)
from .version import VERSION

logger = logging.getLogger(__name__)


def _quality(rel: Decimal, owner: str) -> EvidenceQuality:
    return EvidenceQuality(
        reliability=rel,
        relevance=rel,
        independence=rel,
        freshness=rel,
        assessed_by=ResponsibilityRef(owner=owner, source="Quality Assessment 2026-Q3"),
        method="Structured evidence review",
    )


def _build_example_decision() -> DecisionRequest:
    owner = ResponsibilityRef(
        owner="Strategy Committee",
        source="Board Resolution 2026-Q3-07",
        role="decision_owner",
    )

    legal_counsel = ResponsibilityRef(
        owner="Legal Counsel", source="External Legal Opinion"
    )
    infra_lead = ResponsibilityRef(owner="Infrastructure Lead", source="Cloud RFP")
    bd_lead = ResponsibilityRef(owner="BD Lead", source="PartnerCo MOU")
    growth_team = ResponsibilityRef(owner="Growth Team", source="Market Research v1")
    cfo = ResponsibilityRef(owner="CFO Office", source="Capital Plan 2026")
    pmo = ResponsibilityRef(owner="PMO", source="Launch Plan 2026")
    rev_ops = ResponsibilityRef(owner="Revenue Ops", source="Forecast Model v3")

    assumptions = [
        Assumption(
            id="A1",
            statement="Local AI regulatory filing can be completed within 90 days",
            source=AssumptionSource.EXPLICIT,
            falsification_condition="Filing rejected or takes longer than 180 days; entry delayed or cancelled.",
            critical=True,
            responsibility=legal_counsel,
        ),
        Assumption(
            id="A2",
            statement="Local cloud provider meets data-residency requirements",
            source=AssumptionSource.EXPLICIT,
            falsification_condition="Provider cannot deliver data-residency certification; infrastructure rebuild required.",
            critical=True,
            dependencies=["A1"],
            responsibility=infra_lead,
        ),
        Assumption(
            id="A3",
            statement="First-year user-acquisition cost stays below 150 USD per paying user",
            source=AssumptionSource.EXPLICIT,
            falsification_condition="CAC exceeds 150 USD for two consecutive quarters; channel mix must be restructured.",
            critical=False,
            dependencies=["A2"],
            responsibility=growth_team,
        ),
        Assumption(
            id="A4",
            statement="At least one local distribution partner is signed before launch",
            source=AssumptionSource.EXPLICIT,
            falsification_condition="No partner signed; launch proceeds via direct sales only with reduced revenue forecast.",
            critical=True,
            responsibility=bd_lead,
        ),
    ]

    alternatives = [
        Alternative(
            id="S1",
            name="Direct Entry",
            description="Establish a local subsidiary, own infrastructure, direct sales.",
            metrics={
                "capital_required": Decimal("5000000"),
                "time_to_market_months": Decimal("12"),
                "expected_revenue_year1_musd": Decimal("8.0"),
                "risk_score": Decimal("0.75"),
                "local_partner_required": False,
            },
            required_assumptions=["A1", "A2", "A3"],
        ),
        Alternative(
            id="S2",
            name="Partner-Led Entry",
            description="Partner with a local distributor; lower capital, shared revenue.",
            metrics={
                "capital_required": Decimal("1500000"),
                "time_to_market_months": Decimal("6"),
                "expected_revenue_year1_musd": Decimal("3.5"),
                "risk_score": Decimal("0.40"),
                "local_partner_required": True,
            },
            required_assumptions=["A1", "A2", "A3", "A4"],
        ),
    ]

    criteria = [
        Criterion(
            id="K1",
            name="Capital Efficiency",
            metric="capital_required",
            min_value=Decimal("0"),
            max_value=Decimal("10000000"),
            scoring_rule=ScoringRule.LOWER_IS_BETTER,
            weight=Decimal("0.30"),
            responsibility=cfo,
        ),
        Criterion(
            id="K2",
            name="Time to Market",
            metric="time_to_market_months",
            min_value=Decimal("0"),
            max_value=Decimal("24"),
            scoring_rule=ScoringRule.LOWER_IS_BETTER,
            weight=Decimal("0.25"),
            responsibility=pmo,
        ),
        Criterion(
            id="K3",
            name="Expected Revenue",
            metric="expected_revenue_year1_musd",
            min_value=Decimal("0"),
            max_value=Decimal("15"),
            scoring_rule=ScoringRule.HIGHER_IS_BETTER,
            weight=Decimal("0.45"),
            responsibility=rev_ops,
        ),
    ]

    constraints = [
        Constraint(
            id="C1",
            name="Capital ceiling",
            kind=ConstraintKind.HARD,
            metric="capital_required",
            operator=ConstraintOperator.LTE,
            expected=Decimal("6000000"),
            responsibility=cfo,
        ),
    ]

    evidence = [
        Evidence(
            id="E1",
            statement="Legal opinion estimates filing timeline 60-90 days for SaaS products of this category.",
            source="External legal opinion, LLP",
            status=EvidenceStatus.SUPPLIED,
            observed_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
            quality=_quality(Decimal("0.8"), "Legal Counsel"),
            responsibility=legal_counsel,
        ),
        Evidence(
            id="E2",
            statement="Cloud provider confirms data-residency region available; SLA pending final sign-off.",
            source="Cloud Provider SLA Draft",
            status=EvidenceStatus.SUPPLIED,
            observed_at=datetime(2026, 7, 10, tzinfo=timezone.utc),
            quality=_quality(Decimal("0.6"), "Infrastructure Lead"),
            responsibility=infra_lead,
        ),
        Evidence(
            id="E3",
            statement="MOU signed with PartnerCo; exclusivity pending legal review.",
            source="Distribution Partner MOU",
            status=EvidenceStatus.SUPPLIED,
            observed_at=datetime(2026, 8, 1, tzinfo=timezone.utc),
            quality=_quality(Decimal("0.8"), "BD Lead"),
            responsibility=bd_lead,
        ),
        Evidence(
            id="E4",
            statement="Market research estimates CAC 120-200 USD; methodology contested by growth team.",
            source="Market Research Report",
            status=EvidenceStatus.DISPUTED,
            observed_at=datetime(2026, 6, 15, tzinfo=timezone.utc),
            quality=_quality(Decimal("0.4"), "Growth Team"),
            responsibility=growth_team,
        ),
    ]

    assumptions[0].evidence_ids = ["E1"]
    assumptions[1].evidence_ids = ["E2"]
    assumptions[2].evidence_ids = ["E4"]
    assumptions[3].evidence_ids = ["E3"]
    alternatives[0].evidence_ids = ["E1", "E2"]
    alternatives[1].evidence_ids = ["E1", "E2", "E3"]

    return DecisionRequest(
        decision_id="DEC-MKT-ENTRY-001",
        objective="Select overseas market-entry strategy for AI SaaS product (Direct vs Partner-Led)",
        decision_owner=owner,
        time_horizon="12 months",
        evaluation_as_of=datetime(2026, 8, 26, tzinfo=timezone.utc),
        evaluation_mode=EvaluationMode.WEIGHTED,
        criteria=criteria,
        constraints=constraints,
        assumptions=assumptions,
        alternatives=alternatives,
        evidence=evidence,
        metadata={"scenario": "market_entry", "region": "APAC"},
    )


def _run_hub_demo() -> None:
    decision = _build_example_decision()

    request = HubAnalysisRequest(
        decision=decision,
        scenarios=[
            ScenarioDefinition(
                id="SC1",
                name="Critical assumption A1 failure (regulatory filing rejected)",
                failed_assumption_ids=["A1"],
            ),
            ScenarioDefinition(
                id="SC2",
                name="Capital cost shock (Direct Entry requires 8M)",
                metric_overrides={"S1": {"capital_required": Decimal("8000000")}},
            ),
        ],
        run_causal_reconstruction=False,
        run_cognitive_audit=True,
    )

    hub = IntelligentDecisionHub()
    report = hub.analyze(request)

    print("=" * 70)
    print(f"NOMOS Intelligent Decision Hub  v{VERSION}")
    print("=" * 70)
    print(f"Hub Run ID:       {report.hub_run_id}")
    print(f"Decision ID:      {report.decision_record.result.decision_id}")
    print(f"Decision Status:  {report.decision_record.result.status.value}")
    print(f"Audit Verified:   {report.algorithm_audit_verified}")
    print(f"Leading Candidates: {report.decision_record.result.leading_candidate_ids}")

    if report.decision_record.result.alternatives:
        print("\n--- Candidate Scores ---")
        for alt in report.decision_record.result.alternatives:
            score = f"{alt.total_score}" if alt.total_score is not None else "n/a"
            print(f"  {alt.alternative_id} [{alt.status.value}]  total={score}")

    if report.cognitive_audit:
        print(
            f"\n--- GCAE Cognitive Audit ({report.cognitive_audit.scanner_version}) ---"
        )
        print(f"Total findings:   {report.cognitive_audit.total_findings}")
        for f in report.cognitive_audit.findings:
            sev = f.severity.value.upper()
            print(f"  [{sev}] {f.code}: {f.description}")

    print(f"\n--- Scenarios ({len(report.scenarios)}) ---")
    for s in report.scenarios:
        print(f"  {s.scenario.id} '{s.scenario.name}': {s.outcome_status.value}")
        for issue in s.issues:
            print(f"    - {issue}")

    print(f"\n--- Information Priorities ({len(report.information_priorities)}) ---")
    for ip in report.information_priorities:
        print(f"  [{ip.tier}] {ip.item}")

    print(f"\nReport hash: {report.report_hash[:16]}...")
    print("=" * 70)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    if len(sys.argv) > 1 and sys.argv[1] == "--version":
        print(VERSION)
        return
    _run_hub_demo()


if __name__ == "__main__":
    main()
