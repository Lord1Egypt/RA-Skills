# git-sync 完整使用指南

> 本文档是 SKILL.md 的渐进式补充，包含完整的执行流程、步骤详解和配置说明。

---

## 完整执行流程（步骤 0 → 9）

### 步骤 0：参数解析 + 类型检测（v2.25+）

| 操作 | 说明 |
|------|------|
| 参数解析 | `--skip-market` / `--market-only` / `--pypi` / `--release` |
| `all` 模式 | `git-sync all` 遍历配置的全部仓库项目（仓库名/路径由 `config.json` 的 `repos` 注册表决定） |
| 类型检测 | 自动识别 skill（`_meta.json`）或 agent（`__init__.py`） |
| 版本号读取 | skill→`_meta.json`，agent→`__init__.py` 中的 `__version__` |

### 步骤 0.7：版本号比对（v1.6+）

与仓库中已有版本对比，决定是否需要同步：版本相同跳过，本地更新则正常升级。

### 步骤 1：维护清单检查（v1.3+）

同步前自动检查 `manifest.json`。

### 步骤 2~3.5：标准校验（仅 skill）

| 步骤 | 操作 | 适用 |
|------|------|------|
| 2 | `_meta.json` 标准化校验 | skill 仅 |
| 3 | SKILL.md 规范审查（只读） | skill 仅 |

### 步骤 3.7：LLM 文件过滤器（v2.29.0，替换硬编码黑名单）

Python 扫描源目录文件树 + 自动查找规则文件（`blueprint*`, `*rules*`, `blueprints/`），生成扫描报告后**全量打印文件列表 + 排除规则到 stdout**，要求调用方（AI 助手）在回复中输出决策 JSON。决策写入 `.file_filter_{name}.json.decisions.json`，**重新运行 git-sync 后读取该文件继续同步**。

交互流程：
1. git-sync 扫描文件 → 打印完整文件列表 + 排除规则 → 退出（返回 None）
2. 调用方（AI 助手）看到输出后，审核文件列表，按规则决定保留/排除
3. 调用方（AI 助手）在回复中输出 `{"allow": ["path/to/file.py", ...]}`，**同时写入决策文件**
4. 重新运行 git-sync → 读取决策文件 → 只复制允许的文件 → 继续后续步骤

| 环境 | 行为 |
|------|------|
| 有决策文件 | 直接读取，跳过审核 |
| 无决策文件 | 打印审核指令，等待调用方（AI 助手）回复决策 |
| 决策文件解析失败 | 默认保留所有文件 |

> ⚠️ **决策文件写入规范（2026-08-09 实战教训，必须遵守）**
>
> **🔥 铁律第一条：让位 → 写决策 → 重跑，必须在同一条 Bash 命令里完成，一次跑完，禁止拆成多条命令。**
>
> 2026-08-09 git-sync 自推送实战：拆成"先跑让位 → 再单独写决策 → 再重跑"三条命令时，第二次命令里 scan/resume 文件**凭空消失**（git-sync 每次运行会重建/清理 temp），导致反复"决策文件存在却读不到"→ 重试 N 次全部失败；合并为一条命令 `让位 && 写决策 && 重跑` 后**一次通过**。这是已确认的根因规律，不是偶然。
>
> 决策文件**必须用 git-sync 自己的路径函数写入**，严禁用 Write 工具或跨进程手写路径：
>
> ```bash
> # ✅ 正确姿势：一条 Bash 命令完成全流程（cd 到 git-sync/scripts 后）
> python git-sync.py <name> --skip-market ; \
> python -c "import sys,json; sys.path.insert(0,'.'); from _paths import temp_filter_decisions_path; dec=temp_filter_decisions_path('<name>'); dec.write_text(json.dumps({'allow':[...],'exclude':[...]},ensure_ascii=False))" ; \
> python git-sync.py <name> --skip-market
> ```
>
> ```python
> # ✅ 决策内容生成（在 git-sync scripts 目录下，import _paths 用其路径函数写入）
> import sys; sys.path.insert(0, r'<GIT_SYNC_DIR>/scripts')
> from _paths import temp_filter_decisions_path
> dec = temp_filter_decisions_path('<name>')
> dec.write_text(json.dumps({'allow': [...], 'exclude': [...]}), encoding='utf-8')
> ```
>
> ❌ **错误做法（会导致"决策文件存在却读不到"→ 反复让位死循环）**：
> - **把"让位/写决策/重跑"拆成多条独立 Bash 命令**（temp 文件跨命令被重建/清理，必现"文件消失"）
> - 用 Write 工具写决策文件（写入可能被沙箱隔离，git-sync 进程看不到）
> - 手写硬编码路径（`C:\Users\...\temp\file_filter_xxx.decisions.json`），一旦 `_paths.py` 的 `TEMP_DIR` 解析不同则路径不一致
> - 跨 Bash 进程写入后立即重跑（沙箱视图不同，文件"消失"）
>
> **症状识别**：重跑 git-sync 仍显示"已让位（exit 3）：请写入决策文件后重跑"，但 `ls` 明明能看到决策文件——这就是命令拆分/路径/沙箱不一致，**合并为一条命令**并按 ✅ 方式重写决策文件即可。**在 git-sync 脚本环境下（`from _paths import ...`）写入并验证 `dec.exists()` 为 True，与重跑放在同一条命令里，一次通过。**

