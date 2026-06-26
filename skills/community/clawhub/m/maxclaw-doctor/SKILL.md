---
name: mmxagent-guardian
version: 1.0.0
description: 帮助用户使用openclaw时提供文件保护，所有文件操作均建立版本索引，支持删除恢复和修改回滚
---

# 文件保护与版本管理

本 Skill 使用 MiniVCS 对所有文件操作进行版本追踪。

**脚本位置**：与本 SKILL.md 同目录下的 `scripts/minivcs/minivcs.py`
（执行前需先确定本文件所在目录，下文以 `$SKILL_DIR` 表示）

**核心机制：**
- **修改**：保存增量 Diff + 修改前完整快照，**支持回滚**
- **删除**：将文件完整移入 `~/.openclaw/minivcs/trash/`，**支持恢复**
- **所有文件均建立索引**，根据重要程度设定不同留存期
- **每次操作后自动扫描**整体记录表，找出已到期记录并通知用户确认

**使用限制：**
- **二进制文件（图片、PDF、音视频等）**：无法进行文本 diff，改为直接将文件完整复制一份存为 `.bak` 备份，支持回滚还原，原文件不受影响。需告知用户：二进制文件每次调用 `record` 都会保存一份完整副本，占用空间相对较大。
- **首条记录无法回滚**：一个文件第一次被 record 时尚无历史基准，该条记录没有快照；此后每次编辑后调用一次 `record_modify`，均会自动保存快照，支持回滚到任意一次编辑前的状态

---

## 前置检查：确认 Python 已安装

**在执行任何操作前，必须先检查用户环境是否安装了 Python 3。**

### 检测方式

```bash
# macOS / Linux
python3 --version

# Windows（PowerShell）
python --version
```

- 输出 `Python 3.x.x` 即为已安装，可继续
- 提示 `command not found` 或 `不是内部或外部命令` 则需要帮用户安装

### 安装指引（未安装时）

#### macOS

推荐通过 Homebrew 安装：

```bash
# 先检查是否有 Homebrew
brew --version

# 有 Homebrew：直接安装
brew install python3

# 没有 Homebrew：先安装 Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python3
```

**如果用户在中国大陆**，访问 GitHub 速度慢，安装前先配置镜像源加速：

```bash
# 使用清华大学镜像安装 Homebrew
/bin/bash -c "$(curl -fsSL https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/install.sh)"

# 安装完成后，替换 Homebrew 核心源为清华镜像
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"

# 将上面的环境变量写入 shell 配置文件，永久生效
echo 'export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"' >> ~/.zshrc
echo 'export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"' >> ~/.zshrc
echo 'export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"' >> ~/.zshrc
echo 'export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"' >> ~/.zshrc
source ~/.zshrc

# 再安装 Python
brew install python3
```

> 如果用户使用 bash 而非 zsh，把上面的 `~/.zshrc` 替换为 `~/.bash_profile`。
> 中国大陆镜像源参考：清华 https://mirrors.tuna.tsinghua.edu.cn/help/homebrew/

也可引导用户前往官网下载安装包：https://www.python.org/downloads/macos/

#### Linux（Debian / Ubuntu）

```bash
sudo apt update && sudo apt install -y python3 python3-pip
```

#### Linux（CentOS / RHEL / Fedora）

```bash
# CentOS / RHEL
sudo yum install -y python3

# Fedora
sudo dnf install -y python3
```

#### Windows

推荐引导用户从官网下载安装：https://www.python.org/downloads/windows/

安装时勾选 **"Add Python to PATH"**，否则命令行无法识别 `python` 命令。

安装完成后在 PowerShell 中验证：
```powershell
python --version
pip --version
```

> **注意**：Windows 上部分系统命令为 `python`，macOS/Linux 为 `python3`。
> 后续所有命令中的 `python` 请根据实际环境替换为正确的命令名。

---

## 留存策略

| 文件类型 | 留存天数 | 判定规则 |
|---------|---------|---------|
| 重要文件 | **14 天** | 系统路径（`/etc/`、`/root/`、`~` 目录）、Windows C 盘、配置文件（`.yaml/.toml/.env` 等）、入口文件（`main.py/index.ts` 等） |
| 普通文件 | **7 天** | 其余所有文件 |

每条记录创建时自动设置 `expireAt`（到期时间戳）和 `expireAtDatetime`（可读时间）字段。

---

## 操作流程

### 第一步：初始化 MiniVCS 工作目录

首次使用时自动创建存储目录，无需额外操作：

```bash
python "$SKILL_DIR/scripts/minivcs/minivcs.py" history --project-root <project_root>
```

