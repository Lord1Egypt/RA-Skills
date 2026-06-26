# 🔗 Logseq Bridge

**Pure file-based interaction with your Logseq graph.**

Read, write, search, and manage Logseq journals and pages from any external agent, script, or CLI — without installing any Logseq plugins or HTTP APIs.

## ✨ Features

- **📝 Write** to daily journals and pages via direct `.md` file append
- **📖 Read** any journal entry or knowledge page
- **🔍 Search** across all notes with `grep` or database `strings`
- **📋 Create** new pages with properties
- **🔄 No plugins, no HTTP APIs** — works directly with `.md` files on the filesystem

## Quick Start

```bash
# 1. Find your Logseq graph directory
# Open Logseq → Settings → Advanced → "Current graph directory"

# 2. Try it
DATE=$(date +%Y_%m_%d)
echo "- ✅ Logseq Bridge works!" >> "/path/to/your/graph/journals/$DATE.md"

# 3. Reload in Logseq (Ctrl/Cmd+Shift+R) to see the new entry
```

## 📖 Full Documentation

See [`SKILL.md`](SKILL.md) for complete API reference, operation templates, and troubleshooting.

## 📦 Install from ClawHub

```bash
clawhub install logseq-bridge
```

## 🔗 Links

- [Logseq](https://logseq.com/)
- [ClawHub](https://clawhub.ai)
