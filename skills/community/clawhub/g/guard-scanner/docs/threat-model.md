# Guard-Scanner Threat Model

## Scope

Guard-scanner protects against threats targeting **AI agent skills and MCP-connected workflows**. It does **not** replace traditional application security tools (SAST, DAST, container scanners).

## What guard-scanner defends against

### Static Analysis (352 patterns, 32 categories)

| Threat Class | Examples | Detection Method |
|-------------|----------|-----------------|
| Prompt Injection | "ignore all previous instructions", role override | Regex pattern matching on doc/code files |
| Identity Hijack | SOUL.md overwrite, memory poisoning | File operation pattern + soul-lock patterns |
| Supply Chain | curl\|bash, npm postinstall abuse, typosquatting | Command pattern matching + IoC check |
| Data Exfiltration | env/credential harvesting, network exfil | Data flow + network pattern detection |
| Remote Code Execution | eval(), exec(), reverse shells | Dangerous function + shell pattern matching |
| PII Exposure | SSN/credit card collection, PII logging | PII regex patterns + context analysis |
| Social Engineering | Trust exploitation, authority claims | Social engineering phrase detection |
| Tool Shadowing | MCP tool descriptions with hidden instructions | MCP-specific pattern matching |
| Context Crush | Prompt overstuffing / context window manipulation | Token density heuristics |

### Runtime Guard (26 checks, 5 layers)

| Layer | Name | Function |
|-------|------|----------|
| L1 | Command Safety | Block reverse shells, curl\|bash, SSRF, cred exfil |
| L2 | Identity Protection | Block SOUL.md/memory tampering |
| L3 | Prompt Safety | Detect injection/override in tool args |
| L4 | Behavioral Safety | Detect no-research execution |
| L5 | Trust Safety | Detect authority claims, creator bypass, fake audits |

## What guard-scanner does NOT defend against

| Limitation | Explanation |
|-----------|-------------|
| Obfuscated code | Regex-only — no deobfuscation. Base64/encoded payloads may evade. |
| AST-level taint analysis | No data flow tracking across functions/files (planned P2). |
| Sandbox escape | Does not provide sandboxing — complementary to container isolation. |
| Zero-day attack patterns | Detects known patterns only — new techniques require pattern updates. |
| Code within markdown blocks | Doc files scanned for prompt patterns; JS in code blocks partially covered. |
| Pipe-to-curl variants | `env \| curl` not yet caught by runtime guard (tracked for improvement). |

## Threat Categories (OWASP Agentic Security Mapping)

| OWASP ID | Name | guard-scanner Coverage |
|----------|------|----------------------|
| ASI01 | Agent Goal Hijack | ✅ prompt-injection, context-crush patterns |
| ASI02 | Tool Misuse | ✅ tool-shadowing, MCP poisoning patterns |
| ASI03 | Identity Abuse | ✅ soul-lock patterns, SOUL.md protection |
| ASI04 | Supply Chain | ✅ curl\|bash, typosquatting, IoC database |
| ASI05 | RCE | ✅ eval/exec detection, shell patterns |
| ASI06 | Memory Poisoning | ✅ memory write detection |
| ASI07 | Inter-Agent | ✅ A2A smuggle, SSRF patterns |
| ASI09 | Human-Trust | ✅ social engineering, authority claims |
| ASI10 | Rogue Agent | ✅ persistence, identity hijack |

## CVE Coverage

| CVE | Product | Detection |
|-----|---------|-----------|
| CVE-2026-25905 | mcp-run-python (Pyodide) | ✅ Sandbox escape pattern |
| CVE-2026-27825 | mcp-atlassian | ✅ Path traversal pattern |
| CVE-2026-2256 | MS-Agent (CERT VU#431821) | ✅ Denylist bypass pattern |
| CVE-2026-25046 | execSync filename injection | ✅ Unsanitized exec pattern |