数据统一存储在 `~/.openclaw/minivcs/`：
```
~/.openclaw/minivcs/
  logs.json     # 操作日志（含 expireAt 字段）
  diffs/        # 文本文件修改的增量补丁
  bases/        # 下次比较的基准（按完整相对路径命名，无同名冲突）
  snapshots/    # 文本文件修改前的完整快照（用于回滚）
  trash/        # 已删除文件的完整备份（用于恢复）
  backups/      # 二进制文件的 .bak 完整副本备份（用于回滚）
```

---

### 第二步：操作前询问用户确认

**删除或修改文件前，必须向用户说明以下内容，并等待确认：**

1. 要操作的文件路径
2. 操作类型（修改 / 删除）
3. 操作目的与意图
4. 可能产生的影响
5. **告知保护范围：只有文本文件会被自动备份和追踪；若涉及二进制文件（图片、PDF 等），不会被记录，需用户自行保管**
6. **告知文本文件已纳入版本记录，可随时恢复/回滚**

操作前示例：
```
我即将对以下文件进行操作，请确认：
- 文件：/path/to/file.py
- 操作：删除
- 原因：该文件已被新版本替代，不再使用
- 影响：需确认没有其他模块导入此文件
- 保护：操作完成后将自动备份，留存 7 天（重要文件 14 天），期间可随时恢复
是否确认继续？
```

操作完成后，**必须告知用户记录结果**，示例：
```
# 修改完成后
已完成对 path/to/file.py 的修改，并记录了本次变更（Record ID: 1710000000000）。
- 变更摘要：+5 lines, -2 lines
- 留存期：7 天（到期时间：2026-03-20 10:00:00）
- 可回滚：是（使用 restore 1710000000000 可恢复到修改前状态）
如需查看 Diff 或回滚，请告诉我。

# 删除完成后
已将 path/to/file.py 移入回收站并建立备份（Record ID: 1710000001000）。
- 留存期：14 天（到期时间：2026-03-27 10:00:00）[重要文件]
如需恢复该文件，请告诉我。
```

---

### 第三步：使用 MiniVCS 操作文件

#### 修改文件（支持回滚）

**每次编辑后调用一次 `record` 即可**，快照链自动形成，支持回滚到任意历史状态：

```
初次使用该文件 → record() → base 建立（无快照，首条记录不可回滚）
编辑 → C1      → record() → snapshot=初始内容,  R1 可回滚
编辑 → C2      → record() → snapshot=C1,        R2 可回滚 → 恢复 R2 得到 C1
编辑 → C3      → record() → snapshot=C2,        R3 可回滚 → 恢复 R3 得到 C2（即 t2 时刻）
```

```bash
# 每次编辑完成后执行一次
python "$SKILL_DIR/scripts/minivcs/minivcs.py" record <file_path> --project-root <project_root>
# 输出含 "Rollback: available" 表示快照已保存，可回滚
```

Python API：
```python
import sys, os
sys.path.insert(0, os.path.join(SKILL_DIR, "scripts", "minivcs"))
from minivcs import MiniVCS

vcs = MiniVCS(project_root="/path/to/project")

# 每次编辑后调用一次
result = vcs.record_modify("path/to/file.py")
# result 包含：
# {
#   "success": True,
#   "recordId": "...",
#   "summary": "+5 lines, -2 lines",
#   "canRollback": True,   # 有快照时为 True，首条记录为 False
#   "snapshotFile": "...",
#   "isImportant": False,
#   "retentionDays": 7,
#   "due_for_cleanup": [...]
# }
```

#### 删除文件（支持恢复）

**不要直接删除文件**，改用 `record_delete`，文件自动移入 trash：

```bash
python "$SKILL_DIR/scripts/minivcs/minivcs.py" delete <file_path> --project-root <project_root>
```

Python API：
```python
result = vcs.record_delete("path/to/file.py")
# result 包含：
# {
#   "success": True,
#   "recordId": "...",
#   "trashFile": "~/.openclaw/minivcs/trash/1234567_file.py.bak",
#   "isImportant": True,
#   "retentionDays": 14,
#   "due_for_cleanup": [...]
# }
```

#### 恢复/回滚

同一命令 `restore` 处理两种场景：

```bash
# DELETE 记录 → 恢复文件到原路径
# MODIFY 记录（含快照）→ 回滚到修改前状态
python "$SKILL_DIR/scripts/minivcs/minivcs.py" restore <record_id> --project-root <project_root>
```

Python API：
```python
result = vcs.restore_file(record_id="...")
# DELETE 成功后：记录标记为 RESTORED，不再出现在 trash 列表
# MODIFY 成功后：记录标记为 ROLLED_BACK
# 重复恢复：返回 {"success": False, "error": "already been restored/rolled_back"}
```

---

