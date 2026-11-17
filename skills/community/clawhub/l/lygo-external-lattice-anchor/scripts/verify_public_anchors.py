#!/usr/bin/env python3
"""
HTTP-check public verify components (Layer C).

Default (v1.1.1): true non-mutating verify
  - HTTP GET public endpoints only
  - Does NOT write report files (use --write-report to persist tests/*.json)
  - Does NOT run builders (use --build-manifest explicitly; executes skill-local Python)
No os.system / shell.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

SIG = "Delta9Phi963-EXTERNAL-LATTICE-ANCHOR-v1.1.1"
UA = "LYGO-ExternalLatticeAnchor/1.1.1 (+https://eternalhaven.ca)"

# Fallback when no local manifest (no local code execution required)
DEFAULT_ENDPOINTS = [
    {
        "id": "immutable_anchors",
        "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/network_builder/IMMUTABLE_ANCHORS.json",
        "role": "ledger",
        "verify": "http_required",
    },
    {
        "id": "haven_star_chart",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/HavenStarChart.html",
        "role": "world_map",
        "verify": "http_required",
    },
    {
        "id": "kernel_egg_retrieval",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/KernelEggRetrieval.html",
        "role": "public_verify_ui",
        "verify": "http_required",
    },
    {
        "id": "pages_stack",
        "url": "https://deepseekoracle.github.io/lygo-protocol-stack/",
        "role": "public_http_mirror",
        "verify": "http_required",
    },
    {
        "id": "eternalhaven_hub",
        "url": "https://eternalhaven.ca/",
        "role": "public_hub",
        "verify": "http_required",
    },
    {
        "id": "sovereign_seeds_snapshot",
        "url": "https://raw.githubusercontent.com/DeepSeekOracle/lygo-protocol-stack/main/docs/sovereign_seeds_snapshot/registry.json",
        "role": "sovereign_mirror",
        "verify": "http_soft",
    },
    {
        "id": "clawhub_publisher",
        "url": "https://clawhub.ai/deepseekoracle",
        "role": "skill_registry",
        "verify": "http_soft",
    },
]


def fetch(url: str, timeout: int = 25) -> tuple[int, bytes | None, str | None]:
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(), None
    except urllib.error.HTTPError as e:
        return e.code, None, str(e)
    except Exception as e:
        return 0, None, str(e)


def stack_root() -> Path:
    env = os.environ.get("LYGO_STACK_ROOT", "").strip()
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "docs" / "network_builder" / "IMMUTABLE_ANCHORS.json").is_file():
            return p
    return Path.cwd()


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Layer C public HTTP verify. Default: GET-only, zero filesystem writes, no builder. "
            "Opt-in: --write-report (tests/), --build-manifest (executes skill-local builder; needs --i-trust-stack)."
        )
    )
    ap.add_argument("--manifest", default="")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--stack-root", default="")
    ap.add_argument(
        "--i-trust-stack",
        action="store_true",
        help="Required with --build-manifest: affirm LYGO_STACK_ROOT / --stack-root is code you trust",
    )
    ap.add_argument(
        "--build-manifest",
        action="store_true",
        help=(
            "OPT-IN EXECUTE: if manifest missing, run skill-local build_public_verify_manifest.py "
            "in-process (runpy; may write docs/public_verify_manifest.json). Requires --i-trust-stack."
        ),
    )
    ap.add_argument(
        "--write-report",
        action="store_true",
        help="OPT-IN WRITE: persist tests/public_anchors_last_run.json under stack root",
    )
    ap.add_argument(
        "--no-write-report",
        action="store_true",
        help="Deprecated alias: default already does not write reports",
    )
    args = ap.parse_args()
    stack = Path(args.stack_root).resolve() if args.stack_root else stack_root()
    write_report = bool(args.write_report) and not args.no_write_report

    man_path = Path(args.manifest) if args.manifest else stack / "docs" / "public_verify_manifest.json"
    built = False
    if args.build_manifest:
        if not args.i_trust_stack:
            print(
                json.dumps(
                    {
                        "verdict": "BLOCKED",
                        "errors": ["build_manifest_requires_i_trust_stack"],
                        "hint": "pass --i-trust-stack only for a stack checkout you control",
                    }
                ),
                file=sys.stderr,
            )
            return 2
        if not man_path.is_file():
            builder = Path(__file__).resolve().parent / "build_public_verify_manifest.py"
            if builder.is_file():
                from _safe_invoke import run_python_script  # noqa: E402

                code, out = run_python_script(
                    builder,
                    ["--stack-root", str(stack)],
                    cwd=stack,
                    stack=stack,
                )
                built = code == 0
                if code != 0:
                    print(f"build_manifest_failed code={code} {out[:300]}", file=sys.stderr)

    endpoints = []
    if man_path.is_file():
        man = json.loads(man_path.read_text(encoding="utf-8"))
        endpoints = man.get("public_endpoints") or []
    else:
        endpoints = list(DEFAULT_ENDPOINTS)

    ALLOWED_VERIFY = {"http_required", "http_soft", "skip"}
    results = []
    hard_fail = False
    for ep in endpoints:
        if not isinstance(ep, dict):
            continue
        url = ep.get("url")
        if not url:
            continue
        # HTTPS only (no file://, no SSRF to localhost via http cleartext policy)
        if not str(url).startswith("https://"):
            results.append(
                {
                    "id": ep.get("id"),
                    "url": url,
                    "ok": False,
                    "error": "https_only",
                    "note": "non-https endpoints are skipped for safety",
                }
            )
            continue
        vmode = str(ep.get("verify") or "http_soft")
        if vmode not in ALLOWED_VERIFY:
            vmode = "http_soft"  # unknown verify strings never escalate to dispatch
        if vmode == "skip":
            results.append({"id": ep.get("id"), "url": url, "ok": True, "verify": "skip", "skipped": True})
            continue
        # role is classification only — never used for code dispatch
        status, body, err = fetch(url)
        ok = 200 <= status < 400
        item = {
            "id": ep.get("id"),
            "url": url,
            "http_status": status,
            "ok": ok,
            "role": ep.get("role"),
            "verify": vmode,
            "error": err,
            "bytes": len(body) if body else 0,
        }
        if body and url.endswith(".json") and ok:
            try:
                data = json.loads(body.decode("utf-8", errors="replace"))
                if isinstance(data, dict):
                    if "registry_merkle_root" in data:
                        item["registry_merkle_root"] = data.get("registry_merkle_root")
                    if "version" in data and "immutable_anchors" in data:
                        item["anchors_version"] = data.get("version")
            except Exception:
                item["json_parse"] = False
        if vmode == "http_required" and not ok:
            hard_fail = True
        results.append(item)

    local_sov = stack / "data" / "sovereign_seeds" / "registry.json"
    if local_sov.is_file():
        try:
            lr = json.loads(local_sov.read_text(encoding="utf-8")).get("registry_merkle_root")
            pub = next((r for r in results if r.get("id") == "sovereign_seeds_snapshot"), None)
            if pub and pub.get("registry_merkle_root") and lr:
                item = {
                    "id": "sovereign_root_sync",
                    "local": lr,
                    "public": pub.get("registry_merkle_root"),
                    "match": lr == pub.get("registry_merkle_root"),
                }
                if not item["match"]:
                    item["note"] = "mirror lag or unpublished snapshot — re-run local snapshot + git push"
                results.append(item)
        except Exception:
            pass

    report = {
        "signature": SIG,
        "created_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "verdict": "PUBLIC_OK" if not hard_fail else "PUBLIC_DEGRADED",
        "checked": len(results),
        "results": results,
        "mode": {
            "network": "http_get_only",
            "auto_build_manifest": False,
            "build_manifest_opt_in": bool(args.build_manifest),
            "built_manifest": built,
            "write_report": write_report,
            "shell": False,
            "os_system": False,
        },
        "user_protection": {
            "do_not_trust_public_over_local": True,
            "if_mismatch_prefer_local_verify": True,
            "trust_stack_root": "only use LYGO_STACK_ROOT you control",
        },
    }

    if write_report:
        out = stack / "tests" / "public_anchors_last_run.json"
        try:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            report["report_path"] = str(out)
        except OSError as e:
            report["report_write_error"] = str(e)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"verdict={report['verdict']} checked={report['checked']}")
        for r in results:
            if "http_status" in r:
                print(f"  {r.get('id')}: {r.get('http_status')} ok={r.get('ok')} {r.get('url','')[:70]}")
            else:
                print(f"  {r.get('id')}: {r}")

    return 0 if not hard_fail else 1


if __name__ == "__main__":
    raise SystemExit(main())
