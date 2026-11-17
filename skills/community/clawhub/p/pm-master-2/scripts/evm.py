#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PM Master · Earned Value Management (EVM) calculation
---------------------------------------------------
Input metrics.yaml (or .json), containing at least:
  pv: Planned Value
  ev: Earned Value
  ac: Actual Cost
  bac: Budget At Completion   # optional, defaults to sum of pv

Output CPI / SPI / CV / SV / EAC / ETC / VAC and a health flag.

Usage:
  python3 evm.py --data metrics.yaml
"""
import argparse
import json

try:
    import yaml
except ImportError:
    yaml = None


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        raw = f.read()
    if path.endswith(('.yaml', '.yml')):
        return yaml.safe_load(raw)
    return json.loads(raw)


def compute(pv, ev, ac, bac=None):
    bac = bac if bac is not None else pv
    cpi = ev / ac if ac else 0.0
    spi = ev / pv if pv else 0.0
    cv = ev - ac
    sv = ev - pv
    eac = bac / cpi if cpi else float('inf')
    etc = eac - ac
    vac = bac - eac
    # Health flag
    flags = []
    if cpi < 0.95:
        flags.append("cost overrun (CPI<0.95)")
    if spi < 0.95:
        flags.append("schedule slippage (SPI<0.95)")
    if not flags:
        flags.append("healthy")
    return {
        'PV': pv, 'EV': ev, 'AC': ac, 'BAC': bac,
        'CPI': round(cpi, 3), 'SPI': round(spi, 3),
        'CV': round(cv, 2), 'SV': round(sv, 2),
        'EAC': round(eac, 2) if eac != float('inf') else 'inf',
        'ETC': round(etc, 2) if etc != float('inf') else 'inf',
        'VAC': round(vac, 2), 'flags': flags,
    }


def main():
    ap = argparse.ArgumentParser(description="PM Master EVM calculation")
    ap.add_argument('--data', required=True)
    a = ap.parse_args()
    d = load(a.data)
    pv, ev, ac = d.get('pv', 0), d.get('ev', 0), d.get('ac', 0)
    bac = d.get('bac')
    r = compute(pv, ev, ac, bac)
    print("=== Earned Value Management (EVM) Report ===")
    for k in ['PV', 'EV', 'AC', 'BAC', 'CPI', 'SPI', 'CV', 'SV', 'EAC', 'ETC', 'VAC']:
        print(f"  {k:<4}: {r[k]}")
    print(f"  Health: {' | '.join(r['flags'])}")


if __name__ == '__main__':
    main()
