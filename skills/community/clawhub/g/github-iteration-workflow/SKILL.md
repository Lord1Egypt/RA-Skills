---
name: github-iteration-workflow
description: GitHub Issue 全流程自动化处理。当用户要求处理 GitHub Issue、拉取并修复 Issue、创建 PR、监控 CI/CD、合并部署时使用此技能。涵盖从 Issue 拉取、代码修复、PR 创建、CI/CD 监控到合并部署的完整自动化流程。
---

# GitHub Issue 全流程自动化

从拉取 Issue 到合并部署的端到端自动化工作流。

## 前置条件

- GitHub CLI 已认证（`gh auth status` 正常）
- 仓库已克隆到本地
- 有仓库的 push 权限

## 工作流

### 1. 拉取所有 Open Issue

```bash
cd <repo-path>
gh issue list --state open
```

批量获取所有需要处理的 Issue 详情：

```bash
# 获取所有 open issue 的编号和标题
gh issue list --state open --json number,title,body
```

### 2. 统一分析所有 Issue

一次性获取所有 open issue，整体评估：

```bash
gh issue list --state open --json number,title,body,labels
```

**分析要点：**
- 哪些 Issue 相关（同一模块、同一文件、同一类问题）
- 是否存在依赖关系（A 修了影响 B）
- 能否合并为一次修复（相关 Issue 放同一分支）

**输出一份修复计划：** 分组 → 确定分支策略 → 明确每个 Issue 对应的改动

### 3. 整体修复

基于分析结果，创建分支并一次性实现所有修复：

```bash
git checkout master && git pull origin master
git checkout -b fix/batch-<date>-<总体描述>
```

**修复策略：**
- 用一个子代理传入所有 Issue 描述 + 项目上下文，让它整体规划后统一修改
- 相关 Issue 合并处理，减少重复改动
- 每个 Issue 的修复在同一分支内用独立 commit 区分

### 4. 分 commit 提交推送

每个 Issue 单独一个 commit，便于追踪：

```bash
# 按 Issue 逐个提交
git add <files-for-issue-A>
git commit -m "fix: <issue-A描述> (#<A>)"

git add <files-for-issue-B>
git commit -m "fix: <issue-B描述> (#<B>)"
```

推送统一分支：

```bash
git push -u origin fix/batch-<date>-<总体描述>
```

### 5. 创建一个 PR 关联所有 Issue

```bash
gh pr create \
  --title "Batch fix: <总体描述>" \
  --body "## 关联 Issues

Closes #<A>, Closes #<B>, Closes #<C>

### Issue #<A>: <标题>
<修复说明>

### Issue #<B>: <标题>
<修复说明>

### Issue #<C>: <标题>
<修复说明>" \
  --base master
```

### 6. 监控 CI/CD

```bash
gh pr checks <PR-number>
```

**检查项：** Code Quality / Security Scan / Unit Tests / E2E Tests / Deploy Preview

**CI 失败自动修复：**
1. 查看失败日志：`gh run view <run-id> --log-failed`
2. 修复并推送：`git commit -am "fix: CI ..." && git push`
3. 重新检查直到通过

### 7. 合并并部署

CI 通过后合并：

```bash
gh pr merge <PR-number> --merge
# 分支保护时用 --admin
```

### 8. 验证部署并发送报告

```bash
gh api repos/<owner>/<repo>/deployments --jq '.[0:3] | .[] | "\(.environment) - \(.sha[0:7]) - \(.created_at)"'
```

**报告内容：**
- 每个 Issue 的编号、标题和修复说明
- PR 链接（一个 PR 覆盖所有 Issue）
- CI/CD 结果汇总
- 部署状态
- 修改文件列表

## 提交信息规范

- `fix:` 修复问题
- `feat:` 新功能
- `refactor:` 重构
- `docs:` 文档更新
- `style:` 代码格式
- `test:` 测试相关

## 分支命名规范

- `fix/issue-<n>-<desc>` — 修复
- `feat/issue-<n>-<desc>` — 新功能
- `refactor/issue-<n>-<desc>` — 重构
