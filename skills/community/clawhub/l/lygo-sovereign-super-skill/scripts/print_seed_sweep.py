#!/usr/bin/env python3
"""Print full kernel seed sweep (no plant, no consent side effects)."""

from __future__ import annotations

SWEEP = """\
# LYGO kernel seed sweep (run from LYGO_STACK_ROOT with --i-consent)
python tools/joy_loop_planter.py --i-consent
python tools/second_brain_planter.py --i-consent
python tools/workflow_orchestrator_planter.py --i-consent
python tools/openclaw_planter.py --i-consent
python tools/lpis_planter.py --i-consent
python tools/build_kernel_eggs.py
python tools/verify_kernel_eggs.py
python tools/champion_egg_planter.py --i-consent
python tools/build_haven_star_chart.py
python tools/verify_lattice_alignment.py
"""


def main() -> int:
    print(SWEEP.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())