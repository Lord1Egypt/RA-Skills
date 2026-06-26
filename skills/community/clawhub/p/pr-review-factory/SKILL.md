---
name: pr-review-factory
description: 自动化Code Review工厂 — GitHub PR审查全流程自动化，从提交到修复到合并，一站式质量门禁。
category: 开发
triggers: Code Review, PR审查, Pull Request审查, 代码审查, PR合并, GitHub质量门禁
version: 1.0.0
author: OpenClaw Agent
tags:
  - code-review
  - github
  - automation
  - CI/CD
  - devops
  - quality-gate
dependencies:
  - code-review-skill
  - github-issues-skill
  - github-actions-templates
---

# PR Review Factory（自动化 Code Review 工厂）

## 一句话定位

GitHub Pull Request 提交后，自动完成审查 → 问题记录 → 分派修复 → 验证通过 → 合并的全流程，零人工干预。

---

## 解决的问题

| 痛点 | 传统方式 | 本技能 |
|------|---------|--------|
| PR堆积 | 人工审查速度慢，积压严重 | 自动秒级启动审查 |
| 标准不一 | 每个人审查维度不同 | 结构化5维度审查（正确性/安全/可读/性能/可维护） |
| 问题跟踪难 | 审查意见散落在PR评论中 | 自动创建 GitHub Issues 跟踪每一个问题 |
| 修复无闭环 | 审查完不知道谁改、什么时候改 | Issues 分派责任人，状态驱动闭环 |
| 合并风险 | 没有质量门禁，随便合并 | 必须所有 Blocking 问题修复才可合并 |

---

## 工作流程（4步）

```
PR 创建/更新
    │
    ▼
Step 1: 结构化 Code Review（code-review-skill）
   • 5个独立维度审查：正确性 / 安全 / 可读 / 性能 / 可维护
   • 并行 Agents 独立审查，互不干扰
   • 输出审查结论：Approve / Request Changes / Comment Only
    │
    ▼
Step 2: 问题 Issue 化（github-issues-skill）
   • Blocking 问题 → 创建 Issue 并分派给 PR 作者
   • Suggestion 问题 → 作为 PR 评论保留
   • 每个 Issue 包含：问题描述 / 代码位置 / 修复建议 / 严重程度
    │
    ▼
Step 3: 修复验证循环（github-actions-templates）
   • 生成 CI 验证工作流（lint + test + build）
   • Issue 全部关闭后触发质量门禁检查
   • 自动合并通过审查的 PR
    │
    ▼
Step 4: 合并报告（github-actions-templates）
   • 生成本次审查摘要（问题数/修复时间/质量评分）
   • 记录到项目知识库（可选）
```

---

## 触发方式

| 触发词 | 执行内容 |
|--------|---------|
| `帮我审查这个PR` | 对指定PR进行完整审查流程 |
| `PR审查 xxx/repo#123` | 指定仓库的指定PR审查 |
| `建立PR质量门禁` | 为仓库配置完整的自动化审查工作流 |
| `审查并记录` | 审查PR并自动创建Issue跟踪 |
| `查看PR审查状态` | 查询当前PR的审查进度和Issue状态 |

---

## 快速使用

### 方式一：审查指定 PR

```bash
# 直接审查 PR（格式：owner/repo#pr_number）
启动 code-review-skill，对 GitHub PR 进行结构化审查

示例：
  输入：帮我审查 flutter/flutter#45231
  执行：5维度并行审查 → 输出审查报告
```

### 方式二：创建质量门禁工作流

```bash
启动 github-actions-templates，生成自动化 PR 审查 CI 工作流
  • lint 检查
  • 单元测试
  • 构建验证
  • 审查报告生成
```

### 方式三：问题跟踪与分派

```bash
启动 github-issues-skill
  • 将审查问题创建为 Issue
  • 自动分派给 PR 作者
  • 设置 Milestone 跟踪
  • 修复后自动关闭 Issue
```

---

## 技术架构

| 层级 | 组件 | 职责 |
|------|------|------|
| 审查层 | code-review-skill | 并行5维度Code Review，结构化输出 |
| 跟踪层 | github-issues-skill | 审查问题Issue化，责任分派，状态跟踪 |
| CI层 | github-actions-templates | 自动化CI工作流，质量门禁，合并控制 |
| 编排层 | pr-review-factory | 整体流程编排，状态驱动，结果汇总 |

---

## 审查维度说明

| 维度 | 审查内容 | 严重程度 |
|------|---------|---------|
| 正确性 | 逻辑错误、空指针、边界条件 | 🔴 Blocking |
| 安全性 | 注入风险、敏感信息泄露、依赖漏洞 | 🔴 Blocking |
| 可读性 | 命名规范、注释完整、函数长度 | 🟡 Suggestion |
| 性能 | 复杂度、N+1查询、不必要的循环 | 🟡 Suggestion |
| 可维护 | 重复代码、耦合度、测试覆盖 | 🟡 Suggestion |

---

## 注意事项

1. 首次使用需配置 GitHub Token 环境变量（`GITHUB_TOKEN`）
2. 自动化合并需要仓库管理员权限或 Branch Protection 配置
3. 大型 PR（>1000行）建议拆分成多个小 PR 后再审查
4. Draft PR 默认跳过自动审查，可手动触发
5. 建议配合 Branch Protection 使用，确保审查通过后才能合并

---

## 工作流示例

```
用户: 帮我审查 facebook/react#54321
AI:
  → 启动 code-review-skill，拉取 PR 变更
  → 启动 5 个并行审查 Agent
  → 发现 3 个 Blocking 问题，2 个 Suggestion
  → 启动 github-issues-skill，创建 3 个 Issue 并分派
  → 启动 github-actions-templates，配置 CI 验证工作流
  → 审查报告：2 Blocking 待修复，1 Suggestion 可选
```