---
name: open
description: General helper for opening things from the command line (files, folders, URLs, repositories, docs). Use when the user wants to quickly open something they mentioned, and choose the right OS-specific command to launch it.
---

# Open Anything

This skill helps the agent suggest the **right command or action to open things**:

- Files and folders on disk
- URLs (web pages, docs, dashboards)
- Git repositories in a file explorer
- Logs, configs, or other local resources

It does not actually execute the commands itself; it tells the user what to run.

## When to Use

Use this skill when the user says：

- “打开某某文件 / 目录 / 日志”
- “帮我打开这个链接 / 页面”
- “想在资源管理器里打开这个项目 / 仓库”
- “how do I open this from the terminal”

and you need to translate that intent into a concrete **open** action.

## OS-specific Conventions

### Windows（PowerShell / CMD）

Prefer using `start` for most cases：

- **Open a folder in Explorer**：

```powershell
start .
start "C:\path\to\folder"
```

- **Open a specific file with its default app**：

```powershell
start "C:\path\to\file.txt"
```

- **Open a URL in the default browser**：

```powershell
start "https://clawhub.ai"
```

If the path might contain spaces, always wrap it in quotes.

### macOS（for reference）

If the user is on macOS, suggest：

```bash
open .
open /path/to/folder
open /path/to/file.txt
open "https://clawhub.ai"
```

### Linux（for reference）

If the user is on Linux with a desktop environment, suggest：

```bash
xdg-open .
xdg-open /path/to/folder
xdg-open /path/to/file.txt
xdg-open "https://clawhub.ai"
```

## Common Patterns

### Open the current project folder

From the project root：

- Windows（PowerShell）：

```powershell
start .
```

- macOS：

```bash
open .
```

- Linux：

```bash
xdg-open .
```

### Open a specific file mentioned by the user

If the user says “打开 `logs/app.log`”，assume it is relative to the project root：

- Windows：

```powershell
start ".\logs\app.log"
```

（路径中有空格时同样加引号。）

### Open a URL from text

When the user pastes or mentions a URL：

- Windows：

```powershell
start "https://example.com"
```

- macOS：

```bash
open "https://example.com"
```

- Linux：

```bash
xdg-open "https://example.com"
```

### Open a Git repo in Explorer / Finder

If the user wants to “open the repo” visually：

- Ensure you are in repo root, then：

  - Windows：

  ```powershell
  start .
  ```

  - macOS：

  ```bash
  open .
  ```

  - Linux：

  ```bash
  xdg-open .
  ```

## Guidelines

- **Always respect the user’s OS**：根据用户系统选择 Windows / macOS / Linux 命令。
- **Prefer non-destructive commands**：只负责“打开”，不要顺带修改、删除任何东西。
- **Quote paths and URLs**：凡是可能包含空格或特殊字符的路径与 URL，都加上引号。
- **Clarify ambiguity briefly**：如果用户说“打开它”但上下文里有多个可能的目标，先用一句话确认你指的是哪一个，再给命令。

