# git-sync 完整使用指南

> 本文档是 SKILL.md 的渐进式补充，包含完整的执行流程、步骤详解和配置说明。

---

## 完整执行流程（步骤 0 → 6）

### 步骤 0：安全校验（v1.4 新增）

| 校验项 | 规则 |
|--------|------|
| 路径穿越防护 | 拒绝 `../`、`..\\`、`/` 开头、`C:` 开头 |
| 目标路径范围 | `realpath` 必须在 `WORK_REPO/skills/` 内 |
| 同步工具选择 | 优先 `rsync --delete`，不可用则 `rm -rf` + `cp -r` |

### 步骤 0.5：维护清单检查（v1.3 新增）

同步前自动检查 `manifest.json`，决定行为：

| 检查结果 | 行为 |
|---------|------|
| `FOUND:uploaded` | ✅ 继续执行 |
| `FOUND:not-uploaded` | ⏳ 继续执行，完成后标记 uploaded=true |
| `NOT_FOUND` | ❓ 询问：加入清单 / 仅本次同步 / 中止 |

### 步骤 0.7：版本号三方对比（v1.6 新增）

> 这一步检查的是**清单 version vs 待推送 version**，属于三单一致的前置校验。
> 三单一致完整定义见 `reference.md` 的三单一致模型。

| 对比结果 | 行为 |
|---------|------|
| 清单无此条目 | ✅ 正常执行，完后写入 version 到清单 |
| 清单 version = 待更新 version | ❓ 询问是否跳过（默认跳过） |
| 清单 version < 待更新 version | ✅ 正常升级，更新清单 |
| 清单 version > 待更新 version | ❌ 版本异常，询问策略（覆盖/拉取/合并/中止） |

> 注：以 manifest.json 记录的 version 为准，仓库 _meta.json 仅作参考。

### 步骤 1：_meta.json 版本同步

同步 version 字段，补全缺失的 name/description，**保留所有既有字段**（不删除任何字段）。

| 标准字段 | 缺失时处理 |
|---------|-----------|
| `name` | 使用目录名 |
| `version` | 使用传入的 version 参数 |
| `description` | 从 SKILL.md 提取 |
| `author` | 从 config.json 读取（缺省为 `your-name-here`） |
| `tags` | 设为空数组 `[]` |

### 步骤 1.5：SKILL.md 规范化审查（v1.8 新增）

- **工具**：`-m scripts.skill_audit`（独立 Python CLI，零依赖）
- **规则集**：R-01 ~ R-10（4 ERROR + 6 WARN）
- **模式**：纯警告不阻断（始终 exit(0)）
- **输出**：人类可读终端报告 + 支持 `--json` 模式
- **特性**：同义词关键词匹配容忍章节命名不一致

### 步骤 2：同步文件到工作仓库

将技能从 ``~/.workbuddy/skills/`<skill-name>/` 同步到 `WORK_REPO/skills/<skill-name>/`。

### 步骤 3：全量重新生成 README.md

> **关键原则**：README.md = 仓库实际内容，不手动维护。

从仓库 `skills/` 目录实际扫描，全量替换 README.md 中的技能列表表格和目录结构。

### 步骤 3.5：SKILL.md 审查输出

审查结果以人类可读格式打印到终端：

```
==================================================
📋 Skill 更新检查报告: <skill-name>
==================================================

✅ 通过项:
   ✅ _meta.json 结构正常
   ...

⚠️  警告/建议:
   💡 具体警告信息...

结论: ERROR=0 WARN=1 PASS=5
```

### 步骤 4：提交并推送到双平台

```bash
git add → git commit → git pull --rebase → git push
```

推送结果分别记录（对应三单一致的状态标记）：
- 码云成功 → 更新 `gitee_version` + 标记 `gitee_ok=true`（Gitee 三单一致）
- GitHub 成功 → 更新 `github_version` + 标记 `github_ok=true`（GitHub 三单一致）
- `uploaded` = `gitee_ok AND github_ok`（双平台均三单一致）

