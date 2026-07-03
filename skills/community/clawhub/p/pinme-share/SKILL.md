---
name: pinme-share
description: >
  Upload any local file or directory to PinMe (pinme.eth.limo) and instantly get a short shareable URL
  (*.pinit.eth.limo). Supports all file types: HTML pages, PDFs, images, audio, video, documents, or
  entire directories. PinMe uses public IPFS — uploaded content is publicly accessible; do NOT upload
  internal / private / credential data. AppKey persists to ~/.local/share/pinme-share/appkey.json
  (XDG-compliant), overridable via PINME_APPKEY env or --set-appkey CLI. Use when the user says
  "upload this file", "share this HTML", "host this page", "give me a public link", "deploy to pinme",
  "upload to IPFS", "get a shareable link", "show my upload history", or hands over any file / directory
  and wants a URL to share.
---

# pinme-share

Upload any file or directory to [PinMe](https://pinme.eth.limo) (public IPFS) and get back a short
`*.pinit.eth.limo` URL.

- **Version**: 1.0.0
- **License**: MIT
- **Author**: Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)
- **Repository**: https://github.com/Songhonglei/html-tool-suite

---

## ⚠️ Public-data warning — read before first use

- **PinMe runs on public IPFS**: anything you upload is world-readable; anyone with the URL can open it.
- **CIDs are effectively undeletable**: IPFS nodes cache content; `--rm` only removes the pin from your
  account — third-party copies may still exist.
- **🚫 Never upload**: internal company docs / client data / credentials / private info / unreleased material.
- Every `upload` invocation prints a warning to stderr; pass `--yes` to skip it in automation.

---

## 🔑 First-time setup — configure your AppKey

PinMe v2.x requires authentication. The lookup order is:

