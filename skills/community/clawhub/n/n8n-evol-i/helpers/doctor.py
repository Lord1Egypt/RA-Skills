#!/usr/bin/env python3
"""Health check for an n8n-evol-I workspace."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import yaml

from helpers.workspace import workspace_root

OK, WARN, FAIL = "ok", "warn", "fail"
_ICONS = {OK: "✓", WARN: "⚠", FAIL: "✗"}


def _row(state: str, label: str, detail: str = "") -> tuple:
    return (state, label, detail)


def _fmt(state: str, label: str, detail: str = "") -> str:
    suffix = f" — {detail}" if detail else ""
    return f"  [{_ICONS[state]}] {label}{suffix}"


def _check_workspace(ws: Path) -> list:
    required = [ws / "n8n-config", ws / "n8n-workflows-template"]
    missing = [str(d) for d in required if not d.is_dir()]
    if missing:
        return [_row(FAIL, "workspace tree", f"missing: {', '.join(missing)}")]
    return [_row(OK, "workspace tree", str(ws))]


def _check_env_yaml(ws: Path, env: str) -> list:
    rows = []
    yaml_file = ws / "n8n-config" / f"{env}.yml"
    if not yaml_file.exists():
        return [_row(FAIL, f"{env}.yml", "file not found")]
    try:
        with open(yaml_file) as f:
            data = yaml.safe_load(f) or {}
        rows.append(_row(OK, f"{env}.yml", "parses OK"))
    except Exception as e:
        return [_row(FAIL, f"{env}.yml", str(e))]

    workflows = data.get("workflows", {}) or {}
    placeholder_keys = [
        k for k, v in workflows.items()
        if isinstance(v, dict) and (
            not v.get("id")
            or str(v.get("id", "")).startswith("your-")
            or v.get("id") == "placeholder"
        )
    ]
    if placeholder_keys:
        rows.append(_row(WARN, f"{env} workflow IDs", f"placeholder IDs: {', '.join(placeholder_keys)}"))
    elif workflows:
        rows.append(_row(OK, f"{env} workflow IDs", f"{len(workflows)} configured"))
    else:
        rows.append(_row(WARN, f"{env} workflow IDs", "no workflows configured yet"))
    return rows


def _check_n8n_api(ws: Path, env: str) -> list:
    try:
        from helpers.config import load_yaml, load_env
        import os
        data = load_yaml(env, ws)
        load_env(env, ws)
        api_key = os.environ.get("N8N_API_KEY", "")
        if not api_key:
            return [_row(WARN, f"{env} API key", "N8N_API_KEY not set in .env")]
        from helpers.n8n_client import N8nClient
        instance = data.get("n8n", {}).get("instanceName", "")
        N8nClient(base_url=instance, api_key=api_key).get("workflows", params={"limit": 1})
        return [_row(OK, f"{env} n8n API", "reachable")]
    except Exception as e:
        return [_row(FAIL, f"{env} n8n API", str(e))]


def _check_lock_scopes(ws: Path, env: str) -> list:
    """For every workspace template that wires Lock Acquire, verify its
    static-scope literal (if any) is registered in <env>.yml.lockScopes.

    Dynamic scopes (containing `$json`, etc.) are skipped — they require
    operator-managed lockScopes entries by definition. Static scopes that
    aren't registered get a WARN row pointing the operator at the gap; the
    error-handler cleanup will silently skip those workflows otherwise.

    Returns [] if no locked workflows are found.
    """
    template_dir = ws / "n8n-workflows-template"
    if not template_dir.is_dir():
        return []
    yaml_file = ws / "n8n-config" / f"{env}.yml"
    if not yaml_file.exists():
        return []
    try:
        with open(yaml_file) as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return []
    registered = set(data.get("lockScopes") or [])
    unregistered: list[tuple[str, str]] = []
    for tpl in sorted(template_dir.glob("*.template.json")):
        try:
            t = json.loads(tpl.read_text())
        except Exception:
            continue
        for node in t.get("nodes", []):
            if node.get("name") != "Lock Acquire":
                continue
            inputs = (node.get("parameters") or {}).get("workflowInputs") or {}
            scope_expr = ((inputs.get("value") or {}).get("scope") or "")
            # Reuse the helper's static-scope extractor without importing the
            # whole module (keep doctor's import surface minimal).
            static = _extract_static_scope_for_doctor(scope_expr)
            if static is None:
                continue  # dynamic — operator's responsibility
            if static not in registered:
                unregistered.append((tpl.stem.replace(".template", ""), static))
            break
    if unregistered:
        detail = ", ".join(f"{wf}→{s!r}" for wf, s in unregistered)
        return [_row(WARN, f"{env} lockScopes", f"unregistered: {detail}")]
    return []


def _extract_static_scope_for_doctor(scope_expr: str):
    """Mirror of helpers/add_lock_to_workflow.py:_extract_static_scope; kept
    inline here so doctor doesn't need to import the lock helper module."""
    import re as _re
    if not scope_expr:
        return None
    s = scope_expr.strip()
    if not s.startswith("="):
        return s
    m = _re.match(r"^=\{\{\s*(.+?)\s*\}\}$", s, _re.DOTALL)
    if not m:
        return None
    inner = m.group(1).strip()
    qm = _re.match(r'^([\'"])(.*)\1$', inner, _re.DOTALL)
    if not qm:
        return None
    literal = qm.group(2)
    if "${" in literal:
        return None
    return literal


