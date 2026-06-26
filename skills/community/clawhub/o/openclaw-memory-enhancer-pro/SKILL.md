---
name: memory-enhancer-pro
displayName: Memory Enhancer Pro - 记忆增强专业版
version: 2.0.0
description: |
  Memory Enhancer Pro - 专业版记忆增强工具，让 AI 记住所有重要信息。
  支持语义搜索、自动提炼、智能分类、Token 优化、定时任务。
  优化 token 消耗 30-60%，自动压缩旧记忆。功能超越基础版。
  关键词：memory, enhancer, pro, search, ai, token-optimizer, rag, semantic
license: MIT-0
acceptLicenseTerms: true
tags:
  - memory
  - enhancer
  - pro
  - search
  - ai
  - productivity
  - optimization
  - token-optimizer
  - scheduled-tasks
  - rag
  - semantic-search
  - advanced
---

# Memory Enhancer - 记忆增强助手

强大的记忆管理工具，让 AI 记住所有重要信息。

---

## ✨ 功能特性

- 🔍 **语义搜索** - 搜索所有记忆文件，找到相关内容
- 📌 **自动提炼** - 自动提炼对话要点，保存到 MEMORY.md
- 🏷️ **智能分类** - 自动分类（偏好/决策/待办/项目）
- 🔗 **关联推荐** - 推荐相关的记忆片段
- 🧹 **过期清理** - 自动清理过期记忆
- 📊 **使用统计** - 记忆文件统计、搜索历史

---

## 🚀 安装

```bash
cd ~/.openclaw/workspace/skills
# 技能已安装在：~/.openclaw/workspace/skills/memory-enhancer
chmod +x memory-enhancer/scripts/*.py
```

---

## 📖 使用

### 语义搜索

```bash
python3 memory-enhancer/scripts/search.py "上次提到的飞书配置"
```

### 自动提炼

```bash
python3 memory-enhancer/scripts/summarize.py --session today
```

### 记忆分类

```bash
python3 memory-enhancer/scripts/classify.py --auto
```

---

## 🛠️ 脚本说明

| 脚本 | 功能 | 写入文件 |
|------|------|---------|
| `search.py` | 语义搜索 | ❌ 否 |
| `summarize.py` | 自动提炼 | ❌ 否 |
| `classify.py` | 智能分类 | ❌ 否 |
| `token-optimizer.py` | Token 优化分析 | ✅ config/, logs/ |
| `scheduled-optimizer.py` | 定时任务 | ✅ config/, logs/ |
| `cleanup.py` | 过期清理 | ✅ 删除旧文件 |

---

## 📄 许可证

MIT-0

---

**作者：** @williamwg2025  
**版本：** 1.0.0

---

## 🔒 安全说明

### 文件写入 ⚠️
**本技能会写入文件：**
- **配置文件：** `~/.openclaw/workspace/skills/memory-enhancer/config/`
  - `token-stats.json` - Token 使用统计
  - `token-optimizer-schedule.json` - 定时任务配置
- **日志文件：** `~/.openclaw/workspace/skills/memory-enhancer/logs/`
  - `optimizer-schedule.log` - 定时任务执行日志
- **记忆文件：** `~/.openclaw/workspace/memory/`
  - 每日记忆文件（由其他技能创建，本技能可能清理）

**只读操作：**
- 读取 `~/.openclaw/workspace/MEMORY.md`
- 读取 `~/.openclaw/workspace/SESSION-STATE.md`
- 读取会话历史（不修改）

### 网络访问
- **不联网：** 所有操作在本地执行
- **无外部依赖：** 不克隆外部仓库

### 定时任务 ⚠️
**如启用定时任务：**
- 需要手动添加 cron 条目到系统 crontab
- 或使用 OpenClaw 内置 cron（推荐）
- 定时任务会定期执行写入操作

**建议：**
1. 先手动运行测试（`--analyze`）
2. 确认输出符合预期
3. 再启用定时任务

### 数据安全
- **本地存储：** 所有数据保存在本地
- **不上传：** 不发送数据到外部服务器
- **建议备份：** 启用定时任务前备份 `~/.openclaw/`

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
