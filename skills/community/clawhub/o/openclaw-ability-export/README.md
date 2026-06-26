# openclaw-ability-export

Export and import your OpenClaw agent configuration as a shareable Markdown bundle — directly in chat.

<p align="left">
  <a href="README_zh.md">中文</a>
</p>

---

## Features

- **Export** — Scan five core config files and generate a Markdown ability package, sent directly in chat
- **Import** — Parse incoming ability packages, preview contents, let users choose what to import
- **Selective Import** — Import only specific files, not everything
- **Security Reminders** — Warn before exporting MEMORY.md, show preview before importing

## Trigger Words

| Action | Keywords |
|--------|----------|
| Export | `export ability`, `导出能力包`, `打包我的能力` |
| Import | `import ability`, `导入能力包`, `学习能力包` |

## Exported Files

| File | Description |
|------|-------------|
| `AGENTS.md` | Agent workspace rules and conventions |
| `SOUL.md` | Agent personality and behavior guidelines |
| `TOOLS.md` | Local tools configuration and notes |
| `IDENTITY.md` | Agent identity |
| `MEMORY.md` | Long-term memory and preferences |

## Quick Start

**Export:**
```
User: export ability
Agent: → Scans config files → Generates Markdown bundle → Sends in chat
```

**Import:**
```
User: [Paste ability package content]
Agent: Shows preview of all files → User selects what to import → Writes selected files
```

## Install

```bash
npx skills add openclaw-ability-export
```

Or browse on [ClawhHub](https://clawhub.com/skills/openclaw-ability-export).
