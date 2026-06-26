from __future__ import annotations

from pathlib import Path
from typing import Any

from openclaw_sec.models import AuditContext, Finding
from openclaw_sec.utils import flatten_json, load_json


MESSAGE_CHANNEL_KEYS = {"telegram", "qqbot", "discord", "slack", "lark", "webhook"}


def load_and_scan_config(context: AuditContext) -> tuple[list[Finding], dict[str, Any] | None]:
    findings: list[Finding] = []
    config_path = context.config_path
    if not config_path.exists():
        findings.append(
            Finding(
                id="CFG-001",
                title="OpenClaw config file not found",
                category="config",
                severity="info",
                confidence="high",
                heuristic=False,
                evidence=[str(config_path)],
                risk="The audit could not inspect explicit OpenClaw configuration and may miss config-specific risks.",
                recommendation="Confirm whether OpenClaw is using a different config path or only default settings.",
                references=["OpenClaw config path"],
            )
        )
        return findings, None

    try:
        data = load_json(config_path)
    except Exception as exc:
        findings.append(
            Finding(
                id="CFG-002",
                title="OpenClaw config file could not be parsed",
                category="config",
                severity="high",
                confidence="high",
                heuristic=False,
                evidence=[f"{config_path}: {exc}"],
                risk="Malformed config can hide insecure settings, break runtime assumptions, or make the audit unreliable.",
                recommendation="Fix JSON syntax or regenerate the config before trusting the deployment.",
                references=["OpenClaw config parser"],
            )
        )
        return findings, None

    findings.extend(_scan_network_bind_hints(data))
    findings.extend(_scan_auth_hints(data))
    findings.extend(_scan_sandbox_hints(data))
    findings.extend(_scan_exec_hints(data))
    findings.extend(_scan_channel_hints(data))
    return findings, data


def _scan_network_bind_hints(data: dict[str, Any]) -> list[Finding]:
    risky: list[str] = []
    severe = "high"
    for key, value in flatten_json(data):
        if not isinstance(value, str):
            continue
        lowered_key = key.lower()
        lowered_value = value.lower().strip()
        if "baseurl" in lowered_key or lowered_value.startswith("http"):
            continue
        if any(token in lowered_key for token in ("bind", "listen", "host", "address")):
            if lowered_value in {"0.0.0.0", "::", "[::]", "*"}:
                risky.append(f"{key}=<wildcard bind>")
                severe = "critical"
            elif lowered_value.startswith(("10.", "192.168.", "172.")) or lowered_value == "lan":
                risky.append(f"{key}={_describe_private_bind(lowered_value)}")
    if not risky:
        return []
    return [
        Finding(
            id="NET-001",
            title="Potential non-loopback bind detected in OpenClaw config",
            category="network",
            severity=severe,
            confidence="medium",
            heuristic=True,
            evidence=risky[:8],
            risk="A non-loopback bind can expose control surfaces or local tools beyond the host.",
            recommendation="Restrict listener addresses to 127.0.0.1 or a private control plane unless external exposure is intentional and protected.",
            references=["OpenClaw bind/listen heuristic"],
        )
    ]


def _scan_auth_hints(data: dict[str, Any]) -> list[Finding]:
    auth = data.get("auth")
    channels_present = any(key in data for key in MESSAGE_CHANNEL_KEYS)
    if auth is None:
        return [
            Finding(
                id="AUTH-001",
                title="Auth configuration is missing",
                category="config",
                severity="critical" if channels_present else "high",
                confidence="medium",
                heuristic=True,
                evidence=["auth section missing"],
                risk="Missing auth hints can mean message channels or remote operations are protected only by network placement.",
                recommendation="Define explicit auth profiles and ensure externally reachable channels require them.",
                references=["OpenClaw auth heuristic"],
            )
        ]
    findings: list[Finding] = []
    profiles = auth.get("profiles") if isinstance(auth, dict) else None
    if profiles in ({}, [], None):
        findings.append(
            Finding(
                id="AUTH-001",
                title="Auth profiles appear empty or missing",
                category="config",
                severity="critical" if channels_present else "high",
                confidence="medium",
                heuristic=True,
                evidence=["auth.profiles is empty or missing"],
                risk="Weak or absent auth increases the chance of unauthorized command execution or message-triggered actions.",
                recommendation="Populate auth profiles or confirm the deployment is isolated to a trusted local environment.",
                references=["OpenClaw auth heuristic"],
            )
        )
    for key, value in flatten_json(auth, "auth"):
        lowered_key = key.lower()
        if any(token in lowered_key for token in ("enabled", "mode", "token")):
            rendered = str(value).strip().lower()
            if rendered in {"false", "off", "disabled", "none", ""}:
                findings.append(
                    Finding(
                        id="AUTH-001",
                        title="Auth appears explicitly disabled or weak",
                        category="config",
                        severity="critical" if channels_present else "high",
                        confidence="medium",
                        heuristic=True,
                        evidence=[f"{key}={_describe_disabled_setting(rendered)}"],
                        risk="Explicitly weakened auth settings can expose automation endpoints to unintended callers.",
                        recommendation="Enable a non-empty auth mode or gate the instance behind trusted local-only access.",
                        references=["OpenClaw auth heuristic"],
                    )
                )
                break
    return findings


