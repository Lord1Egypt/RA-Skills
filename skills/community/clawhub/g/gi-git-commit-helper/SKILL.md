---
name: gi-git-commit-helper
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
tags: ["git", "commit", "conventional-commits", "changelog"]
---

# Git Commit 提交信息生成

根据 git diff 分析变更内容，生成符合 Conventional Commits 规范的提交信息。

## 何时使用

- 用户请求「帮我写 commit message」「生成提交信息」
- 用户提到「git commit」「提交说明」
- 审查已暂存变更并生成描述

## 提交格式

遵循 Conventional Commits：

```
<type>(<scope>): <subject>

[optional body]
```

### type 类型

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | 修复 bug |
| docs | 文档 |
| style | 格式（不影响逻辑） |
| refactor | 重构 |
| perf | 性能优化 |
| test | 测试 |
| chore | 构建/工具/依赖 |

### scope 范围（可选）

- 后端：`api`、`service`、`dao`、`router`、`auth`
- 前端：`component`、`view`、`router`、`store`
- 通用：`config`、`deps`、`db`

### subject 主题

- 使用祈使句，如「add」「fix」「update」
- 首字母小写，结尾不加句号
- 控制在 50 字符内

## 示例

**示例 1：**
- 变更：新增用户登录接口
- 输出：`feat(auth): add JWT login endpoint`

**示例 2：**
- 变更：修复报表日期时区显示错误
- 输出：`fix(reports): correct date timezone in report generation`

**示例 3：**
- 变更：重构订单服务，拆分支付逻辑
- 输出：`refactor(service): extract payment logic from order service`

**示例 4：**
- 变更：更新 Vue 依赖版本
- 输出：`chore(deps): upgrade vue to 3.4.x`

## 生成流程

1. 运行 `git diff --staged` 或 `git diff` 获取变更
2. 分析变更文件与内容（新增/修改/删除）
3. 确定 type 和 scope
4. 用中文或英文写出简洁的 subject
5. 若变更复杂，可加简短 body 说明
