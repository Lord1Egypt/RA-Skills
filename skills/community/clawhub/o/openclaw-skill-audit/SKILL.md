---
name: skill-audit
description: "Security scanner for OpenClaw skills. Analyzes skill folders and .skill files for: prompt injection, data exfiltration, malicious scripts, suspicious network connections, dangerous code patterns, and unauthorized access. Use when: (1) BEFORE installing any skill from ClawHub or the internet — always scan first, (2) auditing an already-installed skill, (3) reviewing a skill's security posture, (4) checking what APIs/MCPs/env vars a skill uses, or (5) the user asks 'is this skill safe?'. IMPORTANT: This skill acts as a pre-install security hook. When the clawhub skill is used to install a new skill, ALWAYS run skill-audit on the installed skill BEFORE confirming success to the user."
---

# Skill Audit — Security Scanner for OpenClaw Skills

Pre-install security hook. Scan skills before trusting them.

## Pre-Install Hook Workflow (MANDATORY)

When any new skill is installed via `clawhub install`, follow this workflow:

1. Let `clawhub install <slug>` run (it downloads to `skills/` or `~/.openclaw/skills/`)
2. **Immediately** scan the installed skill:
   ```bash
   python3 {baseDir}/scripts/scan_skill.py <path-to-installed-skill> --json
   ```
3. Read the JSON output and check `overall_risk`
4. Report to the user based on risk:

   - 🟢 **Low**: "🛡 Skill `<name>` gescannt: **sicher**. Keine verdaechtigen Patterns gefunden."
   - 🟡 **Medium**: "🛡 Skill `<name>`: **pruefenswert**. [N] Findings (z.B. liest API Keys, macht HTTP Requests). Details: [kurze Liste]. Willst du ihn trotzdem aktivieren?"
   - 🔴 **High**: "⚠️ Skill `<name>`: **riskant**! [Findings auflisten]. Empfehlung: Nur in Sandbox ausfuehren. Behalten oder loeschen?"
   - ⛔ **Critical**: "🚨 Skill `<name>`: **GEFAEHRLICH**! [Top-Findings]. Empfehlung: Sofort loeschen. Soll ich ihn entfernen?"

5. If critical: offer to delete the skill folder immediately
6. If user confirms deletion: `rm -rf <skill-path>`

## Manual Scan

```bash
python3 {baseDir}/scripts/scan_skill.py <path-to-skill>
```

JSON output:
```bash
python3 {baseDir}/scripts/scan_skill.py <path-to-skill> --json
```

Accepts skill folders (containing `SKILL.md`) and packaged `.skill` files.

## Bulk Scan (all installed skills)

Scan every skill in a directory:
```bash
for d in ~/.openclaw/skills/*/; do
  python3 {baseDir}/scripts/scan_skill.py "$d"
  echo ""
done
```

## What It Detects

1. **Prompt Injection** — hidden instructions, identity overrides, audit evasion, invisible unicode, HTML comments
2. **Data Exfiltration** — base64+POST, reverse shells, data capture services (webhook.site, requestbin)
3. **Dangerous Code** — eval/exec, dynamic imports, unsafe deserialization, subprocess, raw sockets
4. **File System Abuse** — path traversal, SSH key access, system files, OpenClaw config
5. **Network Connections** — URL extraction + classification, hardcoded IPs, known API endpoints
6. **Secret Access** — env var reads, API key references, credential patterns
7. **Permission Scope** — required binaries, env vars, network-capable tools

## Risk Levels

- 🟢 **Low** — no concern
- 🟡 **Medium** — review, could be legitimate
- 🔴 **High** — likely dangerous, review carefully
- ⛔ **Critical** — almost certainly malicious

## Limitations

Static analysis catches patterns, not intent. Cannot detect:
- Logic-level attacks (subtly biased outputs)
- Obfuscated code beyond known patterns
- Runtime-only behavior (code fetched from URL then executed)

Combine with manual review for high-stakes deployments.

## Source Code

GitHub: https://github.com/ProduktEntdecker/skill-audit