### 步骤 5：生成 ZIP 安装包

```
输出: `.dist/<skill-name>-v<x.x.x>.zip`
排除: *.zip, __pycache__/, .DS_Store, .git, *.html, *.log, ...
```

打包在临时副本中进行，不影响源文件。敏感信息过滤（如果启用）作用于副本。

### 步骤 6：统一输出 + HTML 索引

1. 复制 ZIP 到统一目录 `~/.workbuddy/skills/.dist/`
2. 自动生成/刷新 `index.html` 索引页（含 file:// 链接 + 文件大小 + 时间）
3. 自动打开 dist/ 目录（Windows explorer / macOS open / Linux xdg-open）

> **每次执行完毕后 AI 必须主动调用 `preview_url` 打开 index.html。**

---

## config.json 完整配置模板

```json
{
  "author": "你的作者名",
  "gitee": {
    "user": "你的码云用户名",
    "repo": "workbuddy-skills",
    "branch": "main",
    "remote_name": "gitee"
  },
  "github": {
    "user": "你的 GitHub 用户名",
    "repo": "workbuddy-skills",
    "branch": "main",
    "remote_name": "origin"
  }
}
```

**关键字段说明**：

| 字段 | 影响范围 |
|------|---------|
| `author` | `_meta.json` 默认作者名；敏感扫描中的用户名检测基准 |
| `gitee.user` / `github.user` | 生成的查看链接和 README 安装命令中的用户名占位符 |
| `gitee.repo` / `github.repo` | 工作仓库名称（通常两个平台相同） |
| `branch` | 推送目标分支（通常为 main） |

---

## 跨平台环境适配

> 本技能依赖 `rsync` 做本地文件同步。不同平台/安装方式下 `rsync` 可用性不同，需提前确认。

### 环境矩阵

| 环境 | rsync 是否可用 | 说明 |
|------|----------------|------|
| Linux / macOS | ✅ 自带 | 无需额外操作 |
| Git for Windows 完整版 | ✅ 自带 | 位于 Git 安装目录的 usr/bin/ 下 |
| **WorkBuddy PortableGit** | ❌ 不含 | 需手动安装（见下方） |
| Cygwin / MSYS2 | ✅ 自带 | 通过包管理器安装 |
| WSL | ✅ 自带 | 无需额外操作 |

### Windows 下 Python 路径转换问题（重要）

当 `rsync` 不可用时，脚本会 fallback 到 `sync_with_exclude.py`（Python 方案）。

**问题根因：**
- Git Bash 只对 **MSYS2 编译的程序** 自动转换 Unix 路径（`/c/Users/...` → `C:\Users\...`）
- 如果 `python` 是 **Windows 原生 exe**（如 `.workbuddy\binaries\...`），路径不会被转换
- Python 收到 `/c/Users/...` 会误解为 `C:\c\Users\...`，导致文件找不到

**症状：**
```
C:\Users\sm001\.workbuddy\binaries\python\...\python.exe: can't open file 'c:\\c\\Users\\...'
```

**解决方案（任选其一）：**

| 方案 | 操作 | 推荐度 |
|------|------|--------|
| **A. 安装 rsync** | 见下方「各平台安装 rsync」| ⭐⭐⭐ 最推荐 |
| **B. 用 MSYS2 版 Python** | `pacman -S python`（MSYS2 内）| ⭐⭐ |
| **C. 手动调用 Python 时传 Windows 路径** | `python sync_with_exclude.py "C:\..." "C:\..."` | ⭐ 临时 |

### 各平台安装 rsync

#### Windows（WorkBuddy PortableGit 环境）

**方式一：下载独立 rsync.exe 放到 PortableGit**

