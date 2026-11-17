#!/usr/bin/env python3
"""
phd-research-companion - cross-platform CLI entrypoint.

Replaces the bash-only `./run` of v1.x. Works on Windows, macOS and Linux
because it always re-invokes the current Python interpreter.

    python run.py <command> [args...]
    python run.py help
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"

# command -> (script, ) ; extra args are forwarded verbatim
COMMANDS = {
    "init":       [ROOT / "init_research_project.py"],
    "search":     [SCRIPTS / "multi_source_search.py"],
    "analyze":    [SCRIPTS / "paper_analyzer.py"],
    "template":   [SCRIPTS / "generate_latex_template.py"],
    "experiment": [SCRIPTS / "create_experiment_design.py"],
    "revision":   [SCRIPTS / "revision_tracker.py"],
    "math":       [SCRIPTS / "verify_math_notation.py"],
    "check":      [SCRIPTS / "check_compliance.py"],
    # theory track
    "ledger":     [SCRIPTS / "proof_ledger.py"],
    "priority":   [SCRIPTS / "priority_check.py"],
    "certify":    [SCRIPTS / "rational_certificate.py"],
    "audit":      [SCRIPTS / "self_audit.py"],
    "session":    [SCRIPTS / "long_horizon_session.py"],
}

# Self-scoring commands. They measure THIS repository's publishing hygiene, so
# they are dropped from the Coze export (a user there has no repo to score) and
# may legitimately be absent. Every other command must resolve or the install is
# broken -- so only these degrade to "unknown command".
OPTIONAL_COMMANDS: dict[str, list[Path]] = {
    "score":    [SCRIPTS / "self_score.py"],
    "selftest": [SCRIPTS / "score_selftest.py"],
}

HELP = """phd-research-companion 2.4.0

usage: python run.py <command> [args...]

commands:
  init        create a research project skeleton        (init_research_project.py)
  search      multi-source literature search            (multi_source_search.py)
  analyze     analyse downloaded PDFs                   (paper_analyzer.py)
  template    generate a compiling LaTeX skeleton       (generate_latex_template.py)
  experiment  baseline / ablation / robustness design   (create_experiment_design.py)
  revision    record revision rounds + evidence         (revision_tracker.py)
  math        notation + proof consistency lint         (verify_math_notation.py)
  check       pre-submission compliance audit           (check_compliance.py)

theory track:
  ledger      claim ledger (lemma -> theorem DAG)       (proof_ledger.py)
  priority    novelty / priority check before claiming  (priority_check.py)
  certify     exact rational-arithmetic certificate     (rational_certificate.py)
  audit       proven vs publishable gap report          (self_audit.py)
  session     long-horizon research state machine       (long_horizon_session.py)
"""


def _available() -> tuple[dict, dict]:
    """Split the command table into present and absent entries."""
    present, absent = {}, {}
    for table, sink in ((COMMANDS, present), (OPTIONAL_COMMANDS, absent)):
        for name, paths in table.items():
            (present if paths[0].exists() else sink)[name] = paths
    return present, absent


def main(argv: list[str]) -> int:
    present, absent = _available()

    if not argv or argv[0] in ("-h", "--help", "help"):
        print(HELP, end="")
        if present:
            print("self-check:")
            for name in sorted(present):
                print(f"  {name:<10} {present[name][0].name}")
        if absent:
            print("not shipped in this build:")
            for name in sorted(absent):
                print(f"  {name:<10} {absent[name][0].name}")
        return 0

    cmd = argv[0]
    if cmd in present:
        target = present[cmd][0]
    elif cmd in absent:
        print(f"'{cmd}' is not available in this build "
              f"({absent[cmd][0].name} is not shipped)", file=sys.stderr)
        return 2
    else:
        print(f"unknown command: {cmd}\n", file=sys.stderr)
        print(HELP, file=sys.stderr, end="")
        return 2

    # NOTE: cwd is deliberately NOT forced to ROOT. Several scripts default
    # their output to a relative path ("math-notation-check.md", "./session",
    # "02-methodology-dev", ...). Pinning cwd to the install directory made
    # every default output land INSIDE the skill folder. Let the caller's cwd
    # decide where relative outputs go; scripts are invoked by absolute path.
    proc = subprocess.run([sys.executable, str(target), *argv[1:]])
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