### 第四步：处理到期清理通知（每次操作后必须执行）

每次调用 `record_modify` 或 `record_delete` 后，返回值中包含 `due_for_cleanup` 字段。

**若 `due_for_cleanup` 不为空，Agent 必须：**

1. 向用户展示到期记录列表（从早到晚排序）
2. 询问用户哪些可以删除、哪些需要延期

展示格式示例：
```
以下 N 条历史记录已到期，请确认是否可以清理：

[1] ID=1710000000000  文件=src/old.py  操作=MODIFY
    记录时间=2026-03-01 10:00:00  到期时间=2026-03-08 10:00:00

[2] ID=1710000001000  文件=config.yaml  操作=DELETE  [重要文件]
    记录时间=2026-02-28 09:00:00  到期时间=2026-03-14 09:00:00

请问这些记录可以删除吗？（可以全部删除 / 指定哪些延期）
```

用户响应后的处理：

```python
# 用户确认全部删除
result = vcs.delete_due_records(record_ids=["id1", "id2"])

# 用户说某条暂不删除 → 延后一个留存周期（7天或14天）
result = vcs.extend_record_expiry(record_id="id1")
```

命令行：
```bash
# 查看所有到期记录
python "$SKILL_DIR/scripts/minivcs/minivcs.py" cleanup --project-root <project_root>

# 确认清理
python "$SKILL_DIR/scripts/minivcs/minivcs.py" cleanup --confirm --project-root <project_root>

# 延期某条记录
python "$SKILL_DIR/scripts/minivcs/minivcs.py" extend <record_id> --project-root <project_root>
```

---

## 其他常用操作

```bash
# 查看操作历史（标注 [rollback available] 的记录可回滚）
python "$SKILL_DIR/scripts/minivcs/minivcs.py" history --project-root <project_root>
python "$SKILL_DIR/scripts/minivcs/minivcs.py" history <file_path> -d --project-root <project_root>

# 查看 trash 中尚未恢复的文件
python "$SKILL_DIR/scripts/minivcs/minivcs.py" trash --project-root <project_root>

# 删除指定记录（日志 + 物理文件一并清理）
python "$SKILL_DIR/scripts/minivcs/minivcs.py" remove <record_id> --project-root <project_root>
```

---

## 记录字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `recordId` | string | 唯一记录 ID（毫秒时间戳） |
| `filePath` | string | 相对或绝对路径 |
| `action` | string | `MODIFY` / `DELETE` / `BINARY_BACKUP` / `RESTORED` / `ROLLED_BACK` |
| `timestamp` | number | 创建时间（毫秒） |
| `datetime` | string | 创建时间（可读） |
| `isImportant` | bool | 是否为重要文件 |
| `retentionDays` | number | 留存天数（7 或 14） |
| `expireAt` | number | 到期时间（毫秒） |
| `expireAtDatetime` | string | 到期时间（可读） |
| `diffFile` | string | Diff 补丁路径（MODIFY 专有） |
| `snapshotFile` | string | 修改前快照路径（MODIFY 有快照时才有） |
| `trashFile` | string | Trash 备份路径（DELETE 专有） |
| `backupFile` | string | `.bak` 副本路径（BINARY_BACKUP 专有） |
| `summary` | string | 变更摘要 |

---

## 完整操作流程图

```
用户发起修改/删除请求
       │
       ▼
[询问确认] 说明操作目的、影响、已有保护 → 等待用户确认
       │
       ├─── 修改文件 ─────────────────────────────────────────┐
       │    1. 执行实际修改                                    │
       │    2. record_modify（Diff + 快照 → canRollback=True） │
       │       快照 = 本次修改前内容，可逐级回滚历史状态         │
       │                                                      │
       └─── 删除文件 ─────────────────────────────────────────┤
            record_delete（移入 trash，不直接删除）             │
                                                              │
                           ┌──────────────────────────────────┘
                           ▼
              告知用户：Record ID / 留存期 / 可回滚/可恢复
                           │
                           ▼
              检查返回值 due_for_cleanup
                           │
               ┌───────────┴───────────┐
             有到期记录               无到期记录
               │                         │
               ▼                         ▼
       展示到期记录（从早到晚）        操作完成
       询问用户确认
               │
       ┌───────┴──────────┐
     确认删除           暂不删除
       │                  │
       ▼                  ▼
delete_due_records   extend_record_expiry
                     （延后一个留存周期）

------- 用户需要回滚/恢复时 -------
用户："帮我恢复/回滚 xxx"
       │
       ▼
restore_file(record_id)
  ├── DELETE 记录 → 从 trash 恢复，标记 RESTORED
  └── MODIFY 记录（有快照）→ 写回快照内容，标记 ROLLED_BACK
```
