from __future__ import annotations

import platform
import socket
from pathlib import Path

from openclaw_sec.models import Finding
from openclaw_sec.utils import read_text, run_command


def scan_host() -> tuple[list[Finding], dict[str, object], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    host_info = {
        "hostname": socket.gethostname(),
        "platform": platform.system(),
        "platform_release": platform.release(),
    }

    ssh_findings, ssh_notes = _scan_ssh_config()
    findings.extend(ssh_findings)
    notes.extend(ssh_notes)

    brute_findings, brute_notes = _scan_bruteforce_hints()
    findings.extend(brute_findings)
    notes.extend(brute_notes)

    firewall_findings, firewall_notes = _scan_firewall()
    findings.extend(firewall_findings)
    notes.extend(firewall_notes)

    fail2ban_findings, fail2ban_notes = _scan_fail2ban()
    findings.extend(fail2ban_findings)
    notes.extend(fail2ban_notes)

    umask_findings, umask_notes, umask_value = _scan_umask()
    findings.extend(umask_findings)
    notes.extend(umask_notes)
    if umask_value:
        host_info["umask"] = umask_value

    return findings, host_info, notes


def _scan_ssh_config() -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    config_paths = [Path("/etc/ssh/sshd_config")]
    include_dir = Path("/etc/ssh/sshd_config.d")
    if include_dir.exists():
        config_paths.extend(sorted(include_dir.glob("*.conf")))
    merged_text = "\n".join(read_text(path) for path in config_paths if path.exists())
    if not merged_text:
        notes.append("HOST-002/HOST-003 skipped: sshd config not readable")
        return findings, notes

    effective: dict[str, str] = {}
    for line in merged_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split(None, 1)
        if len(parts) == 2:
            effective[parts[0].lower()] = parts[1].strip()

    permit_root = effective.get("permitrootlogin", "")
    if permit_root.lower() == "yes":
        findings.append(
            Finding(
                id="HOST-002",
                title="SSH root login is enabled",
                category="host",
                severity="critical",
                confidence="high",
                heuristic=False,
                evidence=[f"PermitRootLogin {permit_root}"],
                risk="Root SSH access removes an isolation layer and raises the impact of brute force or credential theft.",
                recommendation="Set PermitRootLogin no and use sudo from a non-root administrative account.",
                references=["/etc/ssh/sshd_config"],
            )
        )
    elif permit_root.lower() in {"without-password", "prohibit-password"}:
        findings.append(
            Finding(
                id="HOST-002",
                title="SSH root login is partially enabled",
                category="host",
                severity="high",
                confidence="high",
                heuristic=False,
                evidence=[f"PermitRootLogin {permit_root}"],
                risk="Key-based root SSH access still exposes a high-value account directly to the network.",
                recommendation="Disable direct root SSH login unless you have a tightly controlled operational reason.",
                references=["/etc/ssh/sshd_config"],
            )
        )

    password_auth = effective.get("passwordauthentication", "")
    if password_auth.lower() == "yes":
        findings.append(
            Finding(
                id="HOST-003",
                title="SSH password authentication is enabled",
                category="host",
                severity="high",
                confidence="high",
                heuristic=False,
                evidence=[f"PasswordAuthentication {password_auth}"],
                risk="Password-based SSH significantly increases brute force and credential stuffing exposure on internet-facing hosts.",
                recommendation="Disable PasswordAuthentication and use SSH keys with rate limiting or allowlists.",
                references=["/etc/ssh/sshd_config"],
            )
        )
    return findings, notes


def _scan_bruteforce_hints() -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    auth_log = Path("/var/log/auth.log")
    evidence_count = 0
    if auth_log.exists():
        text = read_text(auth_log, limit=512 * 1024)
        evidence_count += sum(1 for line in text.splitlines() if "Failed password" in line or "Invalid user" in line)
    else:
        result = run_command(["journalctl", "-u", "ssh", "-n", "200", "--no-pager"], timeout=8)
        if result.ok:
            evidence_count += sum(1 for line in result.stdout.splitlines() if "Failed password" in line or "Invalid user" in line)
        else:
            notes.append("HOST-004 skipped: auth.log and journalctl ssh output unavailable")
    if evidence_count:
        findings.append(
            Finding(
                id="HOST-004",
                title="SSH brute-force evidence detected",
                category="host",
                severity="high" if evidence_count >= 10 else "medium",
                confidence="medium",
                heuristic=False,
                evidence=[f"{evidence_count} failed SSH authentication lines observed"],
                risk="Repeated SSH failures suggest the host is being probed or attacked, which increases urgency for hardening controls.",
                recommendation="Review exposed SSH reachability, disable password auth, and ensure firewall and fail2ban protections are active.",
                references=["auth.log", "journalctl -u ssh"],
            )
        )
    return findings, notes


def _scan_firewall() -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    ufw = run_command(["ufw", "status"], timeout=5)
    if ufw.ok and "Status: active" in ufw.stdout:
        return findings, notes
    nft = run_command(["nft", "list", "ruleset"], timeout=5)
    if nft.ok and nft.stdout.strip():
        return findings, notes
    iptables = run_command(["iptables", "-S"], timeout=5)
    if iptables.ok and any(line.startswith("-P") or line.startswith("-A") for line in iptables.stdout.splitlines()):
        return findings, notes
    findings.append(
        Finding(
            id="HOST-005",
            title="No clear firewall control was detected",
            category="host",
            severity="medium",
            confidence="low",
            heuristic=True,
            evidence=["ufw inactive/unavailable, nftables empty/unavailable, iptables unavailable or empty"],
            risk="Without host firewall controls, accidentally exposed listeners rely entirely on application-level protections.",
            recommendation="Enable ufw, nftables, or equivalent host firewall rules that restrict remote access to expected ports only.",
            references=["ufw", "nft", "iptables"],
        )
    )
    return findings, notes


def _scan_fail2ban() -> tuple[list[Finding], list[str]]:
    findings: list[Finding] = []
    notes: list[str] = []
    systemctl = run_command(["systemctl", "is-active", "fail2ban"], timeout=5)
    if systemctl.ok and systemctl.stdout.strip() == "active":
        return findings, notes
    client = run_command(["fail2ban-client", "ping"], timeout=5)
    if client.ok:
        return findings, notes
    findings.append(
        Finding(
            id="HOST-006",
            title="fail2ban was not detected",
            category="host",
            severity="medium",
            confidence="medium",
            heuristic=False,
            evidence=["systemctl is-active fail2ban != active", "fail2ban-client ping failed"],
            risk="Missing login throttling leaves SSH and other auth endpoints more exposed to brute force attempts.",
            recommendation="Install and enable fail2ban or another equivalent authentication abuse control if the host is remotely reachable.",
            references=["fail2ban"],
        )
    )
    return findings, notes


def _scan_umask() -> tuple[list[Finding], list[str], str | None]:
    findings: list[Finding] = []
    notes: list[str] = []
    result = run_command(["bash", "-lc", "umask"], timeout=5)
    if not result.ok:
        notes.append("HOST-007 skipped: unable to read shell umask")
        return findings, notes, None
    umask = result.stdout.strip()
    if umask in {"000", "002", "0002"}:
        findings.append(
            Finding(
                id="HOST-007",
                title="Host umask appears permissive",
                category="host",
                severity="medium" if umask.startswith("000") else "low",
                confidence="medium",
                heuristic=True,
                evidence=[f"umask {umask}"],
                risk="A permissive umask increases the chance that newly created config, logs, or artifacts become readable by other local users.",
                recommendation="Use a more restrictive default umask such as 027 or 077 for security-sensitive automation accounts.",
                references=["shell umask"],
            )
        )
    return findings, notes, umask
