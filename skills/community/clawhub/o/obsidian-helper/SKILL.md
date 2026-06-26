---
name: obsidian-helper
description: Operate Obsidian vaults from command line. Use when the user wants to list, search, create, read, edit, or delete Obsidian notes, or manage daily notes. Triggers on mentions of "obsidian笔记", "obsidian notes", "obsidian搜索", "obsidian创建", "obsidian列表", or any Obsidian vault operations.
metadata:
  {
    "obsidian-helper":
      {
        "emoji": "📝",
        "requires": { "bins": ["obsidian"], "env": ["OBSIDIAN_VAULT"] },
        "primaryEnv": "OBSIDIAN_VAULT",
      },
  }
---

# Obsidian Helper

A command-line tool for operating Obsidian vaults. Works with vaults stored on Windows (WSL) or Linux.

## Installation

### Quick Install (Recommended)

Run the install script:
```bash
cd ~/skills/obsidian-helper
bash scripts/install.sh
```

This will:
- Copy `obsidian` script to `~/bin/`
- Make it executable
- Add `~/bin` to your PATH (if not already present)

### Verify Installation

```bash
which obsidian
obsidian --version  # or obsidian help
```

## Quick Start

```bash
obsidian list              # 列出所有笔记
obsidian search 关键词      # 搜索笔记内容
obsidian create 文件名      # 创建新笔记
obsidian read 文件名        # 读取笔记
obsidian edit 文件名        # 编辑笔记 (vim)
obsidian daily             # 创建/查看日报
obsidian delete 文件名      # 删除笔记
```

## Configuration

The script auto-detects the vault path:

1. **Environment variable** (highest priority):
   ```bash
   export OBSIDIAN_VAULT=/path/to/your/vault
   ```

2. **WSL environment**: Auto-detects Windows user directory
   ```
   /mnt/c/Users/<WindowsUser>/Documents/Obsidian
   ```

3. **Linux environment**: Uses default path
   ```
   ~/obsidian
   ```

4. **Set your Obsidian vault path** (optional - auto-detects if not set):
   ```bash
   # Add to ~/.bashrc
   echo 'export OBSIDIAN_VAULT=/mnt/c/Users/YourName/Documents/Obsidian/Vault' >> ~/.bashrc
   source ~/.bashrc
   ```
   
## Commands Reference

| Command | Aliases | Description |
|---------|---------|-------------|
| `list` | `ls`, `l` | List all markdown notes in vault |
| `search <term>` | `s`, `find` | Search content in notes |
| `create <name> [content]` | `c`, `new` | Create new note |
| `read <name>` | `r`, `cat`, `show` | Read note content |
| `edit <name>` | `e`, `vim` | Edit note in vim |
| `daily [date]` | `d`, `today` | Create/view daily note |
| `delete <name>` | `del`, `rm` | Delete a note |
| `help` | `h` | Show help |

## Examples

```bash
# List all notes
obsidian list

# Search for "project"
obsidian search project

# Create a note in a folder
obsidian create "Projects/MyProject"

# Create with content
obsidian create "Ideas/Quick Note" "# Quick Note\n\nThis is my idea."

# Read a note
obsidian read "Welcome"

# Create today's daily note
obsidian daily
```

## Daily Notes

Daily notes are stored in `Daily/YYYY/YYYY-MM-DD.md` format.
