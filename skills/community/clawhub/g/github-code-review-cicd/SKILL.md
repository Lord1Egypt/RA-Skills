---
name: github-code-review-cicd
description: |
  GitHub 智能代码审查与 CI/CD 自动化完整工作流。
  场景：收到 PR 或提交代码时，自动完成 AI 代码审查（bug/安全/逻辑问题），
  并根据审查结果智能生成或推荐 GitHub Actions CI/CD 工作流。
  触发词：代码审查、review PR、生成 CI/CD、GitHub Actions 自动生成、代码质量检查。
skills:
  - source: github
    purpose: 读取仓库信息、PR 详情、提交记录、Issue 列表
  - source: quack-code-review
    purpose: AI 代码审查，检测 bug、安全漏洞、逻辑问题，给出修复建议
  - source: github-actions-generator
    purpose: 根据语言/框架/审查结果智能生成 GitHub Actions 工作流
version: 1.0.0
author: openclaw-agent
tags:
  - github
  - code-review
  - cicd
  - github-actions
  - automation
  - devops
---

# GitHub 智能代码审查与 CI/CD 自动化

## 技能简介

本技能是一个三阶段自动化工作流，专门用于**提升 GitHub 项目代码质量与 CI/CD 效率**。

## 工作流程

### 阶段一：GitHub 信息收集（github）

使用 `gh` CLI 获取仓库、PR 或提交的相关信息：

```bash
# 查看 PR 详情
gh pr view <pr-number> --repo <owner/repo> --json title,body,files,additions,deletions,author

# 获取 PR 变更文件列表
gh pr diff <pr-number> --repo <owner/repo>

# 查看最近提交记录
gh api repos/<owner>/<repo>/commits?per_page=10

# 列出仓库所有 Actions 工作流
gh workflow list --repo <owner/repo>
```

收集以下上下文信息：
- PR 标题、描述、作者
- 变更文件列表（新增/修改/删除）
- 代码行数统计
- 当前 CI 状态

### 阶段二：AI 代码审查（quack-code-review）

对收集到的代码变更进行深度 AI 审查：

1. **Bug 检测**：空指针、边界条件、异常处理不当
2. **安全漏洞**：注入风险、敏感信息泄露、不安全依赖
3. **逻辑问题**：业务逻辑错误、状态机问题、并发安全问题
4. **代码质量**：风格不一致、重复代码圈复杂度
5. **最佳实践**：现代语言特性使用、错误处理规范

输出格式：
```
## 🔍 代码审查报告

### 🔴 严重问题（必须修复）
- [文件:行号] 问题描述
- 修复建议

### 🟡 建议改进
- [文件:行号] 问题描述
- 修复建议

### ✅ 审查通过
- 通过检查项列表

### 📊 统计
- 文件数: X | 新增: +X | 删除: -X
- 严重: X | 建议: X
```

### 阶段三：智能 CI/CD 生成（github-actions-generator）

根据阶段二的审查结果与项目技术栈，自动生成 GitHub Actions 工作流：

**生成策略：**
- Node.js/TypeScript → `node.yml`：安装 → lint → test → build
- Python → `python.yml`：安装依赖 → pytest → 覆盖率报告
- Go → `go.yml`：构建 → 测试 → 多平台构建
- Docker 项目 → `docker.yml`：构建 → 推送镜像 → 安全扫描
- 审查发现问题 → 在工作流中增加对应检查步骤（如安全扫描、代码覆盖率阈值）

**生成的文件：**
- `.github/workflows/ci.yml` — 主 CI 工作流
- `.github/workflows/security.yml` — 安全扫描（发现安全问题启用）
- `.github/workflows/cd.yml` — 部署工作流（如适用）

**使用说明：**
```bash
# 生成 Node.js CI 工作流
github-actions-generator --lang node --framework express

# 生成带安全扫描的 Python CI 工作流
github-actions-generator --lang python --security-scan --coverage

# 生成 Docker 构建+推送工作流
github-actions-generator --lang docker --registry ghcr.io
```

## 使用场景

| 场景 | 输入 | 输出 |
|------|------|------|
| PR Code Review | PR 链接或 `owner/repo#pr-number` | 审查报告 + PR 评论 |
| 提交审查 | 提交 SHA 或 commit message | 审查报告 |
| 新项目 CI 搭建 | 仓库 URL + 技术栈 | 完整 CI/CD 工作流 |
| 安全合规检查 | 仓库 URL | 安全扫描报告 + 修复建议 |

## 依赖工具

- `gh` CLI（GitHub 官方命令行工具）
- `quack-code-review`（LogicArt AI 代码分析）
- `github-actions-generator`（Sunshine-Del 团队出品）

## 最佳实践

1. **每次提交必审查**：配合 GitHub Actions 自动触发，在代码合并前发现问题
2. **审查结果写入 PR 评论**：使用 `gh pr comment` 将报告自动写入 PR
3. **CI 工作流渐进生成**：先审查再生成，确保工作流覆盖已有问题
4. **安全优先**：发现安全漏洞时，自动启用 `security.yml` 工作流

## 注意事项

- 审查报告仅作为辅助建议，最终决策由开发者负责
- 生成的 CI/CD 工作流需根据实际项目需求调整
- 敏感信息（如密钥、Token）不要在审查报告中暴露
