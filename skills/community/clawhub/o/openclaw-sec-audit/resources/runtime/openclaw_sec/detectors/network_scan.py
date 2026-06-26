from __future__ import annotations

from openclaw_sec.models import Finding
from openclaw_sec.utils import run_command


def scan_network() -> tuple[list[Finding], dict[str, object], list[str]]:
    notes: list[str] = []
    result = run_command(["ss", "-lntup"], timeout=8)
    if not result.ok:
        notes.append(f"HOST-001 skipped: unable to run ss ({result.stderr or 'command failed'})")
        return [], {"listening_ports": []}, notes

    entries: list[dict[str, str]] = []
    risky: list[str] = []
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("Netid") or stripped.startswith("State"):
            continue
        parts = stripped.split()
        if len(parts) < 5:
            continue
        local_address = parts[3]
        process = parts[-1]
        entries.append({"local_address": local_address, "process": process})
        if any(token in local_address for token in ("0.0.0.0:", "[::]:", "*:")):
            risky.append(f"{local_address} {process}")

    findings: list[Finding] = []
    if risky:
        findings.append(
            Finding(
                id="HOST-001",
                title="Wildcard listening sockets detected",
                category="network",
                severity="high",
                confidence="medium",
                heuristic=False,
                evidence=risky[:12],
                risk="Wildcard binds can expose services beyond localhost, especially on VPS or bridged environments.",
                recommendation="Confirm every wildcard listener is intentional and protected by firewall rules, auth, or loopback binding.",
                references=["ss -lntup"],
            )
        )
    return findings, {"listening_ports": entries[:50]}, notes
