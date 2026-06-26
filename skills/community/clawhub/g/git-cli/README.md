# git-cli Skill

Git 命令行助手：在 Cursor 里回答或执行与 Git 相关的操作（查看状态、暂存提交、分支、推送拉取、stash、历史、标签、合并/变基、克隆等）。**SKILL.md** 面向 AI，说明何时用、如何用、安全原则和快速参考；本 README 面向人类，说明目录与用法。

## 何时会用到

- 用户问「怎么用 Git 做 XXX」「这条命令什么意思」「push 被拒绝了怎么办」等。
- 用户需要查看当前状态、写提交信息、建分支、解决冲突、恢复误操作时，AI 会优先查本 skill 的 Quick Reference 和 reference/，必要时引用 scripts/ 或 assets/。

## 目录结构

```
git-cli/
├── SKILL.md              # AI 工作指南：流程、安全、快速参考、去哪查
├── README.md              # 本文件（人类可读说明）
├── reference/             # 详细参考（命令、工作流、排错）
│   ├── README.md
│   ├── commands.md        # 命令列表与常用选项
│   ├── workflows.md       # 分步工作流
│   └── troubleshooting.md # 常见错误与处理
├── scripts/               # 可执行脚本（需在仓库根目录运行）
│   ├── README.md
│   ├── is-repo.sh         # 当前目录是否 Git 仓库
│   ├── status-summary.sh  # 分支 + 上游 + 最近提交 + 状态
│   └── branch-list.sh    # 本地/远程分支及上游
└── assets/                # 模板与静态资源
    ├── README.md
    ├── commit-msg-template.txt  # 提交信息模板（Conventional Commits）
    └── gitignore-common.txt     # 常用 .gitignore 片段
```

## 各目录说明

| 目录 | 内容 | 典型用法 |
|------|------|----------|
| **reference/** | 命令表、分步工作流、排错说明 | 需要详细步骤或查某条命令时看 [commands.md](reference/commands.md)、[workflows.md](reference/workflows.md)、[troubleshooting.md](reference/troubleshooting.md) |
| **scripts/** | Bash 脚本 | 在**仓库根目录**执行，如：`bash path/to/scripts/status-summary.sh`；Windows 上可用 Git Bash 或 WSL |
| **assets/** | 提交信息与 .gitignore 模板 | 需要格式示例或忽略规则时参考 [commit-msg-template.txt](assets/commit-msg-template.txt)、[gitignore-common.txt](assets/gitignore-common.txt) |

## 运行脚本

- 环境：需要已安装 Git，且当前在要检查的**仓库根目录**（或先 `cd` 到该目录）。
- Windows：在 **Git Bash** 或 **WSL** 中运行，例如：
  ```bash
  bash .cursor/skills/git-cli/scripts/status-summary.sh
  ```
- 各脚本用途见 [scripts/README.md](scripts/README.md)。

## 依赖与约定

- **Git**：需在 PATH 中（`git --version` 可用）。
- **脚本**：仅提供 `.sh` 版本，便于跨平台与 clawhub 发布；Windows 用户通过 Git Bash/WSL 使用。
