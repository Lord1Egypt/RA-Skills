---
name: obsidian-folder-sync
description: |
  将任意文件夹（支持任何 AI agent workspace）同步到 Obsidian Vault。

  **触发场景**:
  - 用户说「同步到Obsidian」「备份到Obsidian」「Obsidian同步」「folder sync」
  - 需要将任意文件夹（skills、memory、项目文档等）备份到 Obsidian
  - 用户提供源目录和目标 Vault 路径时使用

  **功能**: 将指定文件夹内的所有 .md 文件单向同步到 Obsidian Vault 的指定子目录，
  排除 node_modules、.git、__pycache__、.venv 等目录。
---

# Obsidian Folder Sync

将任意文件夹同步到 Obsidian Vault，支持任何 AI agent 或手动管理的文件夹。

## 使用方式

```bash
bash ~/.openclaw/workspace/skills/obsidian-folder-sync/scripts/sync.sh <源目录> <目标Vault> [目标子目录]
```

**参数说明：**

| 参数 | 必填 | 说明 |
|------|------|------|
| 源目录 | ✅ | 要同步的文件夹绝对路径 |
| 目标Vault | ✅ | Obsidian Vault 路径 |
| 目标子目录 | ❌ | Vault 内的子文件夹（默认：源目录名）|

**示例：**

```bash
# 同步 AI agent skills 到 Obsidian
bash sync.sh ~/.openclaw/workspace/skills ~/Obsidian/MyVault

# 同步项目文档到 Vault 的 Projects 子目录
bash sync.sh ~/my-project/docs ~/Obsidian/MyVault Projects

# 同步记忆文件夹
bash sync.sh ~/my-agent/memory ~/Obsidian/MyVault Memory
```

## 同步规则

- ✅ **同步**：所有 `*.md` 文件
- ❌ **排除**：`node_modules/`、`__pycache__/`、`.git/`、`.venv/`、`.clawhub/`、`.learnings/`
- 📁 **映射**：源目录结构保持不变地映射到目标子目录

## 日志

日志文件：`~/.openclaw/workspace/logs/obsidian-folder-sync.log`

## 技术细节

- 工具：`rsync --files-from`，高效增量同步
- 文件列表写入 `/tmp/obsidian-folder-sync-$$/`，执行后自动清理
- 可通过环境变量覆盖配置（高级用法）