def _check_templates(ws: Path) -> list:
    template_dir = ws / "n8n-workflows-template"
    templates = list(template_dir.glob("*.template.json")) if template_dir.is_dir() else []
    if not templates:
        return [_row(WARN, "workflow templates", "none found")]
    bad = []
    for t in templates:
        try:
            with open(t) as f:
                json.load(f)
        except Exception as e:
            bad.append(f"{t.name}: {e}")
    if bad:
        return [_row(FAIL, "workflow templates", "; ".join(bad))]
    return [_row(OK, "workflow templates", f"{len(templates)} parse OK")]


def _summarize_audit_response(report) -> list[tuple[str, int]]:
    """Walk an n8n audit response and return [(category, finding_count)] for non-empty categories.

    The audit response shape is documented at the per-category level (credentials,
    database, nodes, filesystem, instance) but the per-finding shape is not stable
    across n8n versions. Parser stays defensive: for each category we count the
    number of `sections` (or, if the per-category value is a list, the list length).
    Empty categories are silently dropped.
    """
    out: list[tuple[str, int]] = []

    if isinstance(report, dict):
        # Common shape: {"Credentials Risk Report": {...sections...}, "Database Risk Report": {...}, ...}
        # Or:           {"credentials": {...}, "database": {...}, ...}
        for category_name, payload in report.items():
            count = _count_findings_in_category(payload)
            if count:
                out.append((str(category_name), count))
    elif isinstance(report, list):
        # Alt shape: [{"risk": "credentials", "sections": [...]}, ...]
        for item in report:
            if not isinstance(item, dict):
                continue
            category_name = item.get("risk") or item.get("category") or "unknown"
            count = _count_findings_in_category(item)
            if count:
                out.append((str(category_name), count))

    return out


def _count_findings_in_category(payload) -> int:
    if isinstance(payload, dict):
        sections = payload.get("sections")
        if isinstance(sections, list):
            # Each section may contain a `location` array of N findings.
            total = 0
            for section in sections:
                if isinstance(section, dict):
                    locations = section.get("location") or section.get("locations")
                    total += len(locations) if isinstance(locations, list) else 1
            return total
        # Fallback: count top-level keys that aren't metadata.
        return len([k for k in payload if k not in ("risk", "category")])
    if isinstance(payload, list):
        return len(payload)
    return 0