1. **`PINME_APPKEY` env variable** (highest priority, doesn't persist — good for CI / one-shot)
2. **`pinme` CLI already has an AppKey set** → reuse directly
3. **Local file** `~/.local/share/pinme-share/appkey.json` exists → auto-applied to `pinme` CLI
4. **Otherwise** → script returns `error_type: auth_required` and tells the user to grab an AppKey from
   https://pinme.eth.limo

### Configure / replace the AppKey (persistent)

```bash
python3 scripts/upload_to_pinme.py --set-appkey <YOUR_KEY>
```

Writes the key to both the `pinme` CLI and `~/.local/share/pinme-share/appkey.json` (mode 0600).
The local file is **never** committed to git or shipped in the published skill bundle.

### Override the storage path (advanced)

```bash
export PINME_APPKEY_FILE=/custom/path/appkey.json
# or honour $XDG_DATA_HOME automatically:
export XDG_DATA_HOME=$HOME/my-xdg-data   # → $HOME/my-xdg-data/pinme-share/appkey.json
```

### Inspect current configuration

```bash
python3 scripts/upload_to_pinme.py --show-appkey
```

---

## 📤 Upload

```bash
# Any single file
python3 scripts/upload_to_pinme.py /path/to/file.html
python3 scripts/upload_to_pinme.py /path/to/report.pdf

# A whole directory (no index.html required)
python3 scripts/upload_to_pinme.py /path/to/dist/

# Add --verbose to see progress for large files
python3 scripts/upload_to_pinme.py /path/to/video.mp4 --verbose

# Skip the privacy warning (for cron / automated pipelines)
python3 scripts/upload_to_pinme.py /path/to/file.html --yes

# Custom timeout (default: 60s + 2s/MB, floor 180s, ceiling 1800s)
python3 scripts/upload_to_pinme.py /path/to/big.zip --timeout 900
```

Output — the last line of stdout is always a single JSON object:

```json
{"success": true, "url": "https://xxxx.pinit.eth.limo", "size_bytes": 12345, "timeout_used": 180}
```

---

## 📜 Browse upload history

```bash
python3 scripts/upload_to_pinme.py --list
python3 scripts/upload_to_pinme.py --list --limit 5
python3 scripts/upload_to_pinme.py --list --raw   # don't parse; return raw CLI text
```

Structured output:

```json
{"success": true, "count": 3, "history": [
  {"name": "foo.html", "cid": "Qm...", "url": "https://xxxx.pinit.eth.limo", "size": "12 KB", "time": "2026-05-21 09:30"}
]}
```

---

## 🗑️ Unpin (remove from your pin list)

```bash
python3 scripts/upload_to_pinme.py --rm <CID>
```

> ⚠️ Public IPFS copies cannot be truly deleted; this only removes the pin from your account.

---

## 💰 Wallet / quota

```bash
python3 scripts/upload_to_pinme.py --wallet
```

PinMe provides a free quota (~500 uploads). Past that it may charge — see https://pinme.eth.limo console.

---

## 🚪 Logout

```bash
python3 scripts/upload_to_pinme.py --logout
```

Clears both the `pinme` CLI session and `~/.local/share/pinme-share/appkey.json`.

---

## 🧰 stdout / stderr contract

| Stream | Purpose |
|---|---|
| **stdout** | **Always exactly one JSON object on the final line** — safe to pipe into `jq` |
| **stderr** | Progress lines, privacy warnings, debug output — never breaks JSON parsing |

Example:

```bash
URL=$(python3 scripts/upload_to_pinme.py /tmp/foo.html | jq -r '.url')
```

---

## 📋 Error code reference (for agent routing)

| `error_type` | Trigger | Suggested handling |
|---|---|---|
| `auth_required` | AppKey missing / pinme reports login failure | Prompt user to run `--set-appkey` or grab an AppKey |
| `invalid_path` | Path missing / unreadable | Ask user to confirm the path |
| `oversize` | Single file > 200 MB or directory > 1 GB | Split or use different storage |
| `cli_missing` | `pinme` CLI install failed / not found | Check Node.js / network / npm permissions |
| `network` | Timeout / DNS failure / connection refused / 5xx | Retry or verify outbound connectivity |
| `quota_exceeded` | PinMe quota / wallet empty | Top up via PinMe console or switch account |
| `url_not_found` | Upload OK but no parseable URL | Inspect raw output (CLI format may have changed) |
| `usage` | No operation specified | Show `--help` and ask the user what they want to do |
| `invalid_appkey` | AppKey passed to `--set-appkey` looks malformed (length < 20) | Ask user to recheck and re-enter |
| `unknown` | Fallback | `error` field includes raw stderr |

Exit codes: `0` success / `1` generic failure / `2` structured failure (read JSON `error_type`).

---

## 📦 Constraints & dependencies

- Single file ≤ 200 MB, directory ≤ 1 GB (PinMe server limit)
- Static files only (no server-side processing)
- Node.js ≥ 16.13.0 (auto-checked)
- `pinme` CLI (auto-installed via `npm install -g pinme` if missing)
- PinMe AppKey (required)

---

## 🛠️ Pasted-content workflow

If the user pastes HTML content directly into chat, the agent should:

1. Write it to `/tmp/pinme_user_<timestamp>.html`
2. Invoke this script with that path
3. Return the resulting URL

---

## 🔧 Environment variables

| Variable | Purpose | Example |
|---|---|---|
| `PINME_APPKEY` | One-shot / CI override (highest priority, no persist) | `export PINME_APPKEY=abc123...` |
| `PINME_APPKEY_FILE` | Override AppKey storage path | `export PINME_APPKEY_FILE=$HOME/.config/pinme/key.json` |
| `XDG_DATA_HOME` | Honoured for default storage path | `export XDG_DATA_HOME=$HOME/my-xdg-data` |

Default storage: `${XDG_DATA_HOME:-$HOME/.local/share}/pinme-share/appkey.json`.

---

## 🪪 Acknowledgements

- [PinMe](https://pinme.eth.limo) for the IPFS pinning service and `pinme` CLI
- Part of the [html-tool-suite](https://github.com/Songhonglei/html-tool-suite) — HTML generation,
  publishing, and sharing skills
