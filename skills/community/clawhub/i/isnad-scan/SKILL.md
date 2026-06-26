---
name: isnad-scan
description: Scan AI agent skills for security vulnerabilities — detects code injection, prompt injection, credential exfiltration, supply chain attacks, and 69+ threat patterns. Use when installing new skills, auditing existing ones, reviewing untrusted code, or validating packages before publishing.
metadata:
  openclaw:
    emoji: "🛡️"
    requires:
      bins: ["isnad-scan"]
    primaryEnv: null
    install:
      - id: isnad-scan-pip
        kind: pipx
        package: isnad-scan
        bins: ["isnad-scan"]
        label: "Install isnad-scan (pipx)"
---

# isnad-scan — Security Scanner for AI Agent Skills

Scan any skill, package, or directory for security threats before installing or running it.

## Quick Scan

```bash
isnad-scan <path>
```

Scans a directory and reports findings by severity (CRITICAL, HIGH, MEDIUM, LOW).

## Options

```bash
isnad-scan <path> --cve          # Also check dependencies for known CVEs (via OSV.dev)
isnad-scan <path> -v             # Verbose output (show matched lines)
isnad-scan <path> --json         # Machine-readable JSON output
isnad-scan <path> --cve -v       # Full audit: CVEs + verbose findings
```

## What It Detects (69+ patterns)

**Code Injection** — shell execution, eval, exec, subprocess, os.system, dynamic imports
**Prompt Injection** — role override attempts, instruction hijacking, jailbreak patterns
**Credential Exfiltration** — env var harvesting, keychain access, token theft, file reads of sensitive paths
**Network Threats** — reverse shells, DNS exfiltration, unauthorized outbound connections, webhook data leaks
**Filesystem Attacks** — path traversal, symlink attacks, /etc/passwd reads, SSH key access
**Supply Chain** — typosquatting detection, minified JS analysis, binary file scanning, hidden files
**Crypto Risks** — weak algorithms, hardcoded keys, wallet seed extraction

## When to Use

1. **Before installing a new skill** — scan the skill directory first
2. **Auditing existing skills** — periodic security review
3. **Reviewing PRs/contributions** — catch malicious code in submissions
4. **Pre-publish validation** — ensure your own skills are clean before sharing
5. **CI/CD integration** — `isnad-scan . --json` for automated checks

## Interpreting Results

```
🔴 CRITICAL  — Immediate threat. Do not install/run.
🟠 HIGH      — Likely malicious or dangerous. Review carefully.
🟡 MEDIUM    — Suspicious pattern. May be legitimate, verify intent.
🔵 LOW       — Informational. Common in legitimate code but worth noting.
```

## Examples

Scan a ClawHub skill before installing:
```bash
isnad-scan ./skills/some-new-skill/
```

Full audit with CVE checking:
```bash
isnad-scan ./skills/some-new-skill/ --cve -v
```

JSON output for automation:
```bash
isnad-scan . --json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"summary\"][\"critical\"]} critical, {d[\"summary\"][\"high\"]} high')"
```

## Python API

```python
from isnad_scan import scan_directory

results = scan_directory("/path/to/skill")
for finding in results.findings:
    print(f"[{finding.severity}] {finding.category}: {finding.description}")
    print(f"  File: {finding.file}:{finding.line}")
```

## About ISNAD

ISNAD (إسناد) means "chain of transmission" — a method for verifying the authenticity of transmitted knowledge. isnad-scan is the security layer of the [ISNAD Protocol](https://isnad.md), bringing trust verification to the AI agent skill ecosystem.

**PyPI:** `pip install isnad-scan`
**GitHub:** [counterspec/isnad](https://github.com/counterspec/isnad)
**Protocol:** [isnad.md](https://isnad.md)
