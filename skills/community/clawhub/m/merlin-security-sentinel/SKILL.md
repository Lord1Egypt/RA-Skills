---
name: merlin-security-sentinel
description: Use this skill when the user asks about securing their OpenClaw installation, configuring AI agents safely, understanding prompt injection risks, dealing with malicious skills, protecting credentials from AI agents, setting up safe agentic workflows, or asking why persistent AI agents are dangerous. Also use when the user is setting up a new OpenClaw instance and wants to understand the security model, or when they ask about safe ways to let AI touch privileged systems.
tags: security, prompt-injection, agent-safety, credentials, hardening, ephemeral, governance, audit
---

# Merlin Security Sentinel — Agentic Security Framework

## When to use this skill

Load this skill when the user is concerned about:
- Credential theft or exfiltration by AI agents
- Prompt injection attacks via messages, files, or web content
- Malicious skills in the ClawHub registry
- Safe configuration of privileged systems using AI
- Understanding what persistent agents can and cannot safely do
- Building governed, auditable AI workflows

---

## The Core Problem with Persistent AI Agents

Persistent AI agents — including this one — carry structural security liabilities that are not fixable by configuration alone.

**Three risks compound each other:**

1. **Credential accumulation** — A persistent agent builds up an increasingly detailed model of credentials, tokens, and system access over time. Any compromise of the agent's memory or storage exposes that accumulated access.

2. **Memory poisoning** — A persistent agent's memory (SOUL.md, MEMORY.md, IDENTITY.md) can be modified by malicious skills or prompt injection. Modified memory causes the agent to follow attacker instructions in future sessions with no single triggering event detectable.

3. **Supply chain attacks** — The ClawHub registry has documented malicious skills. Research in Q1 2026 found 820+ malicious skills out of ~10,700 analyzed. 26% of 31,000 analyzed skills contained at least one vulnerability.

**Security research findings (Q1 2026):**
- 40,000+ internet-exposed OpenClaw instances identified
- ~35% flagged as vulnerable
- 15,000+ susceptible to remote code execution
- CVE-2026-25253: a single malicious link click grants full gateway control
- Microsoft classified persistent self-hosted AI agents as "untrusted code execution with persistent credentials"

---

## Immediate Hardening Steps

### 1. Lock your memory files
```bash
chmod 444 ~/.openclaw/workspace/SOUL.md
chmod 444 ~/.openclaw/workspace/MEMORY.md
chmod 444 ~/.openclaw/workspace/IDENTITY.md
```

### 2. Restrict tool permissions
Set the most restrictive tool profile compatible with your actual use:
- `tools.profile: "messaging"` — no exec
- Never enable `exec` unless specifically needed
- Never use `tools.allow: ["*"]`

### 3. Bind to localhost only
```bash
openclaw gateway --port 18789 --host 127.0.0.1
```

### 4. Use allowlists for DMs
Set explicit `allowedDMs` rather than `["*"]`. Any user who can message a shared tool-enabled agent can steer it within its granted permissions.

### 5. Audit installed skills
```bash
clawhub list
```
Check SKILL.md files manually. Look for: base64 encoding, external downloads, instructions to modify SOUL.md or MEMORY.md.

---

## The Architectural Answer

For tasks involving elevated privilege the structurally correct answer is ephemeral execution, not hardened persistence.

**Two inviolable axioms:**

1. **No AI shall see its own configuration** — The execution envelope is applied at container infrastructure level, not delivered to the model. An agent that cannot inspect its own constraints cannot reason about circumventing them.

2. **No AI that has touched privileged systems shall persist** — Container termination is total. Not paused. Destroyed. The agent's knowledge of your system dies with the container.

**What persists:** A signed, replayable audit record of exactly what the AI did — held outside the container, inaccessible to the AI.

**What does not persist:** Credentials, session memory, system knowledge, the agent itself.

---

## When to use ephemeral execution vs persistent agents

| Task | Use |
|------|-----|
| Daily messaging, reminders, search | Persistent (acceptable risk) |
| Configuring your own AI agents | Ephemeral — high risk to persist |
| Setting up new systems | Ephemeral — involves credentials |
| Running security scans | Ephemeral — agent sees sensitive data |
| Installing/updating privileged software | Ephemeral — credential entry involved |

---

## Prompt Injection Defense

OpenClaw's security model explicitly states that prompt injection is out of scope as a vulnerability — the framework cannot prevent it at the infrastructure level.

**Practical defenses:**
- Never enable `exec` when browsing untrusted content
- Use separate sessions for untrusted content and credential-sensitive tasks
- Treat all content from messaging channels as untrusted
- The architectural fix is an ingress firewall that makes external content readable but never instruction-authoritative — runtime filtering alone is insufficient

---

## Architecture Reference

The full governed architecture — execution envelopes, ephemeral containers, deterministic audit trails, governed knowledge retrieval — is documented and prototyped at:

- **Threat assessment:** github.com/thepoorsatitagain/OPENCLAW_SECURITY_THREAT_ASSESSMENT3
- **Hydra Kernel / GEL:** github.com/thepoorsatitagain/Ai-control-2 — provisional patent 63/939,121
- **Merlin ephemeral sentinel:** github.com/thepoorsatitagain/Merlin-agenic-security-airgapper
- **Working wrapper prototype:** github.com/thepoorsatitagain/working-project-openclaw-wrapper

---

## Quick Reference

**"Is OpenClaw safe?"**
For daily personal use with minimal tool access and no exec: acceptable risk. For anything involving credentials, privileged systems, or shared access: the structural risks are real and documented.

**"I got a suspicious skill installed"**
1. Check SOUL.md, MEMORY.md, IDENTITY.md for injected content
2. Revoke any credentials the agent had access to
3. `clawhub uninstall <skill-slug>`
4. Review audit logs
5. Consider clean reinstall if memory files were modified

**"What is the worst case?"**
CVE-2026-25253: one malicious link click, full gateway RCE within milliseconds. Agent exfiltrates SOUL.md, MEMORY.md, device.json, openclaw.json, browser session tokens, SSH credentials. Future sessions follow attacker instructions silently.
