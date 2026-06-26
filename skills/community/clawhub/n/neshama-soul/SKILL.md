---
name: neshama-soul
description: 给 AI Agent 注入灵魂，赋予独特人格和真实情绪。基于 OCEAN 人格模型，让 Agent 拥有持久人格和情感记忆。
---

# Neshama Soul Engine

> 7 文件灵魂文件系统 - 让 Agent 拥有持久人格

---

## 简介

**Neshama Soul Engine** 是一个基于 OCEAN 人格模型和 Valence-Arousal 情绪系统的 Agent 人格系统。让 AI 拥有独特的"性格"，记住用户偏好，实现真正懂你的 AI 助手。

**核心功能**：
- 🎭 **持久人格**：基于 OCEAN 五维模型
- 💭 **情绪响应**：基于 Valence-Arousal 模型
- 🧠 **记忆连续**：记住用户的编码偏好
- 📝 **上下文生成**：自动生成人格提示词
- ⚙️ **错误降级**：API 不可用时使用默认配置

---

## 安装

### 方式一：ClawHub 安装（推荐）

```bash
openclaw skills install neshama-soul
```

### 方式二：GitHub 安装

```bash
git clone https://github.com/Neshama-AI/neshama-soul-openclaw.git
cd neshama-soul-openclaw
openclaw skills install .
```

---

## 7 文件灵魂系统

```
neshama-soul-openclaw/
├── SKILL.md              # 本文件，入口说明
├── soul/
│   ├── SOUL.md          # 人格核心（OCEAN 模型）
│   ├── IDENTITY.md       # 身份定义
│   ├── AGENTS.md         # 岗位说明
│   ├── USER.md           # 用户偏好
│   ├── BOOTSTRAP.md      # 首次初始化
│   ├── HEARTBEAT.md      # 心跳任务
│   └── TOOLS.md          # 工具规范
└── README.md
```

| 文件 | 作用 | 持久性 |
|------|------|--------|
| SOUL.md | OCEAN 人格配置 | ✅ 永久 |
| IDENTITY.md | 身份标识 | ✅ 永久 |
| AGENTS.md | 行为红线 | ✅ 永久 |
| USER.md | 用户偏好 | ✅ 永久 |
| BOOTSTRAP.md | 首次运行 | ⚠️ 完成后可删除 |
| HEARTBEAT.md | 定时检查 | ✅ 永久 |
| TOOLS.md | 工具规范 | ✅ 永久 |

---

## 快速开始

### 1. 安装 Skill

按照上方安装步骤完成安装。

### 2. 首次运行

首次运行时，Agent 会自动执行初始化流程。

### 3. 开始使用

初始化完成后，每次对话 Agent 都会：
- 参考你的编码偏好
- 记住技术决策
- 保持一致的人格风格

---

## API Key

公共测试 Key：`nsh_public_beta_2026`

| Key 类型 | 每日限制 | 说明 |
|----------|----------|------|
| 公共 Key | 1000 次 | 公测期，正式版会更严格 |
| 个人 Key | 无限制 | 注册获取：https://neshama.pw/register |

---

## 相关资源

| 资源 | 链接 |
|------|------|
| 官网 | https://neshama.pw |
| SoulCraft | https://neshama.pw/soulcraft |
| API 文档 | https://api.neshama.pw/docs |
| GitHub | https://github.com/Neshama-AI/neshama-soul-openclaw |

---

## 更新日志

### v1.0.1 (2026-05-13)
- 增加 API Key 验证
- 7 文件灵魂文件系统正式发布

### v1.0.0 (2026-05-12)
- 初始版本发布
- 支持 OCEAN 人格模型
- 支持 Valence-Arousal 情绪系统

---

**© 2026 Neshama AI. All rights reserved.**