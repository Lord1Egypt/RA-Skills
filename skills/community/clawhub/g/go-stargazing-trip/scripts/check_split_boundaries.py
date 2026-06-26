#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"command failed: {' '.join(cmd)}\nSTDERR:\n{p.stderr}\nSTDOUT:\n{p.stdout}")
    return json.loads(p.stdout)


def main() -> None:
    nightly = run(
        [
            sys.executable,
            str(WORKSPACE / 'skills' / 'go-stargazing' / 'scripts' / 'go_stargazing.py'),
            '--trip-start-date', '2026-04-04',
            '--trip-days', '2',
            '--scope-preset', 'national',
            '--top-n', '5',
            '--trip-top-n', '3',
        ],
        cwd=WORKSPACE,
    )
    trip = run(
        [
            sys.executable,
            str(ROOT / 'go_stargazing_trip.py'),
            '--trip-start-date', '2026-04-04',
            '--trip-days', '2',
            '--scope-preset', 'national',
            '--top-n', '5',
            '--trip-top-n', '3',
        ],
        cwd=ROOT,
    )

    assert nightly.get('multi_day_mode') is True, 'go-stargazing should expose multi_day_mode=True'
    assert nightly.get('trip_mode') is False, 'go-stargazing should disable trip_mode'
    assert 'trip_plans' not in nightly, 'go-stargazing should not emit trip_plans after split'

    assert trip.get('trip_mode') is True, 'go-stargazing-trip should expose trip_mode=True'
    assert isinstance(trip.get('trip_plans'), list) and trip.get('trip_plans'), 'go-stargazing-trip should emit trip_plans'

    print('PASS split boundaries')


if __name__ == '__main__':
    main()
