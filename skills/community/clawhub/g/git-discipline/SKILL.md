---
name: git-discipline
description: Apply safe git workflow rules for the current local repository: branches, commits, staging, and history handling. Use when the user asks to inspect git state, create branches, prepare commits, review staged changes, or manage history without risking unrelated work. Do not use for GitHub API operations, PR review workflows, or remote repository administration. Chinese triggers: Git 规范、分支命名、提交信息、提交前检查、安全提交、不改公共历史.
---

# Git 规范

让 Git 操作保持收敛、可回退、不误伤共享历史。

## 工作流

1. 动手前先看当前仓库状态。
2. 每个分支和提交只承载一件清晰的事情。
3. 分支名使用小写短横线风格。
4. 提交信息简洁，准确描述真实改动。
5. 不重写已发布历史，不对共享分支 force-push。
6. 提交中不得包含密钥、token、证书等敏感内容。
7. 不丢弃、不覆盖无关的工作区改动。
8. 优先使用非交互式 Git 命令，并明确说明即将执行的动作。

## 输出

- 当前 Git 状态
- 下一步安全操作建议
- 如有需要，给出分支名或提交信息建议
- 如果请求会改写或丢弃历史，明确风险
