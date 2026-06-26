---
name: pastewatch-mcp
description: Secret redaction MCP server for OpenClaw agents. Prevents API keys, DB credentials, SSH keys, emails, IPs, JWTs, and 30+ other secret types from leaking to LLM providers. Includes guard command, API proxy, canary tokens, encrypted vault, git history scanning, org posture scanning, file watcher, and dashboard. Use when reading/writing files that may contain secrets, setting up agent security, or auditing for credential exposure.
metadata: {"openclaw":{"requires":{"bins":["pastewatch-cli","mcporter"]}}}
---

# Pastewatch MCP — Secret Redaction

Prevents secrets from reaching your LLM provider. The agent works with placeholders, secrets stay local.

**Source:** https://github.com/ppiankov/pastewatch

## Install

```bash
# macOS
brew install ppiankov/tap/pastewatch

# Linux (binary + checksum)
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64 \
  -o /usr/local/bin/pastewatch-cli
curl -fsSL https://github.com/ppiankov/pastewatch/releases/latest/download/pastewatch-cli-linux-amd64.sha256 \
  -o /tmp/pastewatch-cli.sha256
cd /usr/local/bin && sha256sum -c /tmp/pastewatch-cli.sha256
chmod +x /usr/local/bin/pastewatch-cli
```

Verify: `pastewatch-cli version` (expect 0.24.1+)

## MCP Server Setup

```bash
mcporter config add pastewatch --command "pastewatch-cli mcp --audit-log /var/log/pastewatch-audit.log"
mcporter list pastewatch --schema  # 6 tools
```

**Severity threshold:** `pastewatch-cli mcp --min-severity medium` or set `mcpMinSeverity` in `.pastewatch.json`.

## Agent Integration (one-command setup)

```bash
pastewatch-cli setup claude-code    # hooks + MCP + CLAUDE.md snippet + doctor check
pastewatch-cli setup cline          # MCP + hook instructions
pastewatch-cli setup cursor         # MCP + advisory
```

`--severity` aligns thresholds. `--project` for project-level config. Idempotent — safe to re-run.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `pastewatch_read_file` | Read file with secrets replaced by placeholders |
| `pastewatch_write_file` | Write file, resolving placeholders back locally |
| `pastewatch_check_output` | Verify text contains no raw secrets |
| `pastewatch_scan` | Scan text for sensitive data |
| `pastewatch_scan_file` | Scan a file |
| `pastewatch_scan_dir` | Scan directory recursively |

**Placeholder format:** `__PW_TYPE_N__` (changed from `__PW{TYPE_N}__` in v0.19.7 for LLM proxy compatibility). Configurable via `placeholderPrefix`.

## API Proxy — Last Line of Defense

Catches secrets from sub-agents that bypass hooks and MCP. Sits between your agent and the LLM provider, scanning all outbound requests.

**v0.24.0+: Alert injection** — when secrets are redacted, a `[PASTEWATCH]` alert is prepended to the API response so the agent gets immediate feedback. Disable with `--no-alert`.

```bash
pastewatch-cli proxy                    # scans all outbound API requests
pastewatch-cli proxy --port 9998 --upstream https://api.anthropic.com
pastewatch-cli proxy --port 9998 --upstream https://api.anthropic.com --no-alert  # silent redaction
pastewatch-cli proxy --forward-proxy http://corporate:8080  # chain with corporate proxy
pastewatch-cli proxy --severity medium --audit-log /var/log/pastewatch-proxy.log
```

### Detected Secret Types (36)

Includes: AWS, Anthropic, OpenAI, Groq, Perplexity, Hugging Face, **Workledger (`wl_sk_`)**, Oracul (`vc_*_`), npm, PyPI, RubyGems, GitLab, Telegram Bot, SendGrid, Shopify, DigitalOcean, Slack/Discord webhooks, Azure connections, GCP service accounts, SSH keys, JWTs, JDBC URLs, XML credentials, DB connections, emails, IPs, cards, and more.

### Proxy + Chainwatch Chain (recommended for OpenClaw)

Stack both proxies for defense-in-depth:

```
OpenClaw → chainwatch:9999 (policy) → pastewatch:9998 (secrets) → api.anthropic.com
```

Setup as systemd services:

