---
name: memory-archiver-hook
description: "统一记忆 Hook：自动搜索 + 自动提取 + 会话笔记追踪"
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "events": ["message:received"],
        "install": [{ "id": "local", "kind": "local", "label": "Local workspace hook" }],
      },
  }
---

# Memory Archiver 统一 Hook

**整合功能**（原 3 个独立 Hook）：
1. 自动记忆搜索（auto-memory-search）
2. 自动记忆提取（auto-memory-extract）
3. 会话笔记追踪（session-notes）

## 触发方式

- **事件**: `message:received`
- **优先级**: 单 Hook 统一处理，避免重复触发

## 模块 1: 自动记忆搜索

当用户消息包含以下类型时，自动搜索相关记忆并注入上下文：

| 类型 | 触发关键词 |
|------|-----------|
| 疑问 | 怎么, 如何, 为什么, what, how, why |
| 修复 | bug, 错误, 修复, fix, error |
| 规范 | 规范, 规则, 标准, spec, rule |
| 特征 | 特征, 特点, feature |
| 配置 | 配置, 设置, 安装, config, setup |
| 命令 | 命令, 脚本, 用法, command |
| 技术 | css, html, php, javascript, tailwind, vite |

## 模块 2: 自动记忆提取

从每条用户消息中自动提取持久记忆，分类存储到：

- `memory/auto/user/` — 用户偏好、角色、目标
- `memory/auto/feedback/` — 纠正、工作模式调整
- `memory/auto/project/` — 项目上下文、环境、工作流
- `memory/auto/reference/` — 参考资料、命令、解决方案

## 模块 3: 会话笔记追踪

- 自动初始化会话笔记
- 每 10 条消息更新一次
- 笔记写入 `memory/sessions/`
- 会话结束后可归档

## 文件结构

```
skills/memory-archiver/
├── hooks/
│   ├── handler.js        # 统一 Hook 处理器
│   └── HOOK.md           # 本文件
├── scripts/
│   ├── auto-memory-search.js  # 记忆搜索脚本
│   ├── memory-extract.js      # 记忆提取脚本
│   ├── memory-classify.js     # 记忆分类脚本
│   ├── memory-dedup-extract.js # 记忆去重脚本
│   └── session-tracker.js     # 会话追踪脚本
└── ...
```

## 禁用

```bash
openclaw hooks disable memory-archiver-hook
```
