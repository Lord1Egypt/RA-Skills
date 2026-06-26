---
name: pr-doctor
description: PR全流程质量医生 — 自动化代码审查、测试分析、问题追踪和持续改进的完整流水线
category: 开发
triggers: 审查PR, PR质量检查, 代码审查, 代码质量报告, PR健康检查, review PR, 检查我的PR, 代码审查流水线
---

# PR Doctor - PR全流程质量医生

## 概述

PR Doctor 是一个完整的 Pull Request 质量保障流水线，同时调用多个专业 Skill 完成从代码审查到问题追踪的全流程。

**解决问题**：开发者花费大量时间手动审查 PR，人工追踪问题和跟进效率低下。

## 核心工作流

```
[PR URL/Repo] 
    │
    ├─→ code-review-skill    (代码审查 + 质量评分)
    │
    ├─→ testing-patterns     (测试覆盖分析 + 建议)
    │
    ├─→ github-issues-skill  (自动创建跟进issue)
    │
    └─→ self-improvement     (记录学习，持续改进)
            │
            ▼
      [综合审查报告]
```

## 使用方法

### 触发词
- `审查PR <PR_URL>`
- `PR质量检查 <owner/repo> <PR号>`
- `检查我的PR`
- `PR健康检查`

### 输入
提供以下任一信息：
- PR URL，例如：`https://github.com/owner/repo/pull/123`
- 或提供：`owner/repo` + PR 编号

### 执行流程

**Step 1: 代码审查**
调用 `code-review-skill`，使用 `gh pr diff` 获取 PR 差异，逐文件审查：
- 代码逻辑问题
- 安全漏洞
- 性能隐患
- 代码风格
- 边界条件

**Step 2: 测试覆盖分析**
调用 `testing-patterns`，分析：
- 新增代码的测试覆盖情况
- 是否有测试缺失的关键路径
- 是否违反 TDD 原则
- 测试命名和结构质量

**Step 3: 创建跟进 Issue**
调用 `github-issues-skill`，对于每个发现的问题：
- 按严重程度分级（critical/major/minor）
- 自动创建 GitHub Issue 描述问题
- 添加适当的标签（bug, security, performance, style）
- 关联到原始 PR

**Step 4: 持续改进**
调用 `self-improvement`：
- 记录本次审查中发现的新型问题模式
- 更新质量检查清单
- 促进后续审查效率提升

### 输出
综合审查报告，包含：
- PR 总体质量评分（1-10）
- 问题清单（按严重程度排序）
- 测试覆盖评估
- 建议行动项
- 相关 GitHub Issue 链接

## 质量评分标准

| 评分 | 等级 | 说明 |
|------|------|------|
| 9-10 | 🟢 Excellent | 可直接合并 |
| 7-8 | 🔵 Good | 小问题修复后可合并 |
| 4-6 | 🟡 Needs Work | 需要重大修改 |
| 1-3 | 🔴 Poor | 建议重新设计 |

## 审查维度

### 代码审查 (code-review-skill)
- ✅ 逻辑正确性
- ✅ 安全漏洞检测
- ✅ 性能影响评估
- ✅ 错误处理完整性
- ✅ 代码可读性
- ✅ 边界条件覆盖

### 测试分析 (testing-patterns)
- ✅ 测试覆盖率
- ✅ 边界条件测试
- ✅ Mock/Stub 使用合理性
- ✅ 测试命名描述性
- ✅ 测试结构（AAA模式）
- ✅ 回归测试完整性

## 示例对话

**用户**：`审查这个PR: https://github.com/owner/project/pull/42`

**AI**：正在启动 PR Doctor 流水线...
> 🔍 Step 1: 代码审查中...
> 📊 Step 2: 测试覆盖分析中...
> 📋 Step 3: 创建跟进Issue中...
> 📚 Step 4: 记录学习点...
> ✅ 审查完成！

**综合报告**：
- 质量评分：7.5/10 🟢
- 发现问题：3个（1个Critical, 2个Minor）
- 测试覆盖：良好，缺失边界测试
- 已创建Issue：#143, #144
- 建议：修复 Critical 问题后合并

## 注意事项

- 使用 `gh` CLI 进行 GitHub API 调用，需要先完成 `gh auth login`
- 代码审查为辅助性质，最终决策由人工做出
- 创建 Issue 前先搜索是否已有重复问题
- self-improvement 日志保存在 `.learnings/` 目录