def _scan_sandbox_hints(data: dict[str, Any]) -> list[Finding]:
    evidence: list[str] = []
    for key, value in flatten_json(data):
        lowered_key = key.lower()
        lowered_value = str(value).strip().lower()
        if lowered_key.endswith("nosandbox") and lowered_value == "true":
            evidence.append(f"{key}=<disabled sandbox hint>")
        if "sandbox" in lowered_key and lowered_value in {"false", "off", "disabled", "none"}:
            evidence.append(f"{key}={_describe_disabled_setting(lowered_value)}")
    if not evidence:
        return []
    return [
        Finding(
            id="EXEC-001",
            title="Sandbox appears disabled in config",
            category="config",
            severity="high",
            confidence="high",
            heuristic=True,
            evidence=evidence[:8],
            risk="Disabled sandboxing broadens the impact of compromised prompts, plugins, or remote instructions.",
            recommendation="Prefer sandboxed execution where possible and isolate the runtime when sandboxing must be disabled.",
            references=["OpenClaw sandbox heuristic"],
        )
    ]


def _scan_exec_hints(data: dict[str, Any]) -> list[Finding]:
    tools = data.get("tools")
    if not isinstance(tools, dict):
        return []
    evidence: list[str] = []
    allow = tools.get("allow")
    if isinstance(allow, list) and "exec" in allow:
        evidence.append("tools.allow includes exec capability")
    exec_cfg = tools.get("exec")
    if isinstance(exec_cfg, dict):
        security = str(exec_cfg.get("security", "")).lower()
        ask = str(exec_cfg.get("ask", "")).lower()
        if security in {"full", "unrestricted"}:
            evidence.append("tools.exec.security indicates unrestricted mode")
        if ask in {"off", "false", "disabled"}:
            evidence.append("tools.exec.ask appears disabled")
    if not evidence:
        return []
    return [
        Finding(
            id="EXEC-002",
            title="Elevated or unrestricted exec appears enabled",
            category="config",
            severity="high",
            confidence="high",
            heuristic=True,
            evidence=evidence,
            risk="Unrestricted local execution materially increases blast radius if OpenClaw receives unsafe input or untrusted tasks.",
            recommendation="Gate exec with approvals, least privilege, and host isolation if remote or multi-user access exists.",
            references=["OpenClaw exec heuristic"],
        )
    ]


def _scan_channel_hints(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for channel in MESSAGE_CHANNEL_KEYS:
        section = data.get(channel)
        if not isinstance(section, dict) or not section:
            continue
        if any(key in section for key in ("allowFrom", "allow_from", "whitelist")):
            continue
        findings.append(
            Finding(
                id="CHAN-001",
                title=f"{channel} channel may be missing sender allowlist controls",
                category="config",
                severity="medium",
                confidence="low",
                heuristic=True,
                evidence=[f"{channel} configured without allowFrom/whitelist hint"],
                risk="Message-driven automations are safer when the accepted sender set is explicit.",
                recommendation="Add sender allowlists or equivalent identity checks for message-facing channels.",
                references=["OpenClaw channel heuristic"],
            )
        )
    return findings


def _describe_private_bind(value: str) -> str:
    if value == "lan":
        return "<lan bind hint>"
    return "<private network address>"


def _describe_disabled_setting(value: str) -> str:
    if value == "":
        return "<empty>"
    return "<disabled>"