### 步骤 4：同步文件

仅复制 LLM 允许列表中的文件到目标仓库（按 `get_work_repo(type)` 解析，v2.37.0 多仓库模型：skill → 技能仓库、agent → 智能体仓库，具体路径见 `config.json` 注册表）。

### 步骤 4.5：LLM 脱敏

扫描已同步文件中的敏感信息（邮箱/token/IP），LLM 自动决策 keep/sanitize，执行脱敏。

> ⚠️ **脱敏决策写入规范**：与步骤 3.7 相同——**同样必须在同一条 Bash 命令里完成让位→写决策→重跑**，用 `_paths.py` 的 `temp_scan_decisions_path('<name>')` 写入，`{"相对路径": "keep"|"sanitize"}` 格式。**critical 级发现（Token/密钥）必须 sanitize，公开署名（如作者 wUwproject）与第三方库作者邮箱可 keep。** 脱敏是强制安全门禁（v2.31.0 起不可跳过），决策文件缺失会反复让位。

### 步骤 5：更新 README.md（skill + agent）

按仓库类型扫描：技能仓库扫技能目录，智能体仓库扫智能体目录（仓库路径由 `config.json` 注册表决定），生成技能表格 + 智能体表格。

### 步骤 6：提交并推送到双平台

Gitee + GitHub，失败自动 pull --rebase 重试。

### 步骤 6.7：更新清单上传状态

### 步骤 7：生成 ZIP 安装包（仅 skill）

### 步骤 7.5：打包前敏感扫描

### 步骤 8：发布到平台（非静默，直接输出）

| 类型 | 平台 | 命令 |
|------|------|------|
| skill | ClawHub | `npx clawhub publish`（shell=True，已知 CLI bug）|
| skill | SkillHub | `skills_store_cli.py publish --version <ver>`（必须传 --version）|
| agent | PyPI | 隔离构建 → `twine upload --disable-progress`（--pypi 标志）|

### 步骤 9：创建 Release（--release 标志）

打 tag + 推双平台 + 创建 GitHub Release + Gitee 发行版。
- tag 格式：skill=`{name}-v{ver}`，agent=`v{ver}`
- 源码包由 GitHub/Gitee 自动从 tag 生成（Source code zip/tar.gz）
- 同时推送 `pypi/{type}/{name}/{version}` 触发 tag，供 GitHub Actions Trusted Publisher 工作流使用
- 仅 `--release` 标志时执行，平时同步不创建 Release

### 步骤 1：_meta.json 版本同步

同步 version 字段，补全缺失的 name/description，**保留所有既有字段**（不删除任何字段）。

| 标准字段 | 缺失时处理 |
|---------|-----------|
| `name` | 使用目录名 |
| `version` | 使用传入的 version 参数 |
| `description` | 从 SKILL.md 提取 |
| `author` | 从 config.json 读取（缺省为 `your-name-here`） |
| `tags` | 设为空数组 `[]` |

### 步骤 1.5：SKILL.md 内联审计（v2.6.31+）

