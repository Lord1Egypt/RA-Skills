# Git Log Tracker Onboarding

> 本文档指导 AI Agent 以**交互式方式**完成首次环境配置。
> Agent 应按顺序向用户提问，根据用户选择执行相应步骤。

## Prerequisites | 前置条件

- Python 3.11+
- `uv` 包管理器
- Git

## 交互流程

### Step 0: 询问用户使用意图

**必须先询问用户，不要自动执行！**

Agent 应使用 `AskUserQuestion` 工具询问用户的使用场景：

```
您打算如何使用 Git Log Tracker？
- 仅当前 repo
- 多个 repo（手动安装到每个）
- 全局模式（新 repo 自动带 hook）
- 批量扫描已有仓库并安装
```

根据用户选择，执行不同的步骤：

| 用户选择 | 执行步骤 |
|----------|----------|
| 仅当前 repo | Step 1-4 |
| 多个 repo | Step 1-3（完成后询问具体 repo 列表） |
| 全局模式 | Step 1-3 + Step 5 |
| 批量扫描已有仓库 | Step 1-3 + Step 6 |

---

### Step 1: 安装 CLI 工具

**所有场景都需要执行此步骤。**

#### 安装方式

从本地路径安装（作为 kinema_skills 组件的一部分）：
```bash
uv tool install D:/modular_dev/kinema_skills/git-log-tracker
```

或使用相对路径（如果在 kinema_skills 目录下）：
```bash
uv tool install ./git-log-tracker
```

#### 验证安装

```bash
git-log-tracker --help
# 期望: 显示帮助信息
git-log-tracker --version
# 期望: git-log-tracker 0.2.0
```

---

### Step 2: 初始化配置和数据库

**所有场景都需要执行此步骤。**

```bash
git-log-tracker setup
```

此命令会：
- 创建 `~/.commit-logs/` 目录
- 创建默认 `config.toml` 配置文件
- 初始化 SQLite 数据库

#### 验证

```bash
ls ~/.commit-logs/
# 期望: config.toml, index.db
git-log-tracker stats
# 期望: Total commits: 0
```

---

### Step 3: 验证环境

**所有场景都需要执行此步骤。**

```bash
git-log-tracker stats
# 期望: 显示统计信息（初始为 0 commits）
```

---

### Step 4: 安装 Hook 到当前 Repo

**仅当用户选择"仅当前 repo"时执行此步骤。**

#### 检测

```bash
git-log-tracker status .
```

#### 安装

```bash
git-log-tracker install .
```

#### 验证

```bash
git-log-tracker status .
# 期望: Status: installed [<repo_path>]
```

---

### Step 5: 全局模式配置

**仅当用户选择"全局模式"时执行此步骤。**

配置 Git template 目录，使新 clone 的 repo 自动带上 hook：

#### 检测

```bash
git config --global --get init.templateDir
```

#### 安装

```bash
git-log-tracker global
```

#### 验证

```bash
git-log-tracker global --off  # 如需关闭
git config --global --get init.templateDir
# 期望: ~/.git-templates
```

---

### Step 6: 批量扫描已有仓库

**仅当用户选择"批量扫描已有仓库"时执行此步骤。**

> ⚠️ **重要提示**：全局模式（Step 5）只会影响**后续创建或 clone 的仓库**，已有仓库不会自动注入 hook。
> 使用 `scan` 命令可以批量扫描并安装已有仓库的 hook。

#### 扫描目录

```bash
# 扫描指定目录（默认深度 5）
git-log-tracker scan D:/modular_dev

# 控制扫描深度
git-log-tracker scan D:/modular_dev --depth 3
```

输出示例：
```
Scanning D:\modular_dev for git repositories (depth=3)...

Found 8 repositories:
+----------------------------------------------------+--------------+--------------------+
| Repo Path                                          | Hook Status  | Branches           |
+----------------------------------------------------+--------------+--------------------+
| D:\modular_dev\kinema_skills\git-log-tracker       | [OK]         | master (1)         |
| D:\modular_dev\other_project                       | [--]         | main (1)           |
+----------------------------------------------------+--------------+--------------------+

Summary: 1 installed, 1 missing
```

#### 批量安装

扫描后可选择批量安装：

```bash
# 自动安装所有缺失 hook（需确认）
git-log-tracker scan D:/modular_dev --install-missing

# 交互式选择安装（选择具体仓库）
git-log-tracker scan D:/modular_dev --interactive

# 排除特定路径
git-log-tracker scan D:/modular_dev --exclude "*/temp/*" --exclude "*/.cache/*"
```

#### 常见场景

| 场景 | 命令 |
|------|------|
| 扫描工作目录下所有仓库 | `git-log-tracker scan ~/work --depth 4` |
| 扫描并安装所有缺失 hook | `git-log-tracker scan ~/work --install-missing` |
| 排除临时目录后扫描 | `git-log-tracker scan ~/work --exclude "*/tmp/*"` |
| 交互式选择安装 | `git-log-tracker scan ~/work --interactive` |

#### 验证

```bash
# 重新扫描验证安装状态
git-log-tracker scan D:/modular_dev
# 期望: Summary 显示全部 installed
```

---

## 数据存储位置

安装后的数据存储结构：

```
~/.commit-logs/
├── config.toml     # 配置文件（排除列表等）
├── index.db        # SQLite 数据库
```

**代码不再存储在 ~/.commit-logs/，而是通过 uv tool install 安装为系统命令。**

---

## Troubleshooting | 故障排除

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `git-log-tracker: command not found` | 未安装工具 | `uv tool install D:/modular_dev/kinema_skills/git-log-tracker` |
| `No module named 'tomllib'` | Python < 3.11 | 安装 Python 3.11+ |
| `uv: command not found` | uv 未安装 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| `Hook not triggering` | hook 文件无执行权限 | `chmod +x .git/hooks/post-commit` |
| `database is locked` | 多进程并发写入 | 等待其他操作完成，SQLite 自动处理 |
| `No commits found` | 数据库为空或排除规则过滤了 repo | 检查 `~/.commit-logs/config.toml` 中的 exclude 列表 |
| `Multiple commits match prefix` | hash 前缀太短 | 使用更长的 hash 前缀或完整 hash |
| `scan: No git repositories found` | 目录下无 git 仓库或深度不足 | 增加 `--depth` 或检查路径是否正确 |
| `scan: Permission denied` | 目录权限不足 | 检查目录访问权限 |

---

## 升级方式

从旧版本升级：

1. **卸载旧 hook**（如果之前已安装）：
   ```bash
   # 如果之前使用 scripts/ 方式安装
   rm ~/.commit-logs/hook.py ~/.commit-logs/db.py ~/.commit-logs/install.py ~/.commit-logs/query.py ~/.commit-logs/setup_global.py
   rm -rf ~/.commit-logs/__pycache__
   ```

2. **重新安装 hook**（使用新 CLI）：
   ```bash
   git-log-tracker install .
   ```

3. **数据保留**：
   - `~/.commit-logs/index.db` 和 `config.toml` 无需迁移，保持原样

---

## 版本管理

**Skill 版本与 CLI 版本绑定，更新时需同步修改以下文件：**

| 文件 | 版本位置 |
|------|----------|
| `pyproject.toml` | `version = "x.y.z"` |
| `src/git_log_tracker/__init__.py` | `__version__ = "x.y.z"` |
| `SKILL.md` | `version: x.y.z` (frontmatter) |

更新版本后需要重新安装 CLI：
```bash
uv tool install D:/modular_dev/kinema_skills/git-log-tracker --force
```