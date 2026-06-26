# MCPSec Skill

[![ClawHub](https://img.shields.io/badge/ClawHub-mcpsec--skill-blue)](https://clawhub.ai/pfrederiksen/mcpsec-skill)
[![Version](https://img.shields.io/badge/version-1.0.3-green)]()

An [OpenClaw](https://openclaw.ai) skill that wraps [pfrederiksen/mcpsec](https://github.com/pfrederiksen/mcpsec) to periodically audit MCP server configurations against the OWASP MCP Top 10.

## ⚠️ Before Installing

This skill depends on an external binary (`mcpsec`). Before using:

1. **Verify provenance** — review the source at <https://github.com/pfrederiksen/mcpsec> and verify the binary checksum matches the published `checksums.txt` before running.
2. **Network behavior** — the wrapper script makes no network calls. The `mcpsec` binary reads local config files only per its source, but this cannot be enforced by the wrapper. Review the source if you need certainty.
3. **What it reads** — MCP config JSON files on your system (Claude Desktop, Cursor, VS Code). It does not transmit them.
4. **Isolation** — for stronger guarantees, run in a container or audit the mcpsec source/build first.

## Features

- 🔍 **Auto-discovery** — finds Claude Desktop, Cursor, VS Code, and custom MCP configs automatically
- 🔴🟠🟡🟢 **Severity classification** — critical / high / medium / low findings
- 📋 **OWASP MCP Top 10** — all 10 risk categories covered
- 🤫 **Quiet mode** — `--quiet` for cron use: silent when nothing found
- 📄 **JSON output** — `--format json` for SIEM/dashboard integration
- 🔒 **Read-only wrapper** — never modifies any config file

## Installing mcpsec

```bash
# macOS (Homebrew)
brew install pfrederiksen/tap/mcpsec

# Linux — pre-built binary (verify checksum first)
curl -L https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/checksums.txt
curl -L https://github.com/pfrederiksen/mcpsec/releases/download/v1.0.0/mcpsec_1.0.0_linux_amd64.tar.gz -o mcpsec.tar.gz
sha256sum mcpsec.tar.gz  # verify against checksums.txt
tar -xzf mcpsec.tar.gz && mv mcpsec /usr/local/bin/
```

## Usage

```bash
# Auto-scan all known MCP config locations
python3 scripts/scan.py

# Specific file
python3 scripts/scan.py ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Quiet mode (ideal for cron — silent if clean)
python3 scripts/scan.py --quiet

# JSON output
python3 scripts/scan.py --format json
```

## Requirements

- Python 3.10+
- `mcpsec` binary on PATH (see above)

## License

Apache 2.0

## Links

- [mcpsec scanner](https://github.com/pfrederiksen/mcpsec)
- [ClawHub](https://clawhub.ai/pfrederiksen/mcpsec-skill)
- [OpenClaw](https://openclaw.ai)
