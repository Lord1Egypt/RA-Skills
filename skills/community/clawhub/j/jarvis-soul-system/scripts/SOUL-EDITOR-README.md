# SOUL Editor - Agent Personality Designer

## Overview
A visual web-based editor for managing SOUL.md personality files in multi-agent systems using the OpenClaw agent-soul-system framework.

## Features
- Visual editing of agent SOUL.md files
- Real-time markdown preview
- Save directly to agent directories via REST API
- Personality selection from pre-built library (8 personalities)
- Agent switching with unsaved changes protection

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  soul-editor.html (Browser)                             │
│  - User interface                                       │
│  - Form inputs + live preview                           │
│  - REST API client                                      │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP :3001
┌─────────────────────▼───────────────────────────────────┐
│  soul-server.js (Node.js)                               │
│  - REST API server                                      │
│  - File system access                                   │
│  - Serves static HTML                                   │
└─────────────────────┬───────────────────────────────────┘
                      │ Local filesystem
┌─────────────────────▼───────────────────────────────────┐
│  C:\Users\Administrator\.openclaw\agents\               │
│  ├── main/SOUL.md                                       │
│  ├── cdo/SOUL.md                                        │
│  ├── cto/SOUL.md                                        │
│  └── cco/SOUL.md                                        │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Option 1: Using the batch file (recommended for Windows)
1. Double-click `soul-server.bat`
2. Open in browser: `file:///C:/Users/Administrator/.openclaw/canvas/soul-editor.html`

### Option 2: Manual
```bash
cd C:\Users\Administrator\.openclaw\workspace\skills\agent-soul-system\scripts
node soul-server.js 3001
# In browser:
file:///C:/Users/Administrator/.openclaw/canvas/soul-editor.html
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/agents` | List all agents with personality info |
| GET | `/api/agents/:name` | Get single agent's SOUL.md content |
| POST | `/api/agents/:name` | Save SOUL.md content (body: `{content: "..."}`) |

## personalities

| Name | Traits |
|------|--------|
| 福尔摩斯 | 观察入微、逻辑推理 |
| 张良 | 运筹帷幄、洞察先机 |
| 马斯克 | 第一性原理、快速迭代 |
| 乔布斯 | 极致产品、用户体验 |
| 诸葛亮 | 深谋远虑、宁静致远 |
| 毛泽东 | 实事求是、集中兵力 |
| 查理·芒格 | 多元思维、逆向思考 |
| 德鲁克 | 目标管理、效能优先 |

## Auto-Start Setup

The server is configured to start automatically on Windows login via Registry Run key.

**Status:** ✅ Registered
**Registry:** `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` → `SOULServer`
**Launcher:** `soul-server-launcher.vbs` (runs hidden, no console window)

To remove auto-start:
```powershell
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "SOULServer"
```

## Files

| File | Purpose |
|------|---------|
| `soul-server.js` | Node.js HTTP server with REST API |
| `soul-server.bat` | Windows launcher script (console) |
| `soul-server-launcher.vbs` | Windows launcher (hidden, for auto-start) |
| `soul-editor.html` | Visual web editor (served from canvas/) |
| `soul-check.py` | Validate all agents have SOUL.md |
| `soul-create.py` | Interactive SOUL.md creation script |
| `soul-ls.py` | List agents with personality info |
| `SOUL-EDITOR-README.md` | This documentation |

## Status

- ✅ Server running at localhost:3001
- ✅ Editor accessible via file:// URL
- ✅ 4 agents configured (main, cdo, cto, cco)
- ⏳ ClawHub publishing pending (requires login)

## License

Part of agent-soul-system (MIT-0 License)
Owner: adamwgp | Published: 2026-05-11