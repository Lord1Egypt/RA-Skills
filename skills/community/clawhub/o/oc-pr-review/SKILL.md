---
name: pr-review
description: "PR 审查技能 — 完整的 Pull Request 审查流程，集成 GitHub CLI，支持安全分析、测试覆盖、性能评估、代码质量检查，并可推送飞书通知。Use when: (1) 审查 PR，(2) 检查 PR 安全性，(3) 分析测试覆盖，(4) 评估代码质量，(5) 生成审查报告。触发词：'review PR', '审查PR', '代码审查', 'pr review', '检查PR'。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["gh"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "gh",
              "bins": ["gh"],
              "label": "Install GitHub CLI (brew)",
            },
          ],
      },
  }
---

# PR Review Skill

完整的 Pull Request 审查工作流，涵盖安全分析、测试覆盖、性能评估、代码质量检查。

## When to Use

✅ **USE this skill when:**

- 审查 Pull Request 的代码变更
- 检查 PR 的安全漏洞和风险
- 分析测试覆盖情况
- 评估代码变更的性能影响
- 生成审查报告并通知到飞书

❌ **DON'T use this skill when:**

- 本地 git 操作（commit、push、pull）→ 直接用 `git`
- 非 GitHub 仓库（GitLab、Bitbucket）→ 不同的 CLI
- 简单查看 PR 状态 → 直接用 `gh pr view`
- 写代码或修复 → 用 `coding-agent` skill

## Prerequisites

```bash
# 确认 gh 已认证
gh auth status

# 如果未认证，执行
gh auth login
```

## 审查流程（6 步）

```
Step 1: 获取 PR 信息
    ↓
Step 2: 分析变更内容
    ↓
Step 3: 安全审查
    ↓
Step 4: 测试覆盖检查
    ↓
Step 5: 性能 & 质量评估
    ↓
Step 6: 生成报告 + 飞书通知
```

---

## Step 1: 获取 PR 信息

### 确定 PR 目标

用户可能提供以下格式之一：
- PR URL: `https://github.com/owner/repo/pull/123`
- PR 编号: `#123`（需要在 git 仓库中）
- 分支名: `feature/xxx`（需查找对应的 PR）

```bash
# 从 URL 解析
# owner/repo: 从 URL 提取
# pr_number: 从 URL 提取

# 获取 PR 详情
gh pr view <pr_number> --repo <owner/repo> --json title,body,author,state,additions,deletions,changedFiles,files,reviews,comments,labels,mergeable,headRefName,baseRefName

# 获取 PR 的文件变更列表
gh pr diff <pr_number> --repo <owner/repo> --stat

# 获取完整 diff
gh pr diff <pr_number> --repo <owner/repo>
```

### 如果用户只提供了分支名

```bash
# 查找分支对应的 PR
gh pr list --repo <owner/repo> --head <branch_name> --json number,title
```

### 如果在 git 仓库内且未指定 PR

```bash
# 获取当前分支的 PR
gh pr view --json number,title,body,state
```

---

## Step 2: 分析变更内容

获取 diff 后，按以下维度分析：

### 变更概览

```
📊 变更概览
- 文件数: X 个文件变更
- 新增: +X 行
- 删除: -X 行
- 涉及模块: [列出模块/目录]
```

### 文件分类

将变更文件分为以下类别：

| 类别 | 说明 | 关注点 |
|------|------|--------|
| 🔐 安全相关 | auth、crypto、permission、config | 注入、暴露、权限绕过 |
| 🧪 测试文件 | test、spec、__tests__ | 覆盖率、边界用例 |
| 📦 依赖变更 | package.json、requirements.txt | 版本锁定、已知漏洞 |
| 🏗️ 核心逻辑 | 业务代码、API、数据库 | 逻辑正确性、性能 |
| 📝 文档 | README、docs | 是否同步更新 |
| ⚙️ 配置 | CI/CD、Dockerfile、环境变量 | 安全配置、敏感信息 |

---

## Step 3: 安全审查