```bash
# 在 Git Bash 中执行，下载 rsync.exe 到 PortableGit/usr/bin/
cd /c/Users/sm001/.workbuddy/vendor/PortableGit/usr/bin/
# 从 Git for Windows 获取 rsync 工具
# 在 Git Bash 中执行：
cd /c/Users/sm001/.workbuddy/vendor/PortableGit/usr/bin/
# 安装 rsync（如已安装可跳过）
# 验证
rsync --version
```

# 验证
rsync --version
```

**方式二：安装完整版 Git for Windows**

从 [git-scm.com](https://git-scm.com/download/win) 下载安装，**安装时勾选「Use Unix tools from the Command Prompt」**，安装后 `rsync` 可用。

#### Linux

```bash
# Debian/Ubuntu
sudo apt install rsync

# RHEL/CentOS
sudo yum install rsync

# Arch
sudo pacman -S rsync
```

#### macOS

```bash
# 自带 rsync，如缺失：
brew install rsync
```

#### MSYS2 / Cygwin

```bash
# MSYS2
pacman -S rsync

# Cygwin（通过安装程序添加 rsync 包）
```

### 故障排除

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| `rsync: command not found` | rsync 未安装或未在 PATH | 按上方对应平台安装 |
| `can't open file 'c:\\c\\Users\\...'` | Python fallback 路径转换失败 | 安装 rsync，或传 Windows 路径调用 Python |
| `SCRIPT_DIR` 路径计算错误 | 用绝对路径调用 `bash git-sync.sh` | **先 `cd` 到脚本目录再执行**（见下方正确调用方式）|

### 正确调用方式

```bash
# ✅ 推荐：先 cd 到脚本目录，再执行
cd ~/.workbuddy/skills/git-sync/scripts
bash git-sync.sh <skill-name> <version>

# ❌ 避免：直接从其他目录用绝对路径调用
bash "C:/Users/sm001/.workbuddy/skills/git-sync/scripts/git-sync.sh" <skill-name> <version>
```

---

## 配置说明（LLM 参考）

> 本技能的配置存放在数据目录，脚本自动读取，无需手动创建文件。

### 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| `config.json` | `skills/.standardization/git-sync/data/config.json` | 平台用户名、仓库名、分支等配置 |
| `manifest.json` | `skills/.standardization/git-sync/data/manifest.json` | 技能同步状态清单 |

### config.json 字段说明

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `author` | `_meta.json` 默认作者名；敏感扫描中的用户名检测基准 | `[username-redacted]` |
| `gitee.user` | 码云用户名，用于生成查看链接和 README 命令 | `[username-redacted]` |
| `gitee.repo` | 码云仓库名 | `workbuddy-skills` |
| `gitee.branch` | 码云推送目标分支 | `main` |
| `github.user` | GitHub 用户名 | `[username-redacted]` |
| `github.repo` | GitHub 仓库名 | `workbuddy-skills` |
| `github.branch` | GitHub 推送目标分支 | `main` |

### 脚本读取方式

所有 `git-sync` 脚本通过以下逻辑定位 `config.json`：

```python
import os
SKILLS_DIR = os.path.expanduser('~/.workbuddy/skills')
GIT_SYNC_DATA = os.path.join(SKILLS_DIR, '.standardization', 'git-sync', 'data')
config_path = os.path.join(GIT_SYNC_DATA, 'config.json')
```

### 初始化配置

首次使用本技能前，确保数据目录中存在 `config.json`：

```bash
mkdir -p ~/.workbuddy/skills/.standardization/git-sync/data
cat > ~/.workbuddy/skills/.standardization/git-sync/data/config.json << 'EOF'
{
  "author": "your-name-here",
  "gitee": {
    "user": "your-gitee-username",
    "repo": "workbuddy-skills",
    "branch": "main",
    "remote_name": "gitee"
  },
  "github": {
    "user": "your-github-username",
    "repo": "workbuddy-skills",
    "branch": "main",
    "remote_name": "origin"
  }
}
EOF
```

> ⚠️ `config.json` 含用户名等敏感信息，已被 `--exclude=config.json` 排除在同步/打包范围外，不会上传到远程仓库。
