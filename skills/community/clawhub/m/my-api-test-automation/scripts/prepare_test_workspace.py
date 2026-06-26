from __future__ import annotations

import argparse
import json
from pathlib import Path


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_manifest(env_name: str, runner: str) -> dict:
    return {
        "environment": env_name,
        "runner": runner,
        "cases": [],
        "metadata": {
            "generated_by": "api-test-automation",
            "notes": "Populate this manifest with generated test cases before execution."
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a reusable API test workspace skeleton.")
    parser.add_argument("--output", required=True, help="Output directory for the generated test workspace")
    parser.add_argument("--runner", default="postman", help="Target runner, for example postman or pytest")
    parser.add_argument("--env-name", default="default", help="Logical environment name")
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    dirs = [
        output,
        output / "cases",
        output / "config",
        output / "scripts",
        output / "reports",
        output / "artifacts",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    env_template = {
        "environment_name": args.env_name,
        "runner": args.runner,
        "base_url": "https://example.test",
        "auth_type": "bearer",
        "auth_source": {"mode": "env", "token_env": "API_TOKEN"},
        "default_headers": {"Content-Type": "application/json"},
        "variables": {},
        "timeout_ms": 10000,
        "report_dir": "./reports",
    }

    write_text(output / "config" / "environment.json", json.dumps(env_template, indent=2, ensure_ascii=False) + "\n")
    write_text(output / "scripts" / "pre-request.js", "// Fill in shared pre-request logic.\n")
    write_text(output / "scripts" / "post-assert.js", "// Fill in shared post-response assertions.\n")
    write_text(
        output / "README.generated.md",
        "# Generated API Test Workspace\n\n"
        "1. Put generated test cases into `cases/`.\n"
        "2. Update `case-manifest.json`.\n"
        "3. Fill in environment and shared scripts.\n"
        "4. Execute the suite and save raw results under `reports/` or `artifacts/`.\n",
    )
    write_text(output / "case-manifest.json", json.dumps(build_manifest(args.env_name, args.runner), indent=2, ensure_ascii=False) + "\n")

    print(json.dumps({
        "workspace": str(output),
        "runner": args.runner,
        "environment": args.env_name,
        "created": [str(d) for d in dirs],
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
