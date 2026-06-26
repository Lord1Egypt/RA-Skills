# GitHub 智能代码审查与 CI/CD 自动化工作流

> 🚀 三技能协同：GitHub 信息获取 × AI 代码审查 × CI/CD 自动生成

## 📋 概述

本 Combo（技能组合）将三个顶级 Skill 无缝串联，打造**从代码审查到 CI/CD 自动化**的完整闭环工作流。

## 🎯 解决的问题

- ✅ PR/提交代码质量参差不齐，审查耗时耗力
- ✅ 团队缺乏统一的 CI/CD 规范，新项目搭建工作流繁琐
- ✅ 安全问题难以在合并前发现，线上事故频发
- ✅ 代码审查与 CI/CD 工作流割裂，无法形成闭环

## 🔧 技能组成

| 技能 | 用途 | 特点 |
|------|------|------|
| **github** | 读取仓库、PR、提交信息 | 官方 `gh` CLI，稳定可靠 |
| **quack-code-review** | AI 代码审查（bug/安全/逻辑） | LogicArt AI 驱动，准确率高 |
| **github-actions-generator** | 智能生成 GitHub Actions 工作流 | 支持多语言/多场景 |

## 📖 工作流详解

```
[开发者提交 PR]
       ↓
阶段一：github 获取 PR 详情与变更文件
       ↓
阶段二：quack-code-review AI 深度审查
  ├─ Bug 检测
  ├─ 安全漏洞扫描
  ├─ 逻辑问题分析
  └─ 代码质量评分
       ↓
阶段三：github-actions-generator 生成工作流
  ├─ 基础 CI（lint/test/build）
  ├─ 安全扫描（如发现问题）
  └─ CD 部署（如适用）
       ↓
[自动将审查报告和工作流建议写入 PR 评论]
```

## 🚀 快速开始

### 方式一：完整流程（推荐）

```
用户输入：帮我审查并为 https://github.com/owner/repo/pull/123 生成 CI/CD
```

Agent 将自动执行：
1. `gh pr view 123 --repo owner/repo` 获取 PR 信息
2. `quack-code-review` 分析代码变更
3. `github-actions-generator` 生成工作流文件
4. 将报告写入 PR 评论

### 方式二：仅代码审查

```
用户输入：review 这个 PR https://github.com/owner/repo/pull/456
```

### 方式三：仅生成 CI/CD

```
用户输入：为我的 Node.js 项目生成 GitHub Actions CI 工作流
```

## 📂 生成的典型文件结构

```
.github/
└── workflows/
    ├── ci.yml          # 主 CI：lint → test → build
    ├── security.yml     # 安全扫描（如有安全问题）
    └── cd.yml          # 部署（如适用）
```

## ⚙️ 前置要求

- `gh` CLI 已安装并认证：`gh auth login`
- 仓库拥有者已安装 `quack-code-review`
- 仓库拥有者已安装 `github-actions-generator`

## 🌍 适用场景

- 🏢 企业内部代码审查流程自动化
- 🧑‍💻 开源项目维护者日常 PR 审查
- 🚀 新项目 CI/CD 快速搭建
- 🔒 安全合规要求严格的项目

## 📊 效果对比

| 对比项 | 手动操作 | 本工作流 |
|--------|----------|----------|
| 审查时间 | 30-60 分钟 | < 5 分钟 |
| 覆盖率 | 依赖审查者经验 | 全面标准化 |
| CI/CD 搭建 | 1-2 天 | < 30 分钟 |
| 安全问题发现 | 上线后才发现 | 合并前发现 |

## 🔗 相关资源

- GitHub CLI: https://cli.github.com/
- quack-code-review: https://clawhub.com/skills/quack-code-review
- github-actions-generator: https://clawhub.com/skills/github-actions-generator

---

**维护者**：OpenClaw Agent  
**版本**：1.0.0  
**标签**：github · code-review · cicd · github-actions · automation · devops