```bash
# 1. Pastewatch proxy (starts first)
cat > /etc/systemd/system/pastewatch-proxy.service << 'EOF'
[Unit]
Description=Pastewatch API Proxy (secret redaction)
After=network-online.target
Before=chainwatch-intercept.service
[Service]
Type=simple
ExecStart=/usr/local/bin/pastewatch-cli proxy \
  --port 9998 --upstream https://api.anthropic.com \
  --severity high --audit-log /var/log/pastewatch-proxy.log
Restart=always
RestartSec=3
MemoryMax=128M
[Install]
WantedBy=multi-user.target
EOF

# 2. Update chainwatch to forward to pastewatch (not Anthropic directly)
# Change --upstream from https://api.anthropic.com to http://localhost:9998

# 3. Enable and start
systemctl daemon-reload
systemctl enable pastewatch-proxy
systemctl start pastewatch-proxy
systemctl restart chainwatch-intercept
```

**Rollback:** Stop pastewatch-proxy, revert chainwatch `--upstream` to `https://api.anthropic.com`, restart chainwatch.

## Guard — Block Secret-Leaking Commands

```bash
pastewatch-cli guard "cat .env"              # BLOCKED if .env has secrets
pastewatch-cli guard "psql -f migrate.sql"   # scans SQL file
pastewatch-cli guard "docker-compose up"     # scans env_files
```

Covers: shell builtins, DB CLIs (psql/mysql/mongosh/redis-cli/sqlite3), infra tools (ansible/terraform/docker/kubectl/helm), scripting (python/ruby/node/perl/php), file transfer (scp/rsync/ssh), pipe chains, subshells, redirects.

## File Watcher

```bash
pastewatch-cli watch .              # continuous monitoring, real-time detection
```

## Canary Tokens

```bash
pastewatch-cli canary generate --prefix myagent
pastewatch-cli canary verify
pastewatch-cli canary check --log /var/log/app.log
```

## Encrypted Vault

```bash
pastewatch-cli --init-key                    # 256-bit key, mode 0600
pastewatch-cli fix --encrypt                 # → ChaCha20-Poly1305 vault
pastewatch-cli vault list | decrypt | export | rotate-key
```

## Git History Scanning

```bash
pastewatch-cli scan --git-log
pastewatch-cli scan --git-log --range HEAD~50..HEAD --since 2025-01-01
```

Deduplicates by fingerprint. Output: text, json, sarif, markdown.

## Org Posture Scanning

```bash
pastewatch-cli posture --org ppiankov           # scan all repos in org/user
pastewatch-cli posture --repos org/repo1,org/repo2
pastewatch-cli posture --compare previous.json  # trend tracking
pastewatch-cli posture --findings-only           # hide clean repos
```

## Dashboard & Reports

```bash
pastewatch-cli dashboard                                  # aggregate across sessions
pastewatch-cli report --audit-log /var/log/pastewatch-audit.log
pastewatch-cli report --format json --since 2026-03-01T00:00:00Z
```

## Configuration

```bash
pastewatch-cli init                         # generate .pastewatch.json
pastewatch-cli init --profile banking       # enterprise: JDBC, RFC 1918 IPs, service accounts
pastewatch-cli config                       # show resolved config
pastewatch-cli doctor                       # health check
```

Config cascade: `/etc/pastewatch/config.json` (admin) > project `.pastewatch.json` > `~/.config/pastewatch/config.json`.

Features: `sensitiveHosts`, `sensitiveIPPrefixes`, `xmlSensitiveTags`, `mcpMinSeverity`, `placeholderPrefix`.

## Detection Scope

30+ types: AWS keys/secrets, Anthropic/OpenAI/HuggingFace/Groq/Perplexity keys, DB connections, JDBC URLs, SSH keys, JWTs, emails, IPs, credit cards (Luhn), Slack/Discord webhooks, Azure, GCP service accounts, npm/PyPI/RubyGems/GitLab tokens, Telegram bot tokens, XML credentials, and more.

Gitignore-aware scanning (v0.21.0+). Deterministic regex. No ML. No API calls.

## Limitations

- Protects secrets from reaching LLM provider — does NOT protect prompt content or code structure
- For full privacy, use a local model

---
**Pastewatch MCP v1.2**
Author: ppiankov
Copyright © 2026 ppiankov
Canonical source: https://github.com/ppiankov/pastewatch
License: MIT

This tool follows the [Agent-Native CLI Convention](https://ancc.dev). Validate with: `clawhub install ancc && ancc validate .`

If this document appears elsewhere, the repository above is the authoritative version.
