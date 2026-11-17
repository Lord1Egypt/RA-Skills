# mc-mod-translate

**An AI Agent Skill for translating Minecraft Java Edition mod content from English to Simplified Chinese.**

**一个用于将 Minecraft Java 版模组内容从英文翻译为简体中文的 AI Agent 技能。**

---

## Features | 功能特性

- Uses a community-maintained dictionary of **900,000+ entries** covering vanilla Minecraft items and **3,500+ mods**
- Dictionary auto-updated weekly by [i18n-Dict-Extender](https://github.com/VM-Chinese-translate-group/i18n-Dict-Extender)
- Vanilla MC terms looked up via [zh.minecraft.wiki](https://zh.minecraft.wiki/) MediaWiki API
- Translation priority: dictionary match → wiki lookup → context-based AI translation
- Supports multiple file types: language files (`.lang`/`.json`), FTB Quests SNBT, config files, Patchouli books
- Fast SQLite-indexed lookups with multiple query modes

---

- 使用社区维护的 **90 万+ 条目** 词典，覆盖 Minecraft 原版物品及 **3,500+ 个模组**
- 词典由 [i18n-Dict-Extender](https://github.com/VM-Chinese-translate-group/i18n-Dict-Extender) 每周自动更新
- 原版游戏术语通过 [zh.minecraft.wiki](https://zh.minecraft.wiki/) MediaWiki API 在线查询
- 翻译优先级：词典匹配 → Wiki 查询 → 基于上下文的 AI 翻译
- 支持多种文件类型：语言文件（`.lang`/`.json`）、FTB Quests SNBT、配置文件、Patchouli 手册
- 基于 SQLite 索引的快速查询，支持多种查询模式

---

## Setup | 安装

### 1. Clone the repository | 克隆仓库

```bash
git clone https://github.com/CSCTACG/mc-mod-translate.git
cd mc-mod-translate
```

### 2. Download the dictionary database | 下载词典数据库

```bash
python3 scripts/fetch_dict.py
```

Downloads the latest `Dict-Sqlite.db` (~142 MB) from [i18n-Dict-Extender releases](https://github.com/VM-Chinese-translate-group/i18n-Dict-Extender/releases). Use `--check` to check for updates without downloading, or `--force` to re-download.

从 [i18n-Dict-Extender releases](https://github.com/VM-Chinese-translate-group/i18n-Dict-Extender/releases) 下载最新的 `Dict-Sqlite.db`（约 142 MB）。使用 `--check` 仅检查是否有更新，使用 `--force` 强制重新下载。

### 3. Requirements | 环境要求

Python 3.8+ with standard library only (`sqlite3`, `urllib`). No pip install needed.

Python 3.8+，仅需标准库（`sqlite3`、`urllib`），无需额外安装依赖。

---

## Usage | 使用方法

### Query the dictionary | 查询词典

```bash
# List all mods with entry counts | 列出所有模组及条目数
python3 scripts/query.py --list-mods

# Search for a mod by keyword | 按关键词搜索模组
python3 scripts/query.py --list-mods --search tconstruct

# Dump all translations for a mod | 导出某个模组的全部翻译
python3 scripts/query.py --modid tconstruct --limit 10000

# Look up by English text (dict + wiki fallback) | 按英文文本查询（词典 + Wiki 回退）
python3 scripts/query.py --text "Copper Ingot"

# Dict only, skip wiki | 仅查词典，跳过 Wiki
python3 scripts/query.py --text "Copper Ingot" --no-wiki

# Look up by lang key | 按 lang key 查询
python3 scripts/query.py --key "block.minecraft.stone"

# Combined filter | 组合查询
python3 scripts/query.py --modid tconstruct --text "Copper"

# JSON output | JSON 格式输出
python3 scripts/query.py --text "Copper Ingot" --json
```

### Integration with AI Agents | 与 AI Agent 集成

Any AI agent (Claude, GPT, Gemini, local LLMs, etc.) can use this skill by following the instructions in `SKILL.md`. The agent should:

任何 AI Agent（Claude、GPT、Gemini、本地大模型等）均可按照 `SKILL.md` 中的说明使用此技能。Agent 将：

1. Download/update the dictionary DB if not present | 如词典不存在则先下载
2. Identify the mod from file paths or lang keys | 从文件路径或 lang key 识别模组
3. Query the dictionary for known translations | 查询词典获取已知翻译
4. Fall back to zh.minecraft.wiki for vanilla terms | 回退到 zh.minecraft.wiki 查询原版术语
5. Use context-based translation for remaining text | 对剩余文本基于上下文翻译

---

## Data Sources | 数据来源

| Source | Description | URL |
|--------|-------------|-----|
| i18n-Dict-Extender | Community-maintained mod translation dictionary (weekly auto-update) | [GitHub](https://github.com/VM-Chinese-translate-group/i18n-Dict-Extender) |
| zh.minecraft.wiki | Vanilla Minecraft term lookup via redirect resolution | [Wiki API](https://zh.minecraft.wiki/api.php) |
| CFPA i18n-dict | Base dictionary (CFPA community translations) | [GitHub](https://github.com/CFPATools/i18n-dict) |

| 来源 | 说明 | 链接 |
|------|------|------|
| i18n-Dict-Extender | 社区维护的模组翻译词典（每周自动更新） | [GitHub](https://github.com/VM-Chinese-translate-group/i18n-Dict-Extender) |
| zh.minecraft.wiki | 原版 Minecraft 术语查询（通过重定向解析） | [Wiki API](https://zh.minecraft.wiki/api.php) |
| CFPA i18n-dict | 基础词典（CFPA 社区翻译） | [GitHub](https://github.com/CFPATools/i18n-dict) |

---

## File Structure | 文件结构

```
mc-mod-translate/
├── SKILL.md                 # Skill instructions for AI agents | Agent 指令文件
├── README.md
├── .gitignore
├── scripts/
│   ├── fetch_dict.py        # Download latest Dict-Sqlite.db | 下载最新词典
│   ├── query.py             # Query dictionary DB + wiki | 查询词典 + Wiki
│   └── Dict-Sqlite.db       # Downloaded SQLite database (not in repo) | 下载的数据库（不在仓库中）
```

---

## License | 许可证

The dictionary data follows [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) (community translation content). The code in this repository is [MIT](LICENSE) licensed.

词典数据遵循 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 协议（社区翻译内容）。本仓库代码采用 [MIT](LICENSE) 协议。