对每个变更文件检查以下安全维度：

### 安全检查清单

```markdown
🔐 安全审查

**认证/授权 (Auth)**
- [ ] 是否有未授权的端点暴露？
- [ ] 权限检查是否完整？
- [ ] Token/Session 处理是否安全？

**数据暴露 (Data Exposure)**
- [ ] 是否有敏感数据泄露到日志？
- [ ] API 响应是否暴露内部信息？
- [ ] 错误消息是否泄露系统细节？

**注入风险 (Injection)**
- [ ] SQL 注入：是否使用参数化查询？
- [ ] XSS：用户输入是否正确转义？
- [ ] 命令注入：是否有未经验证的 shell 执行？
- [ ] 路径遍历：文件路径是否验证？

**加密与密钥 (Crypto)**
- [ ] 是否使用了弱加密算法？
- [ ] 密钥是否硬编码？
- [ ] 是否使用安全的随机数生成？

**依赖安全 (Dependencies)**
- [ ] 新增依赖是否有已知漏洞？
- [ ] 版本是否锁定？
- [ ] 是否引入了不必要的权限？
```

### 安全严重性分级

| 级别 | 标记 | 说明 | 处理 |
|------|------|------|------|
| 🔴 Critical | CRITICAL | 可被远程利用，影响数据安全 | **必须修复**才能合并 |
| 🟠 High | HIGH | 潜在安全风险，需要关注 | **建议修复**后合并 |
| 🟡 Medium | MEDIUM | 最佳实践问题 | 建议改进 |
| 🟢 Low | LOW | 代码风格/建议 | 可选改进 |

---

## Step 4: 测试覆盖检查

### 测试分析清单

```markdown
🧪 测试覆盖分析

**新增代码测试**
- [ ] 新增功能是否有对应测试？
- [ ] 测试是否覆盖正常流程？
- [ ] 测试是否覆盖异常/边界用例？

**测试质量**
- [ ] 断言是否有意义（非 trivial assert）？
- [ ] 测试是否独立（无共享状态）？
- [ ] Mock/Stub 使用是否合理？

**回归测试**
- [ ] 修改的逻辑是否有回归测试？
- [ ] 是否破坏了现有测试？

**覆盖率评估**
- 关键路径覆盖率: __%
- 建议覆盖率目标: 80%+
```

### 测试建议模板

```markdown
## 🧪 测试建议

### 缺失测试
1. [文件路径] — [建议添加的测试]
2. ...

### 边界用例
1. [场景描述] — [建议的测试方法]
2. ...

### 测试改进
1. [现有测试] — [改进建议]
```

---

## Step 5: 性能 & 质量评估

### 性能检查

```markdown
⚡ 性能评估

**算法复杂度**
- [ ] 是否有 O(n²) 或更高复杂度的操作在热点路径？
- [ ] 是否有不必要的嵌套循环？

**数据库/IO**
- [ ] 是否有 N+1 查询问题？
- [ ] 是否有不必要的全表扫描？
- [ ] 文件操作是否有适当的缓冲？

**内存使用**
- [ ] 是否有内存泄漏风险？
- [ ] 大数据集是否分页/流式处理？

**缓存**
- [ ] 是否应该缓存的结果未缓存？
- [ ] 缓存失效策略是否正确？
```

### 代码质量

```markdown
📝 代码质量

**可读性**
- [ ] 命名是否清晰、一致？
- [ ] 函数/方法是否职责单一？
- [ ] 是否有过度复杂的条件逻辑？

**可维护性**
- [ ] 是否遵循项目的代码规范？
- [ ] 是否有重复代码可以提取？
- [ ] 错误处理是否完整？

**架构**
- [ ] 变更是否符合项目架构模式？
- [ ] 是否引入了不当的耦合？
- [ ] 是否有向后兼容性问题？
```

---

## Step 6: 生成报告 + 飞书通知

### 审查报告模板

