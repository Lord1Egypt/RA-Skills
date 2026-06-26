---
name: joplin-cli
description: Joplin 命令行操作（Shell 模式）。用于通过 CLI 创建、查看、编辑、同步笔记，适合脚本和自动化任务。
allowed-tools: Bash(joplin:*)
homepage: https://joplinapp.org/help/apps/terminal/#shell-mode
metadata:
  openclaw:
    requires:
      bins: [joplin]
---

# Joplin CLI Skill

通过命令行直接操作 Joplin，无需 API 服务。

## 常用命令

```bash
# 笔记本操作
joplin mkbook "笔记本名"           # 创建笔记本
joplin use "笔记本名"              # 切换当前笔记本
joplin ls /                        # 列出所有笔记本
joplin ls -l                       # 列出当前笔记本的笔记（含ID）

# 笔记操作
joplin mknote "标题"               # 创建笔记
joplin cat <id|标题>               # 查看笔记内容
joplin set <id> title "新标题"     # 修改标题
joplin set <id> body "内容"        # 修改内容
joplin edit <id>                   # 用编辑器打开

# 同步
joplin sync                        # 同步到远程
```

## 引用笔记

- 用 ID：`joplin cat fe889`
- 用标题：`joplin cat "我的笔记"`
- 用 `$n` 引用当前选中的笔记（TUI 模式）

## 详细文档

- `references/COMMANDS.md` — 完整命令参考
- `references/INSTALL.md` — 安装指南