# pinme-share

> Upload any file or directory to **PinMe** (public IPFS) and instantly get back a short shareable
> URL like `https://xxxx.pinit.eth.limo`.

Part of the [**html-tool-suite**](https://github.com/Songhonglei/html-tool-suite) — a collection
of HTML generation, publishing, and sharing skills for AI agents.

## Features

- 📤 **Upload anything**: HTML pages, PDFs, images, audio, video, documents, or whole directories
- 🔗 **Short URLs out of the box**: prefers `*.pinit.eth.limo` ENS short links over raw CID previews
- 🧾 **Structured JSON output**: the last line of stdout is always one parseable JSON object
- 🔑 **Sensible auth**: AppKey persists to XDG-standard `~/.local/share/pinme-share/` with `0600`
  perms; overridable via `PINME_APPKEY` env or custom path
- 🛡️ **Privacy-first**: prints loud warnings before every upload — public IPFS is forever
- ⚙️ **Smart timeouts**: auto-scales by file size (60s + 2s/MB, capped 180–1800s)
- 📋 **8-class error taxonomy**: `auth_required` / `invalid_path` / `oversize` / `cli_missing` /
  `network` / `quota_exceeded` / `url_not_found` / `unknown` for clean agent routing
- 📜 **History + unpin + wallet**: full management surface beyond just uploading

## Quick Start

```bash
# 1. Get an AppKey from https://pinme.eth.limo
# 2. Configure it (one-time)
python3 scripts/upload_to_pinme.py --set-appkey <YOUR_KEY>

# 3. Upload anything
python3 scripts/upload_to_pinme.py /path/to/file.html
python3 scripts/upload_to_pinme.py /path/to/dist/
```

Output:

```json
{"success": true, "url": "https://xxxx.pinit.eth.limo", "size_bytes": 12345, "timeout_used": 180}
```

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install pinme-share` |
| Claude Code | Copy this directory to `~/.claude/skills/pinme-share/` |
| Cursor | Copy this directory to `.cursor/skills/pinme-share/` |
| Other | Drop the folder into your agent's skill directory; everything is self-contained |

Or clone the whole suite:

```bash
git clone https://github.com/Songhonglei/html-tool-suite.git
# Skills live under html-tool-suite/skills/
```

## ⚠️ Public-data warning

PinMe = public IPFS. Anything you upload is **world-readable** and **practically undeletable**
(third-party IPFS nodes cache content). **Never upload** internal docs, client data, credentials,
private info, or unreleased material. The script prints a stderr warning on every upload; pass
`--yes` to silence it in automation.

## Configuration

| Env var | Purpose |
|---|---|
| `PINME_APPKEY` | One-shot / CI override (highest priority, doesn't persist) |
| `PINME_APPKEY_FILE` | Override AppKey storage path |
| `XDG_DATA_HOME` | Honoured for default path: `$XDG_DATA_HOME/pinme-share/appkey.json` |

Default storage: `~/.local/share/pinme-share/appkey.json` (mode `0600`).

## Requirements

- Node.js ≥ 16.13.0
- `pinme` CLI (auto-installed via `npm install -g pinme` if missing)
- A PinMe AppKey (free at https://pinme.eth.limo)

## Usage

Full details — every flag, every error class, the stdout/stderr contract, and how to use this
from inside an agent — see [SKILL.md](./SKILL.md).

## License

[MIT](./LICENSE) © 2026 Evan Song

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Acknowledgements

- [PinMe](https://pinme.eth.limo) for the IPFS pinning service and `pinme` CLI

## Changelog

### v1.0.0 (2026-06-22)

- Initial public release (forked from internal v2.0.0)
- XDG-compliant AppKey storage (`~/.local/share/pinme-share/`)
- `PINME_APPKEY` / `PINME_APPKEY_FILE` env overrides
- Added `usage` error type for "no operation specified"
- Full English documentation
