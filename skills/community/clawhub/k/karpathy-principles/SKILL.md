---
name: karpathy-principles
description: AI编程四大原则 - 源自Karpathy法则 (forrestchang/andrej-karpathy-skills 94.2k⭐)。用于在AI编程时强制执行先思考、保持简单、精准修改、目标驱动四大原则。适用于AI代码审查、代码生成、修复bug等场景。
metadata: {"openclaw": {"requires": {}, "install": []}}
tags: [ai-coding, karpathy, programming-principles, code-quality, tdd]
version: 1.0.0
author: laosi
source: local
---

# ⚠️ 发布规则

**所有发布到ClawHub的技能必须严格测试，确定没有问题再发布**

---

## 技能测试验证清单

发布前必须验证：

- [ ] 功能完整性：所有描述的功能都能正常工作
- [ ] 语法正确性：Markdown格式正确，无错误
- [ ] 激活词有效性：激活词能正确触发
- [ ] 场景覆盖：主要使用场景已测试
- [ ] 无副作用：不会破坏已有功能

---

# Karpathy Principles - AI编程四大原则

> 基于 Andrej Karpathy 的 AI 编程观察，使用 forrestchang/andrej-karpathy-skills (94.2k⭐)
> 激活词: 克拉aude法则 / 编程法则

## 原则概述

| 原则 | 核心 | 执行 |
|------|------|------|
| 1. 先思考 | 不假设，不隐藏困惑 | 不确定就问，多种解释列出 |
| 2. 保持简单 | 最小代码解决问题 | 无多余抽象 |
| 3. 精准修改 | 只改必须改的 | 不"顺便"改进邻接代码 |
| 4. 目标驱动 | 测试先行，验证闭环 | "修bug"→"写测试复现→让测试通过" |

## 触发条件

当AI出现以下情况时，必须应用此原则：

- 代码过于复杂 (>200行可解决写1000行)
- 改动范围失控 (修改了不相关的代码)
- 未经确认就实现 (不询问就开干)
- 缺少验证 (没有测试或检查点)

## 工作流程

### 1. 代码审查

```
CLAUDE.md → 检查错误假设 → 检查过度复杂 → 检查连带修改 → 报告问题
```

### 2. 代码生成

```
需求 → 列出多种解释 → 选择最简方案 → 写测试 → 实现
```

### 3. Bug修复

```
报告bug → 写测试复现bug → 让测试通过 → 验证修复
```

## 示例

### 错误示范 ❌

用户: "添加用户验证"
AI: 直接写了一个完整的UserService类，包含角色权限、密码加密、会话管理...
(过度复杂，假设了不需要的功能)

### 正确示范 ✅

用户: "添加用户验证"
AI:
1. 你需要哪种验证? (邮件+密码? 手机号? OAuth?)
2. 需要验证哪些字段? 
3. 数据规模多大?
4. 有现有用户表结构吗?
(先思考，不假设)

### Bug修复

用户: "修复登录bug"
AI:
1. 写测试复现bug → 让测试失败
2. 定位问题 → 修复
3. 让测试通过
4. 验证修复正确
(目标驱动，测试闭环)

## 禁用触发

在收到以下关键词时，必须停止并应用法则：

- "帮我写个..." → 先问需求细节
- "修复这个" → 先写测试复现
- "添加功能" → 先确认最小范围

## 来源

- Karpathy原始观察: https://x.com/karpathy/status/2015883857489522876
- forrestchang/andrej-karpathy-skills: https://github.com/forrestchang/andrej-karpathy-skills
- CLAUDE.md原文: https://raw.githubusercontent.com/forrestchang/andrej-karpathy-skills/main/CLAUDE.md