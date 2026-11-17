from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from .decision.engine import IntelligentDecisionEngine
from .models.enums import DecisionStatus
from .models.schemas import DecisionRequest, DecisionResult
from .report import export_expert_report
from .service import DecisionService
from .version import VERSION

logger = logging.getLogger(__name__)

_DEFAULT_EXAMPLE = "market_entry.json"
_JSON_FLAG = "--json"
_DECISION_FLAG = "--decision"
_VERSION_FLAG = "--version"
_REPORT_SUBCOMMAND = "report"


def _example_path(name: str | None = None) -> Path:
    example = (
        Path(__file__).resolve().parents[2] / "examples" / (name or _DEFAULT_EXAMPLE)
    )
    if not example.exists():
        raise SystemExit(
            f"Example not found: {example}. Pass --decision <path> to use another "
            "decision file, or run from a source checkout."
        )
    return example


def _load_decision(decision_file: Path) -> DecisionRequest:
    data = json.loads(decision_file.read_text(encoding="utf-8"))
    return DecisionRequest.model_validate(data)


def _print_human_result(result: DecisionResult) -> None:
    """Human-readable summary for the core decision demo."""
    bar = "=" * 70
    print(bar)
    print(f"NOMOS Decision Core  v{VERSION}")
    print(bar)
    print(f"Decision ID:    {result.decision_id}")
    print(f"Objective:      {result.objective}")
    print(f"Status:         {result.status.value}")
    print(f"Audit passed:   {result.audit_passed}")
    print(f"Leading:        {result.leading_candidate_ids or 'none'}")

    print("\n--- Candidate Scores ---")
    if not result.alternatives:
        print("  (no alternatives evaluated)")
    for alt in result.alternatives:
        score = f"{alt.total_score}" if alt.total_score is not None else "n/a"
        print(f"  {alt.alternative_id} [{alt.status.value}]  total={score}")

    print("\n--- Hard Constraint Filtering ---")
    for alt in result.alternatives:
        passed = "PASS" if alt.hard_constraints_passed else "FAIL"
        print(f"  {alt.alternative_id}: {passed}")

    print("\n--- Unresolved Variables ---")
    if result.unresolved_variables:
        for path in result.unresolved_variables:
            print(f"  {path}")
    else:
        print("  (none)")

    print("\n--- Issues ---")
    if result.issues:
        for issue in result.issues:
            flag = "BLOCKING" if issue.blocking else issue.severity.value.upper()
            print(f"  [{flag}] {issue.code}: {issue.message}")
    else:
        print("  (none)")

    if not result.audit_passed:
        print(
            "\n!! Audit did not pass — decision requires review before approval. "
            "See issues above."
        )
    elif result.status == DecisionStatus.HUMAN_APPROVAL_REQUIRED:
        print("\nDecision is audit-clean and awaiting human approval.")
    print(bar)


def _run_demo(args: list[str]) -> None:
    decision_file: Path | None = None
    raw_json = False
    it = iter(args)
    for arg in it:
        if arg == _DECISION_FLAG:
            decision_file = Path(next(it))
        elif arg == _JSON_FLAG:
            raw_json = True
        elif arg == _VERSION_FLAG:
            print(VERSION)
            return
        else:
            raise SystemExit(f"Unknown argument: {arg}")

    request = _load_decision(decision_file or _example_path())
    result = IntelligentDecisionEngine().evaluate(request)
    if raw_json:
        print(result.model_dump_json(indent=2))
    else:
        _print_human_result(result)


def _run_report(args: list[str]) -> None:
    decision_file: Path | None = None
    out_dir = Path("reports")
    out_file: Path | None = None
    it = iter(args)
    for arg in it:
        if arg == _DECISION_FLAG:
            decision_file = Path(next(it))
        elif arg == "--out":
            out_file = Path(next(it))
        elif arg == _VERSION_FLAG:
            print(VERSION)
            return
        else:
            raise SystemExit(f"Unknown argument: {arg}")

    request = _load_decision(decision_file or _example_path())
    record = DecisionService().evaluate(request)
    written = export_expert_report(
        records=[record],
        out_path=out_file,
        out_dir=out_dir,
    )
    logger.info("expert review report written to %s", written)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(name)s %(levelname)s %(message)s",
    )
    if len(sys.argv) > 1 and sys.argv[1] == _REPORT_SUBCOMMAND:
        _run_report(sys.argv[2:])
        return
    _run_demo(sys.argv[1:])


if __name__ == "__main__":
    main()
