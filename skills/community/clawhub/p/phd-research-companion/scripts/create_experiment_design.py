#!/usr/bin/env python3
"""
Experiment Design Generator

Emits reproducible YAML specifications for the three design families that
top-tier venues expect: baseline comparison, ablation, robustness.

It writes DESIGNS, never results. Any field that would hold a measured number
is emitted as null with a `to_fill` note, so a design file can never be
mistaken for an outcome.

Usage:
    python create_experiment_design.py --type comparison \
        --datasets "CIC-IDS2017,UNSW-NB15" --baselines "A,B" --metrics "acc,f1" -o ./04-experiments
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime
from pathlib import Path

TYPES = ("comparison", "ablation", "robustness")


def _yaml_list(items, indent=2) -> str:
    if not items:
        return " []"
    pad = " " * indent
    return "\n" + "\n".join(f"{pad}- {i}" for i in items)


def build_comparison(datasets, baselines, metrics, seeds) -> str:
    return f"""# Baseline comparison design
# Generated {datetime.now().isoformat(timespec='seconds')}
kind: comparison
reproducibility:
  seeds:{_yaml_list(seeds)}
  deterministic: null      # to_fill: true/false, justify
  framework_versions: null # to_fill
datasets:{_yaml_list(datasets)}
baselines:{_yaml_list(baselines)}
metrics:{_yaml_list(metrics)}
protocol:
  splits: null             # to_fill: train/val/test proportions
  repeated_runs: null      # to_fill: >= 5 for variance reporting
  reporting: "mean +/- std over seeds"
results: null              # NEVER pre-filled; filled only by running the experiment
"""


def build_ablation(components, base_model, metrics, seeds) -> str:
    variants = ["full_model"] + [f"without_{c}" for c in components]
    return f"""# Ablation design
# Generated {datetime.now().isoformat(timespec='seconds')}
kind: ablation
reproducibility:
  seeds:{_yaml_list(seeds)}
base_model: {base_model}
metrics:{_yaml_list(metrics)}
variants:{_yaml_list(variants)}
rule: "each variant removes exactly one component; all else held fixed"
results: null
"""


def build_robustness(attacks, budgets, metrics, seeds) -> str:
    return f"""# Robustness stress-test design
# Generated {datetime.now().isoformat(timespec='seconds')}
kind: robustness
reproducibility:
  seeds:{_yaml_list(seeds)}
attacks:{_yaml_list(attacks)}
perturbation_budgets:{_yaml_list(budgets)}
metrics:{_yaml_list(metrics)}
rule: "evaluate every attack at every budget; report worst case, not mean"
results: null
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate reproducible experiment designs")
    # `baseline` is an alias for `comparison` (that is what check_compliance
    # calls the row), and the singular flag spellings are accepted because they
    # are what people actually type.
    ap.add_argument("--type", "-t", required=True, choices=list(TYPES) + ["baseline"])
    ap.add_argument("--datasets", "--dataset", default="")
    ap.add_argument("--baselines", "--baseline", default="")
    ap.add_argument("--components", "--ablations", default="")
    ap.add_argument("--base-model", default="")
    ap.add_argument("--attack-types", dest="attacks", default="")
    ap.add_argument("--perturbation-budgets", dest="budgets", default="")
    ap.add_argument("--metrics", default="accuracy,f1")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--output-dir", "-o", default=".")
    args = ap.parse_args()

    def split(s):
        return [x.strip() for x in s.split(",") if x.strip()]

    seeds = split(args.seeds)
    metrics = split(args.metrics) or ["accuracy"]

    if args.type in ("comparison", "baseline"):
        if not split(args.datasets) or not split(args.baselines):
            print("error: --datasets and --baselines required for comparison", file=sys.stderr)
            return 2
        content = build_comparison(split(args.datasets), split(args.baselines), metrics, seeds)
        name = "experiment-comparison-design.yaml"
    elif args.type == "ablation":
        if not split(args.components):
            print("error: --components required for ablation", file=sys.stderr)
            return 2
        content = build_ablation(split(args.components),
                                 args.base_model or "base_model", metrics, seeds)
        name = "experiment-ablation-design.yaml"
    else:
        if not split(args.attacks):
            print("error: --attack-types required for robustness", file=sys.stderr)
            return 2
        content = build_robustness(split(args.attacks),
                                   split(args.budgets) or ["unspecified"], metrics, seeds)
        name = "experiment-robustness-design.yaml"

    out_dir = Path(args.output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / name
    path.write_text(content, encoding="utf-8")

    notes = out_dir / "experiment-design-notes.md"
    notes.write_text(
        "# Experiment design notes\n\n"
        f"- Generated: {datetime.now().isoformat(timespec='seconds')}\n"
        f"- Type: {args.type}\n"
        f"- File: {name}\n\n"
        "Rules enforced by this generator:\n\n"
        "1. Result fields are null. A design is not a result.\n"
        "2. Seeds are explicit; single-seed numbers are not reportable.\n"
        "3. Robustness reports worst case, not mean.\n",
        encoding="utf-8")

    print(f"Design : {path}")
    print(f"Notes  : {notes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
