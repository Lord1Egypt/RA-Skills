---
name: memory-optimizer-base
description: |
  多Agent记忆管理系统 - 开放协作的知识库解决方案
  支持私有+公共双层记忆空间，自动生成每日总结，跨Agent知识检索

version: 0.2.0
author: 小天 (改造自 kimi-claw-sanqian-memory-optimizer)
license: MIT-0
tags:
  - openclaw
  - memory
  - multi-agent
  - knowledge-sharing
  - collaboration
---

# Multi-Agent Memory Optimizer

> 让每个 AI Agent 拥有独立记忆，同时共享公共知识库

## 🌟 核心价值

- **隐私保护**：每个 Agent 独立记忆空间，互不干扰
- **知识传承**：重要经验发布到公共空间，其他 Agent 可检索使用
- **自动化**：每日自动生成总结（通过 crontab），减少人工负担
- **开箱即用**：完整工具链，5 分钟快速部署

---

## 📦 安装

```bash
# 1. 进入 skills 目录
cd ~/.npm-global/lib/node_modules/@qingchencloud/openclaw-zh/skills/

# 2. 确保此技能目录存在
#    memory-optimizer-base/

# 3. 初始化你的 Agent
./memory-optimizer-base/memory_optimizer.py init --agent <your_agent_id>
```

---

## 🎯 核心工作流

```
1. OpenClaw 日常会话 → 记录到 memory/YYYY-MM-DD.md
2. 每日 23:00 自动 summarize → 生成 medium-term/YYYY-MM-DD.md
3. 人工确认内容 → 执行 upload → 发布到 public/<agent>/<date>/
4. 任何 Agent 可 search-public → 获取其他 Agent 的经验
```

---

## 🔨 命令速查

```bash
# 初始化
./memory_optimizer.py init --agent xiaotian

# 手动生成总结（测试用）
./memory_optimizer.py summarize --agent xiaotian --date 2026-04-06

# 上传到公共空间
./memory_optimizer.py upload --agent xiaotian --date 2026-04-06 --title "事件标题"

# 搜索公共知识
./memory_optimizer.py search-public "关键词"

# 查看私有记忆
./memory_optimizer.py private list --agent xiaotian

# 分析系统状态
./memory_optimizer.py analyze --agent xiaotian

# 配置管理
./memory_optimizer.py config --set memory.sync_enabled=true
```

---

## ⚙️ 配置

编辑 `config/default.json`：

```json
{
  "memory": {
    "base_path": "~/.openclaw/workspace-xiaotian",
    "private_root": "memory/private",
    "public_root": "memory/public",
    "medium_term_retention_days": 1
  },
  "summarizer": {
    "template": "...",  // 自定义输出格式
  },
  "upload": {
    "require_upload_confirm": true  // 发布前是否需要人工确认
  }
}
```

---

## 📂 文件结构

```
memory-optimizer-base/
├── memory_optimizer.py   # 主程序
├── .gitignore            # 隐私保护
├── README.md             # 详细文档
├── SKILL.md              # 本文档
├── config/
│   ├── default.json      # 默认配置
│   └── agents/           # 各 Agent 配置（自动生成）
└── lib/                  # 核心模块
    ├── analyzer.py
    ├── summarizer.py
    ├── uploader.py
    ├── retriever.py
    ├── optimizer.py
    ├── tierer.py
    └── sync.py
```

---

## 🔐 安全与隐私

- ✅ 所有真实记忆文件（`memory/`、`.openclaw/`）已在 `.gitignore` 中排除
- ✅ 默认上传需人工确认，避免误发
- ✅ 私有空间严格隔离，公共空间仅包含主动分享的内容
- ⚠️ 公共空间内容永久可见，发布前请检查

---

## 📖 完整文档

详见 [README.md](./README.md)

---

## 🤝 贡献

欢迎 Issue 和 PR！

---

**版本**: 0.2.0 | **许可**: MIT-0
