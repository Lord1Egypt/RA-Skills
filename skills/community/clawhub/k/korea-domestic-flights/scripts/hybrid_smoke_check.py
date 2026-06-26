#!/usr/bin/env python3
import json
from pathlib import Path

from hybrid_observability import build_refine_diagnostics, choose_fallback_plan


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "references" / "hybrid-smoke-fixtures.json"



def _load_fixtures():
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))



def _assert_reason_prefixes(actual_reasons, expected_prefixes):
    for prefix in expected_prefixes:
        assert any(reason.startswith(prefix) for reason in actual_reasons), f"missing fallback reason prefix: {prefix}"



def _run_case(case, *, key_fn, label_fn, minimum_target=2, hard_cap=4, pad=2):
    diag = build_refine_diagnostics(
        case["broad_rows"],
        case["detailed_rows"],
        key_fn=key_fn,
        label_fn=label_fn,
    )
    plan = choose_fallback_plan(diag, minimum_target=minimum_target, hard_cap=hard_cap, pad=pad)
    expect = case.get("expect", {})

    for reason in expect.get("required_reasons", []):
        assert diag["counts"].get(reason), f"missing expected reason: {reason}"
    if "dominant_reason" in expect:
        assert diag["dominant_reason"] == expect["dominant_reason"], f"unexpected dominant_reason: {diag['dominant_reason']}"
    if "primary_interpretation" in expect:
        assert diag["primary_interpretation"] == expect["primary_interpretation"], f"unexpected interpretation: {diag['primary_interpretation']}"
    if "fallback_triggered" in expect:
        assert plan["triggered"] is expect["fallback_triggered"], f"unexpected fallback trigger state: {plan['triggered']}"

    _assert_reason_prefixes(plan["reasons"], expect.get("required_fallback_reason_prefixes", []))

    for key, value in expect.get("extraction_summary", {}).items():
        assert diag["extraction_summary"].get(key) == value, f"unexpected extraction_summary[{key}]: {diag['extraction_summary'].get(key)}"

    assert diag["ranked_reasons"], "ranked reasons should not be empty"
    if diag.get("dominant_reason"):
        assert diag.get("dominant_reason_code"), "dominant reason code missing"
        assert diag.get("dominant_reason_category"), "dominant reason category missing"
    return {"diagnostics": diag, "fallback_plan": plan}



def run_date_range_cases():
    fixtures = _load_fixtures()
    outputs = {}
    for case in fixtures.get("date_range_cases", []):
        outputs[case["name"]] = _run_case(
            case,
            key_fn=lambda row: row["departure_date"],
            label_fn=lambda row: row["departure_date"],
        )
    return outputs



def run_matrix_cases():
    fixtures = _load_fixtures()
    outputs = {}
    for case in fixtures.get("matrix_cases", []):
        outputs[case["name"]] = _run_case(
            case,
            key_fn=lambda row: (row["destination"], row["departure_date"]),
            label_fn=lambda row: f"{row['destination']} {row['departure_date']}",
        )
    return outputs


if __name__ == "__main__":
    print(json.dumps({
        "fixture_path": str(FIXTURE_PATH),
        "date_range_cases": run_date_range_cases(),
        "matrix_cases": run_matrix_cases(),
    }, ensure_ascii=False, indent=2))
