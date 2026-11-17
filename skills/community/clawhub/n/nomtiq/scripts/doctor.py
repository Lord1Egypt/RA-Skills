#!/usr/bin/env python3
from __future__ import annotations

"""Nomtiq setup diagnostics. Never prints credential values."""

import argparse
import json
import os
import sys


def build_report() -> dict:
    amap = bool(os.environ.get("AMAP_WEBSERVICE_KEY", "").strip())
    amap_legacy = bool(os.environ.get("AMAP_KEY", "").strip())
    amap_secret = bool(os.environ.get("AMAP_WEBSERVICE_SECRET", "").strip())
    serper = bool(os.environ.get("SERPER_API_KEY", "").strip())
    python_ok = sys.version_info >= (3, 9)

    warnings = []
    if amap_legacy and not amap:
        warnings.append("AMAP_KEY is deprecated; rename it to AMAP_WEBSERVICE_KEY.")
    if amap_secret and not (amap or amap_legacy):
        warnings.append("AMAP_WEBSERVICE_SECRET is set but no Amap key is available.")
    if not amap and not amap_legacy and not serper:
        warnings.append("No map provider is configured yet.")

    return {
        "status": "ok" if python_ok and (amap or amap_legacy or serper) else "setup_required",
        "python": {
            "version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "supported": python_ok,
        },
        "providers": {
            "china_mainland": {
                "provider": "amap",
                "configured": amap or amap_legacy,
                "digital_signature_configured": amap_secret,
            },
            "global": {
                "provider": "serper",
                "configured": serper,
            },
        },
        "warnings": warnings,
        "secrets_printed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Nomtiq setup doctor (never prints key values)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Nomtiq doctor: {report['status']}")
        print(f"Python: {report['python']['version']} ({'ok' if report['python']['supported'] else 'needs 3.9+'})")
        print(f"China mainland / Amap: {'configured' if report['providers']['china_mainland']['configured'] else 'not configured'}")
        print(f"Global / Serper: {'configured' if report['providers']['global']['configured'] else 'not configured'}")
        for warning in report["warnings"]:
            print(f"Warning: {warning}")
    return 0 if report["python"]["supported"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
