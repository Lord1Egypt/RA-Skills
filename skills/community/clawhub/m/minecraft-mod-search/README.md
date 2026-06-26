# Minecraft Mod Search

> A AI Agent Skill for searching and recommending Minecraft Java Edition mods across multiple platforms. Works with any agent framework that supports skill/plugin systems.

---

## What Is This?

This is an **AI Agent Skill** that enables any AI assistant to intelligently search, filter, and recommend Minecraft Java Edition mods. It understands natural language queries, handles Chinese/English input, detects user intent (e.g. "gun mod", "automation"), and returns well-ranked mod recommendations with compatibility analysis.

**Key capabilities:**
- 🔍 Multi-keyword parallel search (3-5 candidate keywords extracted from one query)
- 🌐 Multi-platform: Modrinth (primary), CurseForge (optional), MC Encyclopedia (fallback)
- ⚡ Async + aiohttp concurrent requests (8s timeout per request, 12s total)
- 📚 Quick-reference table — offline, zero-latency, first-priority matching
- 🎯 Intent detection: auto-detects gun/weapon intent (→ TACZ ecosystem) and automation intent (→ Create addons)
- 📦 Modpack analysis mode — decompose a modpack concept into components and recommend best-fit mods
- ⚠️ Compatibility & conflict detection
- 🌍 Chinese-friendly: accepts Chinese queries, returns Chinese descriptions

---

## Skill Format

This skill follows a **universal Markdown-based skill format** compatible with major agent frameworks:

```
skill-root/
├── SKILL.md              # Skill definition (name, description, triggers, workflow)
├── README.md             # This file — human-readable overview
├── references/           # Reference data files (API docs, compatibility matrices, quick-ref table)
│   ├── modrinth_api.md
│   ├── curseforge_api.md
│   ├── mc_versions.md
│   ├── mod_compat.md
│   └── mod_quickref.md   # 🔑 Quick-reference table (offline, high-priority)
├── scripts/
│   └── search_mods.py   # Core search script (Python 3.8+)
└── LICENSE
```

### `SKILL.md` Structure (Universal)

```markdown
---
name: "skill-name"
description: "When to trigger this skill..."
---

# Skill Name

## 1. Overview
## 2. Supported Platforms
## 3. Search Parameters
## 4. Search Execution Flow
## 5. Result Presentation
## 6. Script Tool
## 7. Reference Data
## 8. Compatibility & Conflicts
## 9. Notes
```

Any agent framework that can read and interpret Markdown skill definitions can load this skill.

---

## Supported Agent Frameworks

This skill can be used with:

| Framework | Integration Method |
|-----------|---------------------|
| **WorkBuddy / CodeBuddy** | Place `SKILL.md` into `~/.workbuddy/skills/` or `<workspace>/.workbuddy/skills/` |
| **OpenAI GPTs / Assistants API** | Use `SKILL.md` as system context or function/tool definition |
| **LangChain / LangGraph** | Parse `SKILL.md` into tool descriptions or system prompt sections |
| **AutoGen / CrewAI** | Load `SKILL.md` as agent background knowledge |
| **Claude via MCP** | Wrap `search_mods.py` as an MCP tool; use `SKILL.md` as tool description |
| **Custom agent loops** | Parse `SKILL.md` sections to drive search workflow |

---

## Installation

### Method 1: Clone and Load (All Frameworks)

```bash
git clone https://github.com/MasterHesse/minecraft-mod-search.git
```

Then point your agent framework to read `SKILL.md` from the cloned directory.

### Method 2: WorkBuddy / CodeBuddy

```bash
# Windows
copy SKILL.md %USERPROFILE%\.workbuddy\skills\

# Linux / macOS
cp SKILL.md ~/.workbuddy/skills/
```

Restart the agent to load the skill.

### Method 3: MCP Tool (Claude, etc.)