```markdown
# 🔍 PR 审查报告

**PR**: #<number> — <title>
**作者**: @<author>
**分支**: <head> → <base>
**变更**: +<additions> -<deletions> (<changedFiles> 文件)

---

## 📊 总体评估: [✅ 通过 / ⚠️ 需修改 / ❌ 不建议合并]

### 🔐 安全: [✅/⚠️/❌]
- [发现摘要]

### 🧪 测试: [✅/⚠️/❌]
- 覆盖率: __%
- [发现摘要]

### ⚡ 性能: [✅/⚠️/❌]
- [发现摘要]

### 📝 代码质量: [✅/⚠️/❌]
- [发现摘要]

---

## 📋 详细发现

### 🔴 必须修复 (X)
1. [文件:行号] — [问题描述]

### 🟠 建议修复 (X)
1. [文件:行号] — [问题描述]

### 🟡 改进建议 (X)
1. [文件:行号] — [问题描述]

---

## ✅ 亮点
- [值得肯定的地方]
```

### 飞书通知

如果用户要求通知到飞书，使用 `message` 工具发送审查摘要：

```
发送对象: 用户指定的飞书群/个人
消息格式: 使用卡片或富文本格式
内容: 审查报告的精简版（总体评估 + 关键发现）
```

#### 飞书消息模板

```
🔍 PR 审查完成

PR: #<number> — <title>
作者: @<author>
总体评估: [✅/⚠️/❌]

🔐 安全: [✅/⚠️/❌]
🧪 测试: [✅/⚠️/❌] (覆盖率: __%)
⚡ 性能: [✅/⚠️/❌]
📝 质量: [✅/⚠️/❌]

关键发现:
• [发现1]
• [发现2]

详细报告: [链接或完整内容]
```

### 在 PR 中提交审查（可选）

```bash
# 提交审查评论
gh pr review <pr_number> --repo <owner/repo> --body "审查报告内容" --approve
# 或
gh pr review <pr_number> --repo <owner/repo> --body "审查报告内容" --request-changes
# 或
gh pr review <pr_number> --repo <owner/repo> --body "审查报告内容" --comment

# 对特定文件添加行级评论
gh api repos/<owner/repo/pulls/<pr_number>/comments \
  -f body="这里有个问题" \
  -f commit_id="<commit_sha>" \
  -f path="<file_path>" \
  -f line=<line_number>
```

---

## 快速审查模式

对于简单的 PR，可以跳过某些步骤：

### 快速安全审查

只执行 Step 1 → Step 3 → Step 6（跳过测试和性能分析）

### 快速测试审查

只执行 Step 1 → Step 4 → Step 6（跳过安全和性能分析）

---

## 使用示例

### 完整审查

```
用户: 帮我审查这个 PR https://github.com/myorg/myrepo/pull/42

Agent 执行:
1. gh pr view 42 --repo myorg/myrepo --json ...
2. gh pr diff 42 --repo myorg/myrepo
3. 分析变更 → 安全检查 → 测试检查 → 性能评估
4. 生成审查报告
5. (可选) 发送到飞书通知
```

### 安全审查

```
用户: 检查这个 PR 有没有安全问题 #15

Agent 执行:
1. gh pr view 15 --json ...
2. gh pr diff 15
3. 只做安全审查（跳过测试和性能）
4. 生成安全审查报告
```

### 飞书通知

```
用户: 审查完 PR 后把结果发到 "技术评审" 群

Agent 执行:
1. 执行完整审查流程
2. 使用 message 工具发送到指定飞书群
```

---

## 常见问题

### Q: gh 未认证怎么办？

```bash
gh auth login
# 或设置 token
export GITHUB_TOKEN="your_token"
```

### Q: 私有仓库无权限？

```bash
# 确认 gh 有仓库权限
gh auth status
# 重新授权
gh auth refresh -s repo
```

### Q: PR diff 太大怎么办？

- 使用 `--stat` 先看概览
- 分文件审查，重点关注安全和核心逻辑文件
- 跳过 lock 文件、生成代码等
