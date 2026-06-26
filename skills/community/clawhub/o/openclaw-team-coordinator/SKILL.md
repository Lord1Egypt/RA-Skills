---
name: openclaw-team-coordinator
description: OpenClaw任务分工协调skill，用于明确团队角色和CLI工具分工。当OpenClaw下发任务、分配工作、创建子任务、协调多Agent协作、或需要明确前后端分工和QA验收流程时使用此skill。
---

# OpenClaw Team Coordinator

## 概述

OpenClaw作为主脑(PM)协调Gemini CLI(前端)和Codex CLI(后端)，Claude负责QA验收。

## 团队架构

```
Claude (PM/主脑)
├── 任务规划与分配
├── 进度监控
└── QA验收
    │
    ├── Gemini CLI (前端)
    │   └── React/Vue/HTML/CSS/UI组件
    │
    └── Codex CLI (后端)
        └── API/数据库/业务逻辑
```

## CLI工具职责

| Agent | CLI工具 | 职责范围 |
|-------|---------|----------|
| Claude | Claude CLI | 主脑PM、任务分配、进度协调、QA验收 |
| Gemini CLI | Gemini CLI | 前端开发：React/Vue组件、样式、交互 |
| Codex CLI | Codex CLI | 后端开发：API、数据库、Server逻辑 |

## 任务分配规则

### 任务下发流程

1. **任务接收**：OpenClaw接收用户需求
2. **任务分析**：Claude分析任务类型（前端/后端/全栈）
3. **任务分发**：
   - 前端任务 → Gemini CLI
   - 后端任务 → Codex CLI
   - 全栈任务 → 分解后分别下发
4. **进度跟踪**：Claude跟踪各Agent进度
5. **QA验收**：Claude进行最终验收

### 任务类型判断

```
IF 任务包含 "前端" OR "UI" OR "界面" OR "React" OR "Vue" OR "HTML" OR "样式":
    → Gemini CLI

ELIF 任务包含 "后端" OR "API" OR "数据库" OR "Server" OR "逻辑":
    → Codex CLI

ELSE:
    → Claude先分析，再拆分下发
```

### QA验收标准

所有任务完成后必须经过Claude进行QA验收：
- 功能完整性
- 代码质量
- 安全性检查
- 性能评估

## 使用场景

- OpenClaw下发新任务
- 需要分配前端/后端工作
- 多Agent协作需要协调
- 任务进度跟踪
- 最终QA验收

## 快速开始

当收到任务时：
1. 分析任务类型
2. 调用对应CLI Agent
3. 监控执行进度
4. 执行Claude QA验收
5. 汇总结果反馈
