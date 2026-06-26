---
name: mcpsec
description: "Scan MCP server configuration files for security vulnerabilities using mcpsec (OWASP MCP Top 10). Use when: auditing MCP tool configs for prompt injection, hardcoded secrets, missing auth, insecure transport, or excessive permissions. Auto-discovers config files for Claude Desktop, Cursor, VS Code, and custom paths. Reports findings by severity. Read-only — never modifies any config."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["mcpsec"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "shell",
              "label": "Install mcpsec (Homebrew, macOS)",
              "cmd": "brew install pfrederiksen/tap/mcpsec",
            },
            {
              "id": "binary",
              "kind": "shell",
              "label": "Install mcpsec (pre-built binary, Linux/macOS) — verify checksum before running",
              "cmd": "curl -L https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/checksums.txt && curl -L https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/mcpsec_1.0.0_linux_amd64.tar.gz -o /tmp/mcpsec.tar.gz && sha256sum /tmp/mcpsec.tar.gz && tar -xzf /tmp/mcpsec.tar.gz -C /tmp/ && mv /tmp/mcpsec /usr/local/bin/mcpsec",
            },
          ],
      },
  }
---

# MCPSec

Security scanner for Model Context Protocol (MCP) server configurations. Covers all 10 OWASP MCP Top 10 risk categories via [pfrederiksen/mcpsec](https://github.com/pfrederiksen/mcpsec) — an Apache 2.0 open-source Go binary.

## ⚠️ Trust Model & Security Considerations

This skill scans MCP config files that may contain API keys and tokens. Read this before installing.

### Supply chain
The `mcpsec` binary is an external artifact from GitHub. Mitigate supply chain risk by verifying the SHA256 before running — do not skip this step.

**Pinned checksums for v1.0.0:**
```
e367cce46b1a152ccc8aedf2eeca5c6bcf5523b379a00a3f3704d61bf2b4fbca  linux_amd64
98e6ccf883b3a40cea817e19cecd5dc66ae1816bdaf0a58f7fcd8a46576321b0  linux_arm64
5ab2db3cc517f67600ace32f6dfacb15b2ce0b77319797a0431b105466379f3b  darwin_amd64
a9ea3b8d753f0332ddc7720a9778f870f42f523b589d12d8eed5030befa52ee9  darwin_arm64
```

For stronger guarantees, build from source: `git clone https://github.com/pfrederiksen/mcpsec && cd mcpsec && make build`

### Sensitive data access
MCP config files may contain API keys and tokens. The scanner reads them to detect hardcoded secrets (MCP04) but does not write, transmit, or log them. The wrapper script (`scan.py`) makes no network calls. The binary makes no network calls per its source, but this skill cannot enforce the binary's runtime behavior — review the source or run in an isolated environment if you require certainty.

### Network behavior
- **Wrapper script:** no network calls
- **mcpsec binary:** no network calls per source; cannot be verified at runtime by this skill

### Isolation
For high-security environments, run in a container or VM, or audit the mcpsec binary source before use.

## Usage

```bash
# Auto-discover and scan all known MCP config locations
python3 scripts/scan.py

# Scan a specific config file
python3 scripts/scan.py ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Only show critical and high findings
python3 scripts/scan.py --severity critical,high

# JSON output (for dashboards/SIEM)
python3 scripts/scan.py --format json

# Quiet mode: only output if findings exist (good for cron)
python3 scripts/scan.py --quiet
```

## Installing mcpsec

```bash
# macOS (Homebrew — tap is maintained by pfrederiksen)
brew install pfrederiksen/tap/mcpsec

# Linux amd64 — verify SHA256 BEFORE extracting
curl -L https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/mcpsec_1.0.0_linux_amd64.tar.gz -o mcpsec.tar.gz
echo "e367cce46b1a152ccc8aedf2eeca5c6bcf5523b379a00a3f3704d61bf2b4fbca  mcpsec.tar.gz" | sha256sum -c -
# Only proceed if the above prints "mcpsec.tar.gz: OK"
tar -xzf mcpsec.tar.gz && mv mcpsec /usr/local/bin/mcpsec && chmod +x /usr/local/bin/mcpsec

# Build from source (strongest supply chain guarantee)
git clone https://github.com/pfrederiksen/mcpsec && cd mcpsec && make build
sudo mv mcpsec /usr/local/bin/
```

## What It Scans

Auto-discovers configs at these paths:
- `~/Library/Application Support/Claude/claude_desktop_config.json` (Claude Desktop)
- `~/Library/Application Support/Claude/Claude Extensions/` (DXT extensions)
- `~/.cursor/mcp.json` (Cursor)
- `~/.vscode/mcp.json` (VS Code)
- `~/.openclaw/workspace/mcp-config.json` (custom)

## OWASP MCP Top 10 Coverage

| ID | Risk | Severity |
|---|---|---|
| MCP01 | Prompt injection in tool descriptions | High |
| MCP02 | Excessive tool permissions | Critical/High |
| MCP03 | Missing authentication | Critical/High |
| MCP04 | Hardcoded secrets in env vars | Critical |
| MCP05 | Unsafe resource URIs (SSRF) | High |
| MCP06 | Tool definition spoofing | High/Medium |
| MCP07 | Insecure transport (HTTP, weak TLS) | Critical/High |
| MCP08 | Missing input validation schemas | Medium |
| MCP09 | Missing logging/audit config | Medium/High |
| MCP10 | No rate limiting | Medium |

## Security Design (wrapper script)

- `subprocess` used exclusively with `shell=False`
- All file paths validated against an allowlist pattern before use
- All exceptions caught by specific type — no bare `except`
- Full type hints and docstrings throughout
- Read-only — no config files are modified

## System Access

- **Reads:** MCP config JSON files at known paths (or paths you specify)
- **Executes:** `mcpsec scan` binary — reads local config files only; no network calls per upstream source, but this cannot be enforced by the wrapper
- **No writes, no network calls from the wrapper script**
- **Sensitive data note:** config files may contain API keys or tokens; mcpsec reads them to detect hardcoded secrets but does not transmit them

## Requirements

- Python 3.10+
- `mcpsec` binary on PATH — see install instructions above
