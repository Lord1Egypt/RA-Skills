#!/usr/bin/env python3
"""Skill self-check — pure local, no network required."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import seal_cli  # noqa: E402


def main() -> int:
    checks: dict = {
        "signature": seal_cli.SIG,
        "version": seal_cli.VERSION,
        "dual_ledgers": len(seal_cli.DUAL_LEDGERS),
        "https_only_ledgers": all(u["url"].startswith("https://") for u in seal_cli.DUAL_LEDGERS),
        "subprocess_forbidden": "subprocess" not in sys.modules,
        "psi_sign": False,
        "lock_local": False,
        "no_collapse": False,
        "merkle_verify": False,
        "phase_align": False,
        "attest": False,
        "ok": False,
    }

    psi = seal_cli.build_psi("truth-probe", "chaos-probe", "self-check-node")
    checks["psi_sign"] = bool(psi.get("ok")) and psi["psi"]["prob_truth"] > 0 and psi["psi"]["prob_chaos"] > 0
    checks["no_collapse"] = abs(psi["psi"]["norm"] - 1.0) < 1e-9

    lock = seal_cli.lock_geodesic(psi, network=False, nodes=["self-check-node", "peer-a"])
    checks["lock_local"] = bool(lock.get("ok")) and bool(lock.get("merkle_root"))

    v = seal_cli.verify_artifact(lock)
    checks["merkle_verify"] = bool(v.get("ok")) and v.get("merkle_match") is True

    pa = seal_cli.phase_align_only(lock, ["peer-b", "peer-c"])
    checks["phase_align"] = bool(pa.get("ok")) and pa.get("collapse") is False

    att = seal_cli.attest_bundle("truth-probe", "chaos-probe", "self-check-node", network=False)
    checks["attest"] = bool(att.get("ok")) and att.get("attestation", {}).get("collapse") is False

    # collapse refuse
    bad_psi = dict(psi)
    bad_psi["psi"] = dict(psi["psi"])
    bad_psi["psi"]["prob_truth"] = 0.0
    bad_psi["psi"]["prob_chaos"] = 1.0
    refused = seal_cli.lock_geodesic(bad_psi, network=False, allow_collapse=False)
    checks["collapse_refused"] = refused.get("ok") is False and refused.get("error") == "collapse_detected"

    checks["ok"] = all(
        [
            checks["https_only_ledgers"],
            checks["psi_sign"],
            checks["lock_local"],
            checks["no_collapse"],
            checks["merkle_verify"],
            checks["phase_align"],
            checks["attest"],
            checks["collapse_refused"],
            checks["dual_ledgers"] >= 2,
        ]
    )
    print(json.dumps(checks, indent=2))
    return 0 if checks["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
