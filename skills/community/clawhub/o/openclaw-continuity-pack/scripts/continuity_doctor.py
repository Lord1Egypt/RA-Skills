#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


SOURCE_CHECKS: dict[str, list[str]] = {
    "src/gateway/thread-rollover.ts": [
        "assessThreadPressure(",
        "buildStructuredThreadHandoff(",
        "prepareThreadedSessionForChat(",
    ],
    "src/gateway/server-methods/chat.ts": [
        "prepareThreadedSessionForChat",
        "threadSessionKeys",
        "rolloverDegradedReason",
    ],
    "src/agents/pi-embedded-runner/session-manager-init.ts": [
        "__openclawThreadHandoff",
    ],
    "ui/src/ui/controllers/chat.ts": [
        "chatThreadId",
        "chatThreadSessionKeys",
        "chatRolloverState",
    ],
    "ui/src/ui/chat-event-reload.ts": [
        "shouldReloadHistoryForFinalEvent",
    ],
    "ui/src/ui/views/chat.ts": [
        "renderThreadContinuityNotice",
        "renderContextNotice",
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def run_source_checks(root: Path) -> dict[str, object]:
    failures: list[str] = []
    warnings: list[str] = []
    passed: list[str] = []

    for relative, anchors in SOURCE_CHECKS.items():
        target = root / relative
        if not target.exists():
            failures.append(f"missing file: {relative}")
            continue
        text = read_text(target)
        missing = [anchor for anchor in anchors if anchor not in text]
        if missing:
            failures.append(f"missing anchors in {relative}: {', '.join(missing)}")
        else:
            passed.append(relative)

    if not (root / "dist").exists():
        warnings.append("dist/ 不存在；如果准备部署，请先在源码树里构建。")

    return {
        "ok": len(failures) == 0,
        "root": str(root),
        "passed": passed,
        "warnings": warnings,
        "failures": failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether a target OpenClaw source tree still matches the continuity patch anchors.",
    )
    parser.add_argument("--source-root", required=True, help="Target OpenClaw source root")
    parser.add_argument("--json", action="store_true", help="Emit JSON output")
    args = parser.parse_args()

    root = Path(args.source_root).expanduser().resolve()
    result = run_source_checks(root)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ok"] else 1

    print("OpenClaw Continuity Doctor")
    print(f"Source root: {root}")
    print("Status: PASS" if result["ok"] else "Status: FAIL")

    if result["passed"]:
        print("\nPassed anchors:")
        for item in result["passed"]:
            print(f"  - {item}")

    if result["warnings"]:
        print("\nWarnings:")
        for item in result["warnings"]:
            print(f"  - {item}")

    if result["failures"]:
        print("\nFailures:")
        for item in result["failures"]:
            print(f"  - {item}")

    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
