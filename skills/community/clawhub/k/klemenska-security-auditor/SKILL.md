---
name: security-auditor
description: "Scan and audit installed skills for security risks, suspicious patterns, and permission overreach. Use when: (1) before installing a new skill; (2) periodically reviewing installed skills; (3) before granting skill permissions; (4) when explicitly asked to audit skills or check for vulnerabilities."
---

# Security Auditor

Audit skills for security risks before installing or using them.

## Purpose

Skills can request permissions and access that may be:
- Overreaching (accessing data they shouldn't need)
- Suspicious (behaving oddly, phoning home, etc.)
- Outdated (known vulnerabilities in dependencies)

This skill helps you audit them.

## When to Run

| Trigger | Action |
|---------|--------|
| Before installing a new skill | Full audit |
| Periodic review | Quick scan of installed skills |
| Suspicious behavior | Deep analysis |
| Permission review | Check requested permissions |

## Audit Workflow

### Step 1: Quick Scan

```bash
python3 scripts/audit.py --scan
```

Checks:
- File access patterns
- Network access requests
- Suspicious API usage
- Permission requests

### Step 2: Detailed Audit

```bash
python3 scripts/audit.py --audit <skill-path>
```

Performs deep analysis:
- Code pattern analysis
- Dependency checking
- Permission mapping
- Risk scoring

### Step 3: Generate Report

```bash
python3 scripts/audit.py --report <skill-path> --output report.md
```

Creates detailed security report.

### Step 4: Compare Skills

```bash
python3 scripts/audit.py --compare <skill1-path> <skill2-path>
```

Compare security posture of two skills.

## Risk Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🟢 LOW | Minimal risk, standard permissions | Safe to install |
| 🟡 MEDIUM | Some overreach, review recommended | Read code before install |
| 🔴 HIGH | Significant risks, careful review required | Do not install without review |
| ⛔ CRITICAL | Dangerous patterns detected | Do not install |

## Red Flags to Watch For

### File Access
- Accessing `~/.ssh/` or `~/.aws/`
- Reading `*password*`, `*secret*`, `*key*` files
- Writing to system directories
- Accessing other users' directories

### Network
- Exfiltrating data to unknown servers
- DNS rebinding patterns
- Encrypted payloads to unfamiliar domains

### Permissions
- Requesting exec with no scope limitation
- Reading memory or process info
- Keylogging or screenshot capabilities
- Accessing other installed skills' data

### Code Patterns
- Obfuscated code
- Dynamic code generation
- Shell commands without sanitization
- Credential harvesting patterns

## Files

- `scripts/audit.py` — Main audit script
- `scripts/scan_skill.py` — Skill-specific scanner
- `references/rules.md` — Security rules and patterns
- `references/permissions.md` — Permission reference guide