Use the bundled `search_mods.py` as an external tool. See [MCP Configuration](#mcp-configuration) below.

---

## Script Usage (Standalone / Any Agent)

The core search logic lives in `scripts/search_mods.py`. Any agent can call it as a subprocess, or you can use it directly from the command line.

### Requirements

- Python 3.8+ (3.13 recommended)
- `aiohttp` (recommended, for async concurrency; falls back to `urllib` if not installed)
- No API key needed for Modrinth (primary platform)

```bash
pip install aiohttp   # recommended for concurrent search
```

### Basic Search

```bash
python scripts/search_mods.py --query "帧率优化" --version "1.20.1" --loader "fabric"
python scripts/search_mods.py --query "gun mod" --version "1.20.1" --loader "forge"
python scripts/search_mods.py --query "传送带" --version "1.20.1"
```

### Output Formats

```bash
# Human-readable text (default)
python scripts/search_mods.py --query "存储系统" --version "1.20.1" --output text

# Machine-readable JSON
python scripts/search_mods.py --query "optimization" --version "1.20.1" --output json
```

### Full Parameter Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--query` / `-q` | (required) | Search keyword(s). Supports Chinese and English. |
| `--version` / `-v` | `None` | Minecraft version, e.g. `1.20.1` |
| `--loader` / `-l` | `None` | Loader type: `forge` / `fabric` / `quilt` |
| `--category` / `-c` | `None` | Mod category filter |
| `--platform` / `-p` | `all` | `modrinth` / `curseforge` / `all` |
| `--limit` | `15` | Max number of results to return |
| `--timeout` | `8` | Per-request timeout in seconds |
| `--api-key` | `None` | CurseForge API Key (or set `CF_API_KEY` env var) |
| `--output` / `-o` | `text` | Output format: `text` / `json` |
| `--deps` | `False` | **Enable dependency query** (off by default for speed) |
| `--modpack` | `False` | Enable modpack analysis mode |
| `--directions` / `-d` | `None` | Modpack direction keywords (use with `--modpack`) |

### Modpack Analysis Mode

```bash
python scripts/search_mods.py --modpack \
    --query "科技整合包" \
    --version "1.20.1" \
    --loader "forge" \
    --directions 能源 自动化 物流 加工
```

The agent (or user) receives a structured modpack recommendation: per-direction mod recommendations, compatibility matrix, and installation order suggestion.

---

## How the Search Works

```
User Query
    │
    ▼
[Step 1] Quick-reference table (references/mod_quickref.md)
    │
    ├─ Hit → Return immediately (offline, zero API cost)
    │
    └─ Miss → Continue
            │
            ▼
[Step 2] Multi-keyword extraction (_extract_keywords)
    │        Extract 3-5 candidate keywords (Chinese → English mapping)
    ▼
[Step 3] Intent detection
    │
    ├─ Gun/weapon keywords → TACZ priority search (Timeless & Classics Zero ecosystem)
    │                                       │
    │                                       └─ No results → fallback to general search
    │
    ├─ Automation/mechanical keywords → Create priority search (Create addon ecosystem)
    │                                       │
    │                                       └─ No results → fallback to general search
    │
    └─ General query → Continue
            │
            ▼
[Step 4] Concurrent multi-platform search (asyncio + aiohttp)
    │
    ├─ Modrinth: 3-5 keywords in parallel (timeout 8s each, 12s total)
    ├─ CurseForge: if API key is set (timeout 5s each)
    └─ MC Encyclopedia (mcmod.cn): if Modrinth results < 3 (timeout 8s)
            │
            ▼
[Step 5] Merge, deduplicate, rank
    │        Priority: quickref > modrinth > curseforge > mcmod
    │        Scoring: downloads (30%) + update frequency (25%) + rating (25%) + version match (20%)
    │
    ▼
[Step 6] Output (text or JSON)
```

---

## Supported Platforms

| Platform | Access | API Key | Priority | Notes |
|----------|--------|----------|---------|-------|
| **Quick-ref table** | Offline file | ❌ Not needed | 🥇 Highest | `references/mod_quickref.md` — 150+ popular mods |
| **Modrinth** | REST API | ❌ Not needed | 🥈 Primary | `https://api.modrinth.com/v2/search` |
| **CurseForge** | REST API | ✅ Free key | 🥉 Secondary | Get free key at `https://console.curseforge.com/` |
| **MC Encyclopedia (mcmod.cn)** | Web scrape | ❌ Not needed | 4️⃣ Fallback | Triggered only when Modrinth results < 3 |

### CurseForge API Key Setup

If no API key is configured, the skill **explicitly tells the user** how to set one up (it never silently skips CurseForge):

1. Visit https://console.curseforge.com/ to request a free API key
2. Option A: Edit `references/curseforge_api.md`, add `CF_API_KEY=your_key` at the end
3. Option B: Set environment variable: `export CF_API_KEY=your_key`
4. Option C: Pass at runtime: `--api-key your_key`

---

## Quick-Reference Table

The file `references/mod_quickref.md` is a **locally cached hotlist** of 150+ popular/essential Minecraft mods. When the agent receives a user query, it checks this table **before** making any API calls.

**Format:**
```markdown
## Category Name
- English Name | slug: mod-slug | Brief description | loader version
```

**Matching rules (scored):**
| Priority | Condition | Score |
|----------|-----------|-------|
| 1 (highest) | Mod name contained in query | +100 |
| 2 | slug contained in query | +80 |
| 3 | Extracted keyword hits `keywords` field | +30/word |
| 4 | Category name in query | +20 |
| 5 (penalty) | Version mismatch | −20 |

Agents should **always check the quick-ref table first** before calling any external API.

---

## Intent Detection

The skill auto-detects two special mod ecosystems from user queries:

### 🔫 Gun / Weapon Intent → TACZ Ecosystem

**Trigger keywords (Chinese):** 枪, 枪械, 枪包, 枪模組, 射击, 武器, 手枪, 步枪, 狙击, 霰弹枪, 冲锋枪, 机枪, 左轮, 燧发枪, 火枪, 现代战争, 军事, 弹药, 子弹

**Trigger keywords (English):** gun, firearm, weapon, pistol, rifle, sniper, shotgun, smg, machine gun, revolver, musket, gunpack, tac-z, bullet, ammo, fps, combat, warfare, military

When triggered, the skill:
1. Recommends **TACZ base mod** (`timeless-and-classics-zero`) first
2. Searches for **TACZ gunpacks** on Modrinth (category=`equipment`)
3. Explains gunpack installation: place `.zip` into `.minecraft/tacz/`, then run `/tacz reload`

### ⚙️ Automation / Mechanical Intent → Create Ecosystem

**Trigger keywords (Chinese):** 机械, 机械动力, 自动化, 传送带, 齿轮, 活塞, 动力, 轴承, 铁路, 火车, 旋转, 应力, 流水线, 工厂, 制造, 加工, 机械臂, 蒸汽, 风车, 水车

**Trigger keywords (English):** create, createmod, create addon, conveyor, belt, gear, pulley, bearing, piston, automation, factory, assembly, mechanical, train, railway, steam, windmill, kinetic, stress

When triggered, the skill:
1. Recommends **Create base mod** (`create`) first
2. Searches for **Create addon mods** on Modrinth (category=`technology`)
3. Notes Create ↔ OptiFine incompatibility (use Oculus on Forge, Iris on Fabric)

---

## API Reference

### Modrinth API

- **Endpoint:** `https://api.modrinth.com/v2/search`
- **Key params:** `query`, `facets` (JSON array format: `[[...],[...]]`)
- **Rate limit:** ~100 req/min (unauthenticated)
- **Docs:** https://docs.modrinth.com/api/

### CurseForge API

- **Endpoint:** `https://api.curseforge.com/v1/mods/search`
- **Key params:** `gameId=432`, `searchFilter`, `classId=6`
- **Rate limit:** 4290 req/day
- **Docs:** https://docs.curseforge.com/

### MC Encyclopedia (mcmod.cn)

- **No API** — HTML scraping of search result page
- **URL pattern:** `https://www.mcmod.cn/s?key=<query>&mold=1&version=<version>`
- **Note:** Use **original Chinese query** (higher hit rate than translated English)

---

## Known Mod Conflicts

| Mod A | Mod B | Status | Reason |
|-------|-------|--------|--------|
| OptiFine | Sodium | ⚠️ Conflict | Overlapping render optimization |
| OptiFine | Iris | ⚠️ Conflict | Shader loader incompatibility |
| AE2 | Refined Storage | ❌ Incompatible | Both are storage systems |
| Create | OptiFine | ⚠️ Conflict | Flywheel render engine incompatibility |
| REI | EMI | ⚠️ Overlap | Similar item-view functionality |

Full conflict matrix: `references/mod_compat.md`

---

## MCP Configuration

If you want to expose this skill as an **MCP (Model Context Protocol)** tool to agents like Claude:

```json
{
  "mcpServers": {
    "minecraft-mod-search": {
      "command": "python",
      "args": ["/abs/path/to/scripts/search_mods.py"],
      "env": {
        "CF_API_KEY": "your_curseforge_key_here"
      }
    }
  }
}
```

Note: `search_mods.py` uses CLI arguments (`--query`, `--version`, etc.), so you may need a small wrapper script to adapt it to MCP's stdin-based JSON-RPC format. See `references/mcp_adapter_example.py` (community contribution welcome).

---

## File Structure

```
minecraft-mod-search/
├── SKILL.md              # 🔑 Skill definition (agent-facing)
├── README.md             # This file (human-facing)
├── LICENSE               # MIT License
├── references/
│   ├── modrinth_api.md   # Modrinth API documentation
│   ├── curseforge_api.md  # CurseForge API documentation + API key config
│   ├── mc_versions.md    # Minecraft version compatibility reference
│   ├── mod_compat.md     # Mod conflict matrix (includes TACZ & Create details)
│   └── mod_quickref.md   # 🔑 Quick-reference table (150+ mods, offline)
└── scripts/
    └── search_mods.py    # Core search script (v2.0, async + aiohttp)
```

---

## Contributing

Pull requests are welcome! Please:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Particularly welcome:**
- Additional mods for `references/mod_quickref.md`
- Additional conflict entries for `references/mod_compat.md`
- MCP adapter script (`references/mcp_adapter_example.py`)
- Wrapper scripts for other agent frameworks

---

## License

MIT License — see [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- [Modrinth](https://modrinth.com/) — Primary mod hosting platform
- [CurseForge](https://www.curseforge.com/) — Secondary mod hosting platform
- [MC Encyclopedia (mcmod.cn)](https://www.mcmod.cn/) — Chinese Minecraft mod database
- All Minecraft mod developers who make the game infinitely replayable
