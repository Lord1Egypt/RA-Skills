---
name: work-start-helper
description: 工作开始时的 Git 同步和知识提示工具。当用户说"开干"、"开始干活"、"开始工作"或类似表达时触发此 skill。功能包括：1) stash 当前改动 2) pull --rebase 拉取最新代码 3) stash pop 恢复改动 4) 输出 JS、Vue、React、AI 工具使用知识各一条 5) 输出纳斯达克 100 指数涨跌幅。
---

# Work Start Helper

## 概述

此 skill 在用户说"开干"时自动执行 Git 拉取最新代码的工作流：stash → pull --rebase → stash pop，然后输出 JS、Vue、React、AI 工具使用知识各一条，最后输出纳斯达克 100 指数的涨跌幅。

## 工作流程

### Step 1: Stash 当前改动

在当前项目目录中执行 stash 暂存未提交的改动：

```bash
git stash push -m "temp stash before rebase $(date +%Y%m%d%H%M%S)"
```

### Step 2: Pull --rebase 拉取最新代码

拉取远程最新代码并 rebase 到最新：

```bash
git pull --rebase
```

注意：根据项目实际情况，可能需要指定分支（如 `git pull --rebase origin main`）。

### Step 3: Stash Pop 恢复改动

将 stash 的改动恢复到工作区：

```bash
git stash pop
```

### Step 4: 输出开发知识

工作流完成后，从 references/dev_tips.md 加载知识内容，输出 JS、Vue、React、AI 工具使用知识各一条。

读取 dev_tips.md 文件内容，解析并展示以下四个部分的知识点：
1. JavaScript 知识（防抖与节流）
2. Vue 知识（组合式 API）
3. React 知识（Hooks 最佳实践）
4. AI 工具使用技巧（精准提问、代码审查、调试）

### Step 5: 输出纳斯达克 100 指数涨跌幅

使用 web_search 工具查询纳斯达克 100 指数（Nasdaq 100 或 NDX）的**昨日收盘**涨跌幅信息并输出给用户。

## 注意事项

- 如果 rebase 过程中出现冲突，需要提示用户手动解决冲突后重新运行
- 如果没有 stash 内容，stash pop 会报错，此时可以忽略或提示用户
- 建议在执行前确认当前目录是有效的 Git 仓库