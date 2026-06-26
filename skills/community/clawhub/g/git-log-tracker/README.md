# Git Log Tracker

Git post-commit hook + SQLite 索引工具。自动记录每次 commit 的元数据，支持跨仓库查询、统计和管理。

## 核心特性

> **一句话**：安装 hook → 每次 commit 自动入库 → 跨仓库查询 / 统计 / 管理

### 自动记录

Git post-commit hook 自动写入 commit 元数据（hash、author、branch、repo、subject）到本地 SQLite 数据库。

### 跨仓库查询

- 按 hash、仓库、作者、日期、分支、标签筛选
- 支持前缀匹配查找 commit
- 查找某个 commit 属于哪个仓库

### 仓库标签

- 给仓库打**仓库级标签**（label），按"组"过滤（如 work / personal）
- `list --label` / `stats --label` 只显示带该标签的仓库
- 标签即时对该仓库全部历史 commit 生效

### 统计与管理

- 按仓库 / 作者聚合统计
- CRUD 操作：record / delete / update
- 全局模式：新 repo 自动安装 hook
- 排除规则：fnmatch 通配符排除指定路径

## 安装

### 方法一：通过 Claude Code Marketplace

1. 添加 Marketplace：

```
/plugin marketplace add https://github.com/KinemaClawWorkspace/kinema-skills-marketplace
```

2. 安装 Skill：

```
/plugin install git-log-tracker@kinema-skills-marketplace
```

3. 查看已安装的 Skill：

```
/plugin list
```

### 方法二：通过 ClawHub OpenClaw

```bash
openclaw skills install git-log-tracker
```

## 适用场景

| 场景 | 说明 |
|------|------|
| 查找跨仓库 commit | "abc123 这个 commit 在哪个仓库？" |
| 查看 commit 历史 | "列出最近 50 条 commit" |
| 统计工作量 | "统计各仓库 / 作者的 commit 数量" |
| 管理 git hooks | "给这个仓库安装 hook" |
| 全局 hook 管理 | "新仓库自动带 hook" |

## 触发方式

本 skill 为 OpenClaw/Claude Code 技能，安装后可通过对话触发：

```
安装 git hook 到这个仓库
查找 abc123 这个 commit
列出最近的 commit
统计 commit 数量
git-log-tracker setup
```

首次使用需完成 [ONBOARDING.md](ONBOARDING.md) 环境配置（安装 CLI 工具）。

## 命令列表

| 命令 | 说明 |
|------|------|
| `setup` | 初始化配置和数据库 |
| `install <repo>` | 安装 hook 到指定仓库 |
| `uninstall <repo>` | 从指定仓库移除 hook |
| `status <repo>` | 检查仓库 hook 状态 |
| `scan <path> [--depth] [--install-missing] [--interactive] [--exclude]` | 扫描目录中的 git 仓库，批量管理 hook |
| `global [--off]` | 配置全局 git 模板 |
| `find <hash>` | 按 hash 查找 commit |
| `list` | 列出最近的 commits（支持 `--label` 过滤） |
| `stats` | 显示统计信息（支持 `--label` 过滤） |
| `label add/rm/list [repo] [labels...]` | 管理仓库级标签 |
| `record [repo]` | 手动记录最新 commit |
| `delete <hash>` | 删除 commit 记录 |
| `update <hash> <field> <value>` | 更新 commit 字段 |
| `reinstall [--keep-config]` | 重置数据目录并重新初始化 |

## 文件结构

```
git-log-tracker/
├── SKILL.md              # Skill 定义文件
├── ONBOARDING.md         # 首次配置引导
├── README.md             # 本文档
├── src/
│   ├── cli.py            # CLI 入口
│   ├── config.py         # 配置管理
│   ├── db.py             # SQLite 数据库操作
│   ├── hook.py           # Hook 脚本
│   └── pyproject.toml    # Python 项目配置
│                         # 标签存储于 ~/.commit-logs/labels.json
└── LICENSE               # GPLv3 许可证
```

## 作者

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)

## 许可证

[GNU General Public License v3.0](LICENSE)