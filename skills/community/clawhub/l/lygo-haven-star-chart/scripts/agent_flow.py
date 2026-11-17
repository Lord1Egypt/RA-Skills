#!/usr/bin/env python3
"""Print canonical Haven Star Chart workflow with human consent gates."""

from __future__ import annotations

import json

FLOW = {
    "signature": "Δ9Φ963-HAVEN-STAR-AGENT-FLOW-v1.0.1",
    "policy": "human_approval_required_for_live_writes",
    "skillspector": "scripts use allowlisted in-process imports; no subprocess",
    "steps": [
        {
            "n": 1,
            "action": "trust_check",
            "cmd": "python scripts/self_check.py",
            "writes": False,
        },
        {
            "n": 2,
            "action": "verify_lattice",
            "cmd": "python tools/lygo_network_builder_verify.py",
            "writes": False,
        },
        {
            "n": 3,
            "action": "gate_validate",
            "cmd": "python scripts/gate_submission.py submission.json",
            "writes": False,
            "human_may_run": True,
        },
        {
            "n": 4,
            "action": "dry_run_submit",
            "cmd": "python tools/haven_star_chart_submit.py submission.json --dry-run ...",
            "writes": False,
            "human_may_run": True,
        },
        {
            "n": 5,
            "action": "submit_pending",
            "cmd": "python tools/haven_star_chart_submit.py ... --i-consent",
            "writes": True,
            "requires": "explicit_user_approval",
        },
        {
            "n": 6,
            "action": "steward_ingest",
            "cmd": "python tools/haven_star_chart_ingest.py --i-consent",
            "writes": True,
            "requires": "steward_user_approval",
        },
        {
            "n": 7,
            "action": "verify_feed",
            "cmd": "python scripts/verify_feed.py",
            "writes": False,
        },
    ],
    "live_urls": {
        "chart": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "portal": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChartPortal.html",
        "feed": "https://deepseekoracle.github.io/lygo-protocol-stack/haven_star_chart/haven_star_chart_feed.json",
    },
    "skill_chain": [
        "lygo-protocol-stack-operator",
        "lygo-network-builder",
        "lygo-sovereign-super-skill",
        "lygo-haven-star-chart",
    ],
}


def main() -> int:
    print(json.dumps(FLOW, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())