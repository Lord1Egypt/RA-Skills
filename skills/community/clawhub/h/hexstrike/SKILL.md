---
name: hexstrike
description: "Cybersecurity assistant for CTF challenges, penetration testing, network recon, vulnerability assessment, and security research. Use when: (1) solving CTF challenges (web, crypto, pwn, forensics, rev, OSINT, misc), (2) performing network reconnaissance or port scanning, (3) web application security testing, (4) vulnerability scanning and assessment, (5) binary analysis or reverse engineering, (6) password cracking or hash identification, (7) forensics analysis (file, memory, network, steganography), (8) cloud security assessment (AWS, GCP, K8s, containers), (9) OSINT gathering, (10) any offensive security or red team task. Triggers on: CTF, capture the flag, pentest, recon, nmap, exploit, vulnerability, reverse engineering, forensics, steganography, hash crack, brute force, SQL injection, XSS, buffer overflow, ROP, binary exploitation, OSINT, bug bounty, security audit, cloud security."
---

# HexStrike — Cybersecurity & CTF Skill

## Overview

Execute security tools directly via `exec`. No middleware, no MCP server — direct CLI access to 150+ security tools with methodology-driven workflows.

## First Step: Check Available Tools

Before starting any engagement, run the tool checker to see what's installed:

```bash
bash scripts/tool-check.sh           # All categories
bash scripts/tool-check.sh network   # Just network tools
bash scripts/tool-check.sh web       # Just web tools
```

Adapt the workflow to available tools. If a preferred tool is missing, suggest installation or use alternatives.

## CTF Workflow

When given a CTF challenge:

1. **Identify category** from description/files (web, crypto, pwn, forensics, rev, misc, OSINT)
2. **Read** `references/ctf-playbook.md` for the matching category section
3. **Triage** — run quick identification commands before heavy tools
4. **Iterate** — CTF is exploratory; try the obvious first, escalate to specialized tools
5. **Document findings** as you go — note promising leads

### Category Identification Hints

| Indicators | Category |
|-----------|----------|
| URL, web app, login page, cookies | **web** |
| Ciphertext, hash, encoded data, RSA, AES | **crypto** |
| Binary file, ELF, PE, segfault, nc connection | **pwn** |
| Image file, pcap, memory dump, disk image | **forensics** |
| Binary to analyze, "what does this do", crackme | **rev** |
| Username, location, social media, domain | **OSINT** |
| Encoding, QR code, audio file, esoteric | **misc** |

## Recon / Pentest Workflow

For reconnaissance or penetration testing engagements:

1. **Read** `references/recon-methodology.md` for the full phased approach
2. **Phase 1**: Passive recon (subdomains, DNS, WHOIS, certificate transparency)
3. **Phase 2**: Active recon (port scanning, service enumeration)
4. **Phase 3**: Vulnerability scanning (nuclei, nikto, nmap scripts)
5. **Phase 4**: Web app testing (directory brute-force, injection testing)
6. **Phase 5**: Credential attacks (only when authorized)

## Tool Reference

For quick syntax lookup on any of the 80+ tools, read `references/tool-reference.md`.

## Execution Guidelines

### Output Handling
- Pipe long outputs to files: `nmap ... -oA /tmp/nmap_results`
- Use `| head -50` or `| tail -20` for initial review
- Save important results: `> /tmp/<tool>_<target>_results.txt`

### Safety
- **Never run offensive tools against targets without explicit authorization**
- Default to non-invasive scans first (passive recon, version detection)
- Escalate to active testing only when confirmed authorized
- Use `--batch` flags where available to avoid interactive prompts (e.g., sqlmap)
- Set reasonable timeouts and rate limits to avoid disruption

### Tool Installation
If critical tools are missing, suggest install commands:
- **Debian/Ubuntu**: `sudo apt install <package>`
- **pip tools**: `pip3 install <package>`
- **Go tools**: `go install <repo>@latest`
- **Kali Linux**: Most tools pre-installed; `sudo apt install kali-tools-*` for categories

### Long-Running Scans
Use `exec` with `background: true` and `yieldMs` for scans that take minutes:
```
exec: nmap -sV -sC -p- <TARGET> -oA /tmp/full_scan
background: true, yieldMs: 30000
```
Check progress with `process(action=poll)`.
