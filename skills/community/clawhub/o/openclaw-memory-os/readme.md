# OpenClaw Memory-OS

**English** | [中文](#openclaw-memory-os-中文版)

## 🛡️ Security & Privacy Notice (v0.2.2)

**Current Version:** 0.2.2
**Status:** 100% Local, Zero External APIs, Privacy-First Conversation Memory

**🔒 Privacy Notice (v0.2.2):**
- ✅ **AUTO-TRIGGER is OFF by default** (opt-in only)
- ⚠️ **No confirmation prompt** when enabled (saves immediately - planned for v0.3.0)
- ⚠️ **Privacy filter exists but not integrated** (code implemented, CLI integration pending)
- ⚠️ **No encryption at rest** (plain JSON files)
- ✅ **100% local runtime** - zero network calls during operation (installation requires npm)

**What This Version Does:**
- ✅ Local file-based memory storage (JSON format)
- ✅ Basic keyword search (all local computation)
- ✅ Batch file collection (user-triggered CLI)
- ✅ **Conversation memory extraction** (extract from natural language)
- ✅ **Auto-trigger support** (opt-in, saves immediately without confirmation in v0.2.2)
- ✅ Recursive directory scanning with progress display
- ✅ Automatic file type detection (TEXT vs CODE)
- ✅ Timeline and statistics (local only)

**What This Version Does NOT Do:**
- ❌ No AI embeddings or semantic search
- ❌ No LLM or external API calls
- ❌ No automatic background collection
- ❌ No network activity whatsoever
- ❌ No API keys required

**Your Data:**
- Stored: `~/.memory-os/` (local JSON files)
- Control: You decide what to collect and when
- Ownership: You own all data files
- Deletion: `rm -rf ~/.memory-os/` removes everything

**Recommended Safe Usage:**
1. Test in sandbox/VM first
2. Review files before collection
3. Use specific paths (not broad patterns like `~/Documents`)
4. Inspect collected data in `~/.memory-os/memories/`
5. Monitor network activity (should be zero)

See full security details: [SECURITY.md](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/SECURITY.md)

---

## Overview

Memory-OS is an open-source personal memory management system designed for digital immortality and cognitive continuity. It can collect, store, retrieve, and intelligently process all your digital memories, build personal knowledge graphs, and provide the ability to have conversations with your digitized "self".

**v0.2.2 Focus:** Opt-in conversation memory with local-only storage. AUTO-TRIGGER is disabled by default and saves directly when enabled (no confirmation prompt in v0.2.2). Privacy filter code exists but CLI integration pending. Extract and store information from natural conversations. AI features (semantic search, LLM integration) are planned but NOT implemented in this version.

## Core Features

**Current (v0.2.2):**
- **Opt-In Design** - AUTO-TRIGGER disabled by default
- **Local Storage** - JSON-based file storage, no cloud dependency, no encryption
- **Conversation Memory** - Extract information from natural language
- **Auto-Trigger** - Opt-in, saves immediately (no confirmation prompt)
- **Entity Extraction** - Automatically extracts names, dates, events
- **Privacy Filter** - Code implemented, CLI integration pending v0.3.0
- **Batch File Collection** - Import entire directories with one command
- **Recursive Scanning** - Automatically processes subdirectories
- **Type Detection** - Distinguishes CODE from TEXT files automatically
- **Real-time Progress** - Shows filenames during import
- **Basic Search** - Keyword and tag-based filtering (local)
- **Timeline Tracking** - Temporal organization of memories
- **Privacy-First** - All data stays on your machine
- **Extensible** - Modular architecture for future enhancements

**Planned (v0.2.0+):**
- **Semantic Search** - AI-powered understanding (will require API key)
- **Knowledge Graph** - Automatic relationship discovery (will require API key)
- **LLM Chat** - Conversation with your memories (will require API key)

## Quick Start

### Installation

```bash
# Install via npm
npm install -g openclaw-memory-os

# Or install from source
git clone https://github.com/ZhenRobotics/openclaw-memory-os.git
cd openclaw-memory-os
npm install
npm run build
npm link
```

### Initialization

```bash
# Initialize Memory-OS (creates ~/.memory-os/)
openclaw-memory-os init

# Configure basic information (optional)
openclaw-memory-os config set owner.name "Your Name"
openclaw-memory-os config set owner.email "your@email.com"
```

### Basic Usage

```bash
# Conversation memory (with confirmation prompt)
openclaw-memory-os remember "记住我的名字：刘小容"
openclaw-memory-os remember "Remember the project deadline is 2026-04-01"

# Batch file collection
openclaw-memory-os collect --source ~/my-notes/
openclaw-memory-os collect --source ~/Documents/ --exclude node_modules .git

# Search memories (local keyword search)
openclaw-memory-os search "AI discussions"
openclaw-memory-os search --type code "function"

# View statistics
openclaw-memory-os status
```

### Security Verification

```bash
# Verify data location
ls -la ~/.memory-os/memories/

# Inspect collected memories
cat ~/.memory-os/memories/*.json | jq '.'

# View collection statistics
openclaw-memory-os status

# Monitor network activity (should be ZERO for v0.1.1)
# In one terminal:
sudo tcpdump -i any port 443 or port 80

# In another terminal:
openclaw-memory-os collect --source ~/test-data/
# Should see NO network traffic
```

## Core Concepts

### Memory Unit

The smallest memory unit in Memory-OS, containing:

```typescript
interface Memory {
  id: string;              // Unique identifier (UUID)
  type: MemoryType;        // Type: text, code, chat, file, media, activity
  content: any;            // Content (stored as-is)
  metadata: {
    source: string;        // Source identifier
    timestamp: Date;       // Creation timestamp
    tags: string[];        // User-defined tags
    context: string;       // Optional context
  };
  createdAt: Date;
  updatedAt: Date;
}
```

### Collectors

Collect memories from different data sources:

- `FileCollector` - Documents, notes (.txt, .md, .json, code files)
- `ChatCollector` - Chat history (planned)
- `CodeCollector` - Code repositories (planned)
- `MediaCollector` - Images, audio, video (planned)
- `ActivityCollector` - System activities (planned)

**v0.1.0:** Only `FileCollector` is implemented.

### Storage Layer

**v0.1.1:** Local file system storage

- JSON files in `~/.memory-os/memories/`
- Index file for fast lookup
- Human-readable format
- No encryption (can be added manually)
- Content stored as searchable strings

**Future versions:** Optional vector storage, graph storage, cloud sync.

## Use Cases

### 1. Personal Knowledge Management

```bash
# Import your notes
openclaw-memory-os collect --source ~/Documents/Notes/

# Search for specific topics
openclaw-memory-os search "machine learning algorithms"

# View by timeline
openclaw-memory-os timeline --range "last month"
```

### 2. Memory Recall

```bash
# View activities on a specific day
openclaw-memory-os timeline --date 2024-01-15

# Search for specific content
openclaw-memory-os search --type text --query "project ideas"
```

### 3. API Integration

```typescript
import { MemoryOS, MemoryType } from 'openclaw-memory-os';

const memory = new MemoryOS({
  storePath: '~/.memory-os',
});

await memory.init();

// Collect memory
await memory.collect({
  type: MemoryType.TEXT,
  content: 'Important note about project X',
  metadata: {
    tags: ['project', 'important'],
    source: 'manual',
  },
});

// Search memories
const results = await memory.search({
  query: 'project',
  limit: 10,
});

// View statistics
const stats = await memory.stats();
console.log(`Total memories: ${stats.totalMemories}`);
```

## Documentation

- [README](https://github.com/ZhenRobotics/openclaw-memory-os#readme) - Complete guide
- [SECURITY](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/SECURITY.md) - Security and privacy details
- [ARCHITECTURE](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/ARCHITECTURE.md) - System design
- [QUICKSTART](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/QUICKSTART.md) - 5-minute guide

## Community

- **GitHub**: https://github.com/ZhenRobotics/openclaw-memory-os
- **npm**: https://www.npmjs.com/package/openclaw-memory-os
- **ClawHub**: https://clawhub.ai/skills/openclaw-memory-os
- **Issues**: https://github.com/ZhenRobotics/openclaw-memory-os/issues

## Contributing

Contributions of code, documentation, and ideas are welcome! Please read [CONTRIBUTING.md](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/CONTRIBUTING.md).

## License

MIT-0 License

---

**Memory-OS - Make Memory Eternal, Make Cognition Continue**

---

# OpenClaw Memory-OS (中文版)

**[English](#openclaw-memory-os)** | 中文

## 🛡️ 安全与隐私声明（v0.2.2）

**当前版本：** 0.2.2
**状态：** 100% 本地，零外部 API，隐私优先的对话记忆

**🔒 隐私声明（v0.2.2）：**
- ✅ **AUTO-TRIGGER 默认关闭**（仅限选择加入）
- ⚠️ **启用后无确认提示**（立即保存 - v0.3.0 计划实现）
- ⚠️ **隐私过滤器已实现但未集成**（代码完成，CLI 集成待实现）
- ⚠️ **无静态加密**（明文 JSON 文件）
- ✅ **100% 本地运行** - 运行时零网络调用（安装需要 npm）

**此版本功能：**
- ✅ 本地文件记忆存储（JSON 格式）
- ✅ 基本关键词搜索（全部本地计算）
- ✅ 批量文件采集功能（用户触发的 CLI）
- ✅ **对话记忆提取**（从自然语言提取）
- ✅ **自动触发支持**（选择加入，v0.2.2 无确认提示立即保存）
- ✅ 递归目录扫描并显示进度
- ✅ 自动文件类型检测（TEXT vs CODE）
- ✅ 时间线和统计（仅本地）

**此版本不包含：**
- ❌ 无 AI 向量化或语义搜索
- ❌ 无 LLM 或外部 API 调用
- ❌ 无自动后台收集
- ❌ 无任何网络活动
- ❌ 无需 API 密钥

**您的数据：**
- 存储位置：`~/.memory-os/`（本地 JSON 文件）
- 控制权：您决定收集什么和何时收集
- 所有权：您拥有所有数据文件
- 删除方式：`rm -rf ~/.memory-os/` 删除所有内容

**推荐安全使用：**
1. 先在沙盒/虚拟机中测试
2. 收集前检查文件
3. 使用明确路径（不要用 `~/Documents` 等广泛模式）
4. 检查收集的数据在 `~/.memory-os/memories/`
5. 监控网络活动（应该为零）

详见完整安全说明：[SECURITY.md](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/SECURITY.md)

---

## 概述

Memory-OS 是一个开源的个人记忆管理系统，旨在实现数字永生和认知延续。它能够采集、存储、检索和智能化处理你的所有数字记忆，构建个人知识图谱，并提供与数字化"自我"对话的能力。

**v0.2.2 重点：** 选择加入的对话记忆，纯本地存储。AUTO-TRIGGER 默认关闭，启用后直接保存（v0.2.2 无确认提示）。隐私过滤器代码已实现但 CLI 集成待完成。从自然对话中提取并存储信息。AI 功能（语义搜索、LLM 集成）已计划但此版本未实现。

## 核心特性

**当前版本（v0.2.2）：**
- **选择加入设计** - AUTO-TRIGGER 默认关闭
- **本地存储** - 基于 JSON 文件，无云端依赖，无加密
- **对话记忆** - 从自然语言提取信息
- **自动触发** - 选择加入，立即保存（无确认提示）
- **实体提取** - 自动提取姓名、日期、事件
- **隐私过滤** - 代码已实现，CLI 集成待完成 v0.3.0
- **批量采集** - 从指定文件和目录
- **基本搜索** - 关键词和标签过滤（本地）
- **时间线追踪** - 记忆的时间组织
- **可扩展** - 模块化架构便于未来增强

**计划功能（v0.2.0+）：**
- **语义搜索** - AI 驱动的理解（需要 API 密钥）
- **知识图谱** - 自动关系发现（需要 API 密钥）
- **LLM 对话** - 与您的记忆对话（需要 API 密钥）

## 快速开始

[安装和使用说明与英文版相同]

## 文档

- [README](https://github.com/ZhenRobotics/openclaw-memory-os#readme) - 完整指南
- [安全](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/SECURITY.md) - 安全和隐私详情
- [架构](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/ARCHITECTURE.md) - 系统设计
- [快速入门](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/QUICKSTART.md) - 5分钟指南

## 社区

- **GitHub**: https://github.com/ZhenRobotics/openclaw-memory-os
- **npm**: https://www.npmjs.com/package/openclaw-memory-os
- **ClawHub**: https://clawhub.ai/skills/openclaw-memory-os
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-memory-os/issues

## 贡献

欢迎贡献代码、文档和想法！请阅读 [CONTRIBUTING.md](https://github.com/ZhenRobotics/openclaw-memory-os/blob/main/CONTRIBUTING.md)。

## 许可证

MIT-0 License

---

**Memory-OS - 让记忆永存，让认知延续**

---

**Version:** 0.2.2
**Verified Commit:** 091eeab
**Security Status:** Local-Only, Zero External APIs, Opt-In Design
**Production Ready:** Test in sandbox first (no confirmation prompt, privacy filter pending)
