#!/usr/bin/env python3
"""Safe bounded count of unprocessed Forge variant proposals.

Counts `vp_*.json` / `vd_*.json` files that are GENUINELY unprocessed:
ONLY under `commons/data/ocas-forge/intake/`, EXCLUDING `intake/processed/`,
the `proposals/` SOURCE MIRROR, and the top-level `processed/` dir.

WHY THIS SCRIPT EXISTS:
A hand-rolled recursive `find` / `os.walk` over the WHOLE
`commons/data/ocas-forge/` tree sweeps up the `proposals/` mirror (already
copied into `intake/processed/`) AND the top-level `processed/` dir, yielding
a FALSE nonzero count that flips a `routine_no_op` dispatch into a `genuine`
variant-build dispatch. Re-confirmed live 2026-07-16: a closure orchestrator
recursive-walked the whole tree, found 11 copies in `proposals/` + 11 in
top-level `processed/`, and wrote `unprocessed_proposals: 11` / `action:
genuine` when the true value was 0. This script bounds the walk to prevent
exactly that.

Usage: python3 scripts/forge_count_unprocessed.py
Prints the integer count; exits 0.
"""
import os
import sys

_HELP_ARGS = {"--help", "-h"}
if set(sys.argv[1:]) & _HELP_ARGS:
    print((__doc__ or "").strip() or "Usage: python3 forge_count_unprocessed.py")
    sys.exit(0)


PROFILE = "<hermes-home>/profiles/indigo"
ROOT = os.path.join(PROFILE, "commons", "data", "ocas-forge")
INTAKE = os.path.join(ROOT, "intake")
INTAKE_PROCESSED = os.path.join(INTAKE, "processed")
PROPOSALS = os.path.join(ROOT, "proposals")


def is_proposal(fn):
    return fn.startswith("vp_") or fn.startswith("vd_")


def main():
    unprocessed = []
    if os.path.isdir(INTAKE):
        for dp, _dn, fn in os.walk(INTAKE):
            # never descend into processed / mirror / archive
            if dp == INTAKE_PROCESSED or dp.startswith(INTAKE_PROCESSED + os.sep):
                continue
            if dp == PROPOSALS or dp.startswith(PROPOSALS + os.sep):
                continue
            parts = dp.split(os.sep)
            if ".archive" in parts or ".quarantine" in parts:
                continue
            for f in fn:
                if is_proposal(f):
                    unprocessed.append(os.path.join(dp, f))
    print(len(unprocessed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())