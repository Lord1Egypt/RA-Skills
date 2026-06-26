---
name: pr-quality-gate
description: Code Review + AI 修复 + GitHub Issue 追踪的 PR 质量门禁工作流，确保代码合入前经过系统性 Review。
category: 开发
triggers: review pr, PR质量检查, 代码审查, PR通过条件, 检查PR
---

# PR Quality Gate

代码合并前的系统性质量门禁工作流，自动完成 Code Review → 问题修复 → Issue 追踪的完整闭环。

## 工作原理

当收到 PR Review 请求时，按顺序执行以下 Skill：

1. **code-review** → 读取 PR diff，分析代码质量维度，输出 Review 报告
2. **github-issues** → 发现 Bug 或 Feature 建议时，自动创建 Issue 并关联 PR
3. **kimi-cli / giga-coding-agent** → 高优先级问题触发 AI Coding Agent 修复建议
4. **github** → 最终通过 `gh pr merge` 或带条件合并

## 触发方式

在对话中提及以下关键词即触发：
- "review 这个 PR"
- "帮我 review PR#123"
- "检查这个 pull request"
- "PR 质量 Gate"
- "merge 前检查"

## 使用示例

```
用户：review github.com/owner/repo/pull/456
↓ 激活 pr-quality-gate
↓ code-review: 拉取 diff，分析质量维度（逻辑/安全/性能/可读性/测试）
↓ 发现 2 个 Medium 问题，1 个 High 问题
↓ github-issues: 自动创建 3 个关联 Issue
↓ 高优先级问题触发 kimi-cli 修复建议
↓ 输出 Review 报告 + 关联 Issue 列表
```

## 输出格式

### Review 报告

```
## PR Quality Gate Report

**PR:** owner/repo#456 — "feat: 新增支付模块"

### 质量评分
- 逻辑正确性: ⭐⭐⭐⭐☆ (4/5)
- 安全性:      ⭐⭐⭐⭐⭐ (5/5)
- 性能:        ⭐⭐⭐☆☆ (3/5)
- 可读性:      ⭐⭐⭐⭐☆ (4/5)
- 测试覆盖:    ⭐⭐☆☆☆ (2/5)

### 问题汇总
| # | 严重度 | 位置 | 问题描述 | 状态 |
|---|--------|------|----------|------|
| 1 | High   | payment.js:23 | 未做空值校验 | 🔴 Open |
| 2 | Medium | auth.py:45 | 硬编码密钥应从 env 读取 | 🟡 Open |
| 3 | Medium | utils.js:12 | 重复计算可缓存 | 🟡 Open |

### 关联 Issue
- #issue 123: payment.js:23 空值校验缺失
- #issue 124: auth.py:45 密钥硬编码
- #issue 125: utils.js:12 性能优化

### 建议
✅ 可以合并（条件：通过所有 High 问题）
⚠️ 阻塞：Issue #123 未解决前不建议合并
```

## 质量维度

| 维度 | 检查内容 |
|------|----------|
| 逻辑正确性 | 边界条件、异常处理、核心算法 |
| 安全性 | 注入风险、认证授权、敏感数据 |
| 性能 | N+1 查询、不必要的循环、内存泄漏 |
| 可读性 | 命名规范、注释完整性、函数长度 |
| 测试覆盖 | 单元测试、集成测试、边界用例 |

## 与其他 Skill 的关系

```
pr-quality-gate 编排以下 Skill：

code-review        核心：结构化 Code Review 流程
github-issues     发现问题时创建 Issue 并关联 PR
kimi-cli          High 严重度问题触发 AI 修复建议
github            最终执行 gh pr merge / 评论
```

## 注意事项

- 本 Skill 不会自动合并 PR，最终合并操作由用户确认
- High 严重度问题未解决时，会阻止合入建议
- 涉及密钥、密码等敏感信息的硬编码问题自动标记为 High