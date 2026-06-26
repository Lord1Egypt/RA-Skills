---
name: github-health-diagnosis
description: GitHub 项目健康度诊断 — 输入仓库地址，AI 自动分析 Issues、代码质量、CI状态，生成诊断报告并发布到飞书 Wiki。
category: 开发
triggers: 项目诊断, GitHub健康度, 代码质量报告, 仓库诊断, 项目报告, 质量评估
version: 1.0.0
author: OpenClaw Agent
tags:
  - github
  - code-review
  - feishu-wiki
  - card-renderer
  - devops
  - health-check
  - automation
combo: true
channels:
  - feishu
dependencies:
  - github
  - code-review-skill
  - card-renderer
  - feishu-wiki
---

# GitHub 项目健康度诊断助手

一条命令完成：**仓库数据抓取 → Issues 分析 → 代码质量审查 → CI/CD 状态检查 → 诊断报告卡片生成 → 飞书 Wiki 发布**。

## 核心价值

- **一键诊断**：只需提供一个 GitHub 仓库地址，5分钟内生成完整健康度报告
- **AI 代码审查**：集成专业代码审查 Skill，多维度评估代码质量
- **可视化呈现**：生成诊断卡片，团队一眼看懂项目健康状态
- **知识沉淀**：诊断报告自动发布到飞书 Wiki，便于存档和分享

## 适用场景

- 技术负责人接新项目，快速了解代码库健康状况
- 团队代码质量管理，定期生成健康度报告
- 开源项目维护者定期自检
- 尽职调查 / Due Diligence 场景下的代码质量评估
- CI/CD 流水线异常后的根因分析辅助

## 工作流程（5步）

```
Step 1 → github
   │   获取仓库基本信息（Stars、Fork、Watch、开放 Issues 数量）
   │   获取最近 30 条 Issues 和 PR 列表
   │   获取最新 Commits 和贡献者信息
   ↓
Step 2 → github (代码审查)
   │   对仓库主要代码文件进行语法/逻辑分析
   │   通过 code-review-skill 执行多维度审查
   ↓
Step 3 → code-review-skill
   │   输出：代码质量评分 / 问题列表 / 安全风险 / 性能建议
   │   汇总为结构化诊断数据
   ↓
Step 4 → card-renderer
   │   生成诊断摘要封面卡（雷达图式健康度展示）
   │   生成详情页卡片（分维度评分 + 问题列表）
   ↓
Step 5 → feishu-wiki
   │   将诊断报告发布为飞书 Wiki 页面
   │   包含：项目概览 / 健康度评分 / 问题详情 / 修复建议
```

## 使用方法

### 触发词

```
"诊断项目健康度 [仓库地址]"
"帮我看看这个GitHub项目的质量"
"仓库健康检查 [owner/repo]"
"生成项目诊断报告"
"这个项目代码质量怎么样"
"GitHub项目健康度分析"
```

### 输入格式

```
诊断项目健康度 https://github.com/owner/repo
或
诊断项目健康度 owner/repo
```

### 输出

- **飞书 Wiki 页面链接**：完整诊断报告（含评分、问题列表、修复建议）
- **诊断卡片图片**：封面卡 + 详情卡，可直接分享

## 诊断维度（5大维度，满分100）

| 维度 | 权重 | 评估内容 |
|------|------|---------|
| 代码质量 | 30% | 规范遵循、复杂度、注释覆盖率 |
| Issue 活跃度 | 20% | Issue 响应速度、Open Issues 积压量 |
| CI/CD 状态 | 20% | Workflow 通过率、测试覆盖率 |
| 社区活跃度 | 15% | Stars 增长、PR 合并速度、贡献者数量 |
| 安全风险 | 15% | 依赖漏洞、敏感信息泄露风险 |

## 健康度评级

- 🟢 **90-100**：优秀 — 项目运行良好
- 🟡 **70-89**：良好 — 有少量可改进项
- 🟠 **50-69**：一般 — 存在较多问题需关注
- 🔴 **0-49**：危险 — 需立即介入处理

## 示例报告结构

```
📊 GitHub 项目健康度诊断报告
仓库：facebook/react
诊断时间：2026-04-21

🏆 综合评分：92/100 🟢 优秀

各维度评分：
  代码质量      ████████████ 95/100
  Issue 活跃度  █████████░░░ 85/100
  CI/CD 状态    ████████████ 98/100
  社区活跃度    ████████████ 96/100
  安全风险      █████████░░░ 88/100

📋 主要问题：
  1. [中等] 部分组件缺少 TypeScript 类型定义
  2. [低]  少数工具函数缺少 JSDoc 注释

💡 改进建议：
  1. 建议补充 Props 的 PropTypes 或 TypeScript 类型
  2. 建议对核心工具函数添加 JSDoc 注释提升可维护性
```
