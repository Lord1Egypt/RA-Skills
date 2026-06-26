---
name: o
description: Short alias skill for quickly suggesting OS-specific commands to open files, folders, URLs, logs, or repositories from the command line or file explorer. Use when the user wants to open something and prefers a concise, minimal answer.
---

# o（Open 简写）

这是一个精简版的“打开” Skill，用一个字母 **o** 作为名称，方便被快速触发。它的目标是：

- 帮助选择**合适的打开方式**（命令或动作）
- 根据用户操作系统（尤其是 Windows PowerShell）给出**最简命令**
- 回答尽量简短，不做过多解释

---

## 适用场景

当用户说：

- “打开某个文件 / 目录 / 日志”
- “帮我打开这个链接 / 页面”
- “想在资源管理器里打开这个项目 / 仓库”
- “how do I open this from the terminal”

并且上下文中能看出**要打开的目标**时，应使用本 Skill 的指引。

---

## Windows（PowerShell / CMD）推荐

- **打开当前目录到资源管理器**：

  ```powershell
  start .
  ```

- **打开指定目录**：

  ```powershell
  start "C:\path\to\folder"
  ```

- **用默认程序打开文件**：

  ```powershell
  start "C:\path\to\file.txt"
  ```

- **打开 URL（默认浏览器）**：

  ```powershell
  start "https://example.com"
  ```

> 路径或 URL 可能包含空格时，一律加引号。

---

## macOS（仅在用户使用 macOS 时建议）

```bash
open .
open /path/to/folder
open /path/to/file.txt
open "https://example.com"
```

---

## Linux（桌面环境）

```bash
xdg-open .
xdg-open /path/to/folder
xdg-open /path/to/file.txt
xdg-open "https://example.com"
```

---

## 使用风格

- **答案要短**：优先只给 1–2 行命令，不写长篇解释。
- **尊重用户 OS**：根据会话中已知的操作系统给命令（当前用户是 Windows 10 + PowerShell）。
- **不做危险操作**：只给“打开”的命令，不附带修改 / 删除行为。