- **方式**：`git-sync.py` 内置 `step_skill_audit()`，作为同步工作流的一部分自动执行
- **检查项**：版本一致性（`_meta.json` vs `SKILL.md` frontmatter）+ R-23 脚本引用规范
- **模式**：纯警告不阻断（始终 exit(0)）
- **输出**：终端打印检查报告（ERROR=0 WARN=N PASS=M）

### 步骤 2：同步文件到工作仓库

将技能从 `$SKILLS_DIR/<skill-name>/` 同步到目标仓库（`get_work_repo(type)` 返回的仓库路径下的 `<name>/` 目录，具体路径由 `config.json` 注册表声明）。

### 步骤 3：全量重新生成 README.md

> **关键原则**：README.md = 仓库实际内容，不手动维护。

从仓库实际目录扫描，全量替换 README.md 中的技能列表表格和目录结构（多仓库模型下各仓库维护各自 README）。

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

1. 复制 ZIP 到统一目录 `$SKILLS_DIR/.dist/`
2. 自动生成/刷新 `index.html` 索引页（含 file:// 链接 + 文件大小 + 时间）
3. 自动打开 dist/ 目录（Windows explorer / macOS open / Linux xdg-open）

> **每次执行完毕后 AI 必须主动调用 `preview_url` 打开 index.html。**

---

## config.json 完整配置模板（v2.37.0 多仓库模型）

> 实际配置位于数据目录（`$SKILLS_DIR/.standardization/git-sync/data/config.json`），含 repos 注册表。**下方为示例结构，仓库名/路径/用户名均需按用户实际配置修改。**

```json
{
  "author": "你的作者名",
  "email": "你的邮箱（可选，用于 git commit author）",
  "gitee": {
    "user": "你的码云用户名"
  },
  "github": {
    "user": "你的 GitHub 用户名"
  },
  "repos": {
    "示例仓库名_skills": {
      "type": "skills",
      "path": "C:/Users/你的用户名/你的技能仓库本地路径",
      "gitee": { "user": "你的码云用户名", "repo": "技能仓库名" },
      "github": { "user": "你的 GitHub 用户名", "repo": "技能仓库名" },
      "readme": { "title": "技能仓库标题", "description": "仓库描述", "repo_name": "技能仓库名", "banner": "历史存档说明（可选）" }
    },
    "示例仓库名_agents": {
      "type": "agents",
      "path": "C:/Users/你的用户名/你的智能体仓库本地路径",
      "gitee": { "user": "你的码云用户名", "repo": "智能体仓库名" },
      "github": { "user": "你的 GitHub 用户名", "repo": "智能体仓库名" },
      "readme": { "title": "智能体仓库标题", "description": "仓库描述", "repo_name": "智能体仓库名", "banner": "历史存档说明（可选）" }
    }
  },
  "source_overrides": {},
  "gitee_token": "可选：Gitee API token"
}
```

**关键字段说明**：

| 字段 | 影响范围 |
|------|---------|
| `author` | `_meta.json` 默认作者名；敏感扫描中的用户名检测基准 |
| `email` | git commit 的 author email（`git-sync.py` 中的 `step_commit_and_push()` 使用） |
| `repos.<name>.type` | 仓库类型：`skills`（skill 项目）或 `agents`（agent 项目），`get_repo_name()` 按此匹配项目归属 |
| `repos.<name>.path` | 仓库本地路径，`get_work_repo(type)` 据此返回 |
| `repos.<name>.gitee/github` | 各平台用户名 + 仓库名（推送目标） |
| `repos.<name>.readme` | README 生成配置（标题、描述、banner 存档说明） |
| `gitee_token` | Gitee API token（Release 创建等 API 操作） |

---

## 跨平台环境适配

> 本技能优先用 `rsync` 做本地文件同步；rsync 不可用时（如部分 Windows Git 环境）自动 fallback 到 Python 完整流程（`git-sync.py`），功能等价，无需手动干预。

### 环境矩阵

