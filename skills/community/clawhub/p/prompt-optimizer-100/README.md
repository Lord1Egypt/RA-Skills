# Prompt 优化系统 Skill

> 让 AI 自动完成专业级 Prompt 重构，用户说人话即可

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://clawhub.ai/skills/prompt-optimizer)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-%3E%3D2026.3.8-green.svg)](https://openclaw.ai)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 快速开始

### 安装

```bash
openskills install prompt-optimizer-100
```

> **注意**：clawhub.ai 上的 slug 为 `prompt-optimizer-100`，安装时请使用完整名称。

### 测试

```bash
# L1 测试
写一篇 300 字文章

# L2 测试
调研一下竞品

# L3 测试
技术选型方案

# L4 测试
生成客户方案 PPT
```

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **需求分级** | 自动判断 L1-L4 任务等级 |
| **Prompt 优化** | 5 维度重构（角色/背景/任务/约束/示例） |
| **Agent 路由** | 单 Agent / 多 Agent 并行 |
| **执行保障** | 自检清单 + Badcase 闭环 |
| **Merge 模式** | 保留用户原有规则，增量更新 |

---

## 文档

- [安装指南](SKILL.md)
- [核心规则](rules/prompt-optimization.md)
- [回复模板](templates/response-templates.md)
- [完整设计文档](https://feishu.cn/docx/He9Gdnpd4oTydyxSAZYcVQ1dnTc)

---

## 发布到 ClawHub

```bash
# 打包
openskills pack prompt-optimizer

# 发布到 clawhub.ai
openskills publish prompt-optimizer --target clawhub.ai
```

---

## License

MIT License