def _check_audit(ws: Path, env: str) -> list:
    """Run POST /audit and emit a 3-state row per non-empty risk category.

    Per R-10: this check is opt-in via --with-audit; default doctor.py runs do
    NOT call audit. Per R-16: parser handles both documented shapes (per-category
    dict OR array of risk-report objects) and silently drops empty categories.
    Older n8n instances that lack the endpoint return 404 → graceful WARN row.
    """
    try:
        from helpers.config import load_yaml, load_env
        import os
        data = load_yaml(env, ws)
        load_env(env, ws)
        api_key = os.environ.get("N8N_API_KEY", "")
        if not api_key:
            return [_row(WARN, f"{env} audit", "N8N_API_KEY not set in .env")]
        from helpers.n8n_client import N8nClient
        instance = data.get("n8n", {}).get("instanceName", "")
        client = N8nClient(base_url=instance, api_key=api_key)
        report = client.post("audit", {})
    except Exception as e:
        msg = str(e)
        # Best-effort 404 detection without coupling to requests internals.
        if "404" in msg:
            return [_row(WARN, f"{env} audit", "endpoint not available (older n8n?)")]
        return [_row(FAIL, f"{env} audit", msg)]

    findings = _summarize_audit_response(report)
    if not findings:
        return [_row(OK, f"{env} audit", "no risks reported")]

    rows = []
    for category, count in findings:
        rows.append(_row(WARN, f"{env} audit / {category}", f"{count} finding(s)"))
    return rows


def _derive_verdict(rows: list) -> str:
    """Reduce a row list to a single machine-readable verdict.

    Verdicts (priority order — first match wins):
      - "api-unreachable"     : the n8n API row failed (auth, network, instance)
      - "needs-bootstrap"     : env yaml is missing entirely
      - "needs-mint"          : env yaml present but workflows.* still hold sentinel ids
      - "audit-findings"      : audit ran and at least one risk category is non-empty
      - "ok"                  : every row green or warn-only

    Used by CI / agent dispatch — stable schema, separate from the human report.
    """
    fail_labels = [label for state, label, _ in rows if state == FAIL]
    warn_labels = [label for state, label, _ in rows if state == WARN]
    for label in fail_labels:
        if "n8n API" in label:
            return "api-unreachable"
        if label.endswith(".yml") and "not found" in str(label):
            return "needs-bootstrap"
    for label in warn_labels:
        if "workflow IDs" in label and "placeholder" in label:
            return "needs-mint"
        if " audit / " in label:
            return "audit-findings"
        if "lockScopes" in label:
            return "lock-scopes-unregistered"
    if fail_labels:
        return "fail"
    return "ok"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", default=None, help="Workspace path. Default: ${PWD}/n8n-evol-I-workspace, or ${PWD} if its basename is already n8n-evol-I-workspace.")
    parser.add_argument("--env", default=None, help="Check a specific env (default: all configured envs)")
    parser.add_argument("--with-audit", action="store_true", dest="with_audit",
                        help="Also run POST /audit and report risk categories. Off by default.")
    parser.add_argument("--audit-only", action="store_true", dest="audit_only",
                        help="Run only the audit phase (skips workspace / env / template checks). Implies --with-audit.")
    parser.add_argument("--json", action="store_true", dest="json_mode",
                        help="Emit a structured {verdict, checks} JSON object instead of the human report. "
                             "Verdict values: ok | needs-bootstrap | needs-mint | api-unreachable | "
                             "audit-findings | lock-scopes-unregistered | fail. Stable for CI / agent dispatch.")
    args = parser.parse_args()

    if args.audit_only:
        args.with_audit = True

    ws = workspace_root(args.workspace)
    rows: list[tuple] = []

    if not args.audit_only:
        rows += _check_workspace(ws)

    config_dir = ws / "n8n-config"
    envs: list[str] = []
    if args.env:
        envs = [args.env]
    elif config_dir.is_dir():
        envs = [
            p.stem for p in sorted(config_dir.glob("*.yml"))
            if p.stem not in ("common", "deployment_order")
        ]

    if not envs:
        rows.append(_row(WARN, "environments", "no env configured — run bootstrap-env first"))
    else:
        for env in envs:
            if not args.audit_only:
                rows += _check_env_yaml(ws, env)
                rows += _check_n8n_api(ws, env)
                rows += _check_lock_scopes(ws, env)
            if args.with_audit:
                rows += _check_audit(ws, env)

    if not args.audit_only:
        rows += _check_templates(ws)

    if args.json_mode:
        print(json.dumps({
            "verdict": _derive_verdict(rows),
            "checks": [{"state": s, "label": l, "detail": d} for s, l, d in rows],
        }, indent=2))
    else:
        print("\nn8n-evol-I doctor report:")
        for state, label, detail in rows:
            print(_fmt(state, label, detail))
        print()

    if any(state == FAIL for state, _, _ in rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
