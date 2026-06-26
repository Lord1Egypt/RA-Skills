---
name: good-memory
version: 2.0.1
description: Session 历史记录恢复技能。Session重置后自动恢复对话上下文，解决系统自动重置导致的"失忆"问题。
homepage: https://github.com/openclaw/openclaw
metadata: {"openclaw":{"emoji":"🧠","requires":{"bins":["bash","tail","ls","python3"]}}}
---

# Good-Memory v2.0.0

帮助 Agent 在 session 重置后快速恢复对话上下文。通过检测 `.reset.` 后缀的 session 文件实现，**安装后自动运行，无需手动操作**。

## 核心特性
- ✅ **全平台支持**：支持飞书、Discord、Telegram、Signal等所有OpenClaw平台
- ✅ **零配置**：安装后自动生效，不需要修改配置
- ✅ **轻量高效**：仅基于文件名匹配，不需要解析文件内容，速度快
- ✅ **低侵入性**：默认只修改main的AGENTS.md，不影响其他Agent
- ✅ **自动清理**：历史记录最多保留10条，自动清理过期文件

## 工作原理
1. **重置检测**：每次session启动时自动检测两种重置类型：
   - ✅ **显式重置**：session 文件被系统添加 `.reset.` 后缀（系统自动重置 /new /reset 命令触发）
   - ✅ **隐式切换**：新 session UUID 生成但旧 session 未打 reset 标记（系统自动会话轮换/后台重启触发）
2. **历史恢复**：如果检测到重置/切换，自动读取上一个会话文件的最后50条对话
3. **自动提示**：首条回复会告知用户已恢复历史记录

## 安装

### 🚀 一键安装（推荐）
```bash
# 下载并安装
curl -sSL https://wry-manatee-359.convex.site/api/v1/download?slug=good-memory | bash -s install
```

### 手动安装
```bash
# 1. 创建目录
mkdir -p ~/.openclaw/workspace/skills/good-memory
cd ~/.openclaw/workspace/skills/good-memory

# 2. 下载解压
curl -L https://wry-manatee-359.convex.site/api/v1/download?slug=good-memory | unzip -

# 3. 执行安装
bash scripts/install.sh
```

## 环境变量（可选）
如果你的OpenClaw安装在非默认路径，可以设置：
```bash
export OPENCLAW_BASE="/path/to/your/openclaw"  # 默认：/root/.openclaw
export SESSIONS_DIR="/path/to/sessions"        # 默认：$OPENCLAW_BASE/agents/main/sessions
export AGENTS_MD="/path/to/AGENTS.md"          # 默认：$OPENCLAW_BASE/workspace/AGENTS.md
```

## 手动使用
```bash
# 查看最新的reset文件
bash ~/.openclaw/workspace/skills/good-memory/scripts/recovery.sh latest

# 读取最新reset的50条记录
bash ~/.openclaw/workspace/skills/good-memory/scripts/recovery.sh read --lines 50

# 列出所有reset文件
bash ~/.openclaw/workspace/skills/good-memory/scripts/recovery.sh list
```

## 数据结构
`session-tracker.json` 格式（简化版）：
```json
{
  "description": "Session tracker - maps agent+chat to session files",
  "last_updated": "2026-03-27T15:00:00Z",
  "agents": {
    "main": {
      "ou_123456": {
        "session_key": "",
        "active": "/path/to/current.jsonl",
        "active_uuid": "abc123",
        "last_history": "/path/to/old.jsonl.reset.2026-03-27T15:00:00Z",
        "history": [
          "/path/to/old.jsonl.reset.2026-03-27T15:00:00Z",
          "/path/to/older.jsonl.reset.2026-03-26T10:00:00Z"
        ]
      }
    }
  }
}
```