| 环境 | rsync 是否可用 | 说明 |
|------|----------------|------|
| Linux / macOS | ✅ 自带 | 无需额外操作 |
| Git for Windows 完整版 | ✅ 自带 | 位于 Git 安装目录的 usr/bin/ 下 |
| **Windows 便携版 Git** | ❌ 不含 | 需手动安装（见下方） |
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
C:\Users\USERNAME\.workbuddy\binaries\python\...\python.exe: can't open file 'c:\\c\\Users\\...'
```

**解决方案（任选其一）：**

| 方案 | 操作 | 推荐度 |
|------|------|--------|
| **A. 安装 rsync** | 见下方「各平台安装 rsync」| ⭐⭐⭐ 最推荐 |
| **B. 用 MSYS2 版 Python** | `pacman -S python`（MSYS2 内）| ⭐⭐ |
| **C. 手动调用 Python 时传 Windows 路径** | `python sync_with_exclude.py "C:\..." "C:\..."` | ⭐ 临时 |

### 各平台安装 rsync

#### Windows（便携版 Git 环境）

**方式一：下载独立 rsync.exe 放到 Git 的 usr/bin**

```bash
# 在 Git Bash 中执行，下载 rsync.exe 到 Git 安装目录的 usr/bin/
cd $GIT_INSTALL/usr/bin/
# 从 Git for Windows 获取 rsync 工具
# 在 Git Bash 中执行：
cd $GIT_INSTALL/usr/bin/
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

本机 rsync 不可用，实际走 `git-sync.py`（`git-sync.sh` 会自动切换）。支持以下用法：

```bash
# 基础用法（自动识别类型，版本号自动从 _meta.json/__init__.py 读取）
python git-sync.py <name>

# 跳过市场发布
python git-sync.py <name> --skip-market

# 只发市场不推 git
python git-sync.py <name> --market-only

# 发布到 PyPI（仅 agent）
python git-sync.py <name> --pypi

# 创建 Release
python git-sync.py <name> --release

# 全部项目
python git-sync.py all

# 组合使用
python git-sync.py rag-assistant --pypi --release --skip-market
```

> ⚠️ 注意：`git-sync.py` 不接收版本号位置参数（版本自动读取），`--skip-market` 同时跳过市场与 PyPI。

---

## 配置说明（LLM 参考）

> 本技能的配置存放在数据目录，脚本自动读取，无需手动创建文件。**完整结构见上文「config.json 完整配置模板（v2.37.0 多仓库模型）」**，此处仅补充定位与字段要点。

### 配置文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| `config.json` | `$SKILLS_DIR/.standardization/git-sync/data/config.json` | 平台用户名、repos 注册表、gitee_token 等配置 |
| `manifest.json` | `$SKILLS_DIR/.standardization/git-sync/data/manifest.json` | 技能同步状态清单（按 repos 组织条目） |

### config.json 字段要点（v2.37.0 多仓库）

| 字段 | 说明 |
|------|------|
| `author` | `_meta.json` 默认作者名；敏感扫描中的用户名检测基准 |
| `repos` | **核心注册表**：每个仓库条目含 `type`（skills/agents）、`path`、`gitee`/`github`（user+repo）、`readme` 配置 |
| `repos.<name>.type` | 项目类型→仓库归属的唯一映射（skill→skills 仓库、agent→agents 仓库） |
| `gitee_token` | Gitee API token（Release 创建等 API 操作） |
| `source_overrides` | 个别项目的源路径覆盖（manifest 未命中时用） |

### 脚本读取方式

所有 `git-sync` 脚本**不从 `_paths.py` 之外的任何地方读取路径**——路径常量在 `scripts/_paths.py` 统一定义，脚本直接引用：

```python
# scripts/_paths.py（唯一路径来源）
SKILLS_ROOT   = SKILL_DIR.parent                       # 技能安装根目录
CONFIG_FILE   = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "config.json"
MANIFEST_FILE = SKILLS_ROOT / ".standardization" / "git-sync" / "data" / "manifest.json"
WORK_REPO     = get_work_repo(type)                    # 从 config.json 注册表解析

# 其他脚本一律：
from _paths import CONFIG_FILE, MANIFEST_FILE, WORK_REPO
```

### 初始化配置

首次使用本技能前，确保数据目录中存在 `config.json`（**必须含 repos 注册表**，参考上文完整模板）：

```bash
mkdir -p $SKILLS_DIR/.standardization/git-sync/data
# 将上文「config.json 完整配置模板」写入该路径，替换占位符
```

> ⚠️ `config.json` 含用户名等敏感信息，已被排除在同步/打包范围外，不会上传到远程仓库。
