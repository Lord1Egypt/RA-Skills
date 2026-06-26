from __future__ import annotations

import argparse
import json
from pathlib import Path

from runtime_support import audit_directory, load_json_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit export directory to prevent leakage")
    parser.add_argument("target_dir", type=Path, help="Target directory to audit")
    parser.add_argument("--policy", type=Path, help="Audit policy JSON file")
    parser.add_argument("--output", type=Path, help="Optional, output JSON file")
    return parser.parse_args()


def default_policy_path(script_path: Path) -> Path:
    return script_path.resolve().parents[1] / "policies" / "export-audit-policy.json"


def main() -> int:
    args = parse_args()
    target_dir = args.target_dir.resolve()
    policy_path = args.policy.resolve() if args.policy else default_policy_path(Path(__file__))
    policy = load_json_file(policy_path)
    result = audit_directory(target_dir, policy)
    rendered = json.dumps(
        {
            "policy": policy_path.name,
            "result": result,
        },
        ensure_ascii=False,
        indent=2,
    )
    if args.output:
        args.output.resolve().write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 1 if result["blocked"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
