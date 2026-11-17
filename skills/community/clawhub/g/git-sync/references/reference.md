# git-sync 完整参考手册

> CLI 命令速查、路径变量、排除列表、文件结构规范。

---

## Git 操作 Python 调用规范

> ⚠️ **关键**：所有 Git 操作必须通过 `run_git()` 函数调用，**禁止**直接使用 `subprocess.run(["git", ...])`，否则会触发 CredentialHelperSelector 弹窗。

### 核心函数：`run_git()`

```python
def run_git(*args, workdir=None, check=True):
    """
    运行 git 命令，完全静默不弹 UI。
    关键：-c credential.helper= 覆盖所有配置文件，
          _git_env() 注入 GIT_CONFIG_COUNT，彻底阻止弹窗。
    """
    env = _git_env()
    si = None
    if os.name == "nt":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        si.wShowWindow = 0  # SW_HIDE
    cmd = ["git",
           "-c", "credential.helper=",
           "-c", "credential.https://gitee.com.provider=",
           "-c", "credential.https://github.com.provider=",
           *[str(a) for a in args]]
    return subprocess.run(cmd, cwd=str(workdir or WORK_REPO),
                         capture_output=True, encoding="utf-8",
                         check=check, env=env,
                         stdin=subprocess.DEVNULL,
                         startupinfo=si)
```

### 核心函数：`_git_env()`

```python
def _git_env(base_env: dict = None) -> dict:
    """
    构造完全静默的 git 环境变量字典。
    用 GIT_CONFIG_COUNT 注入 credential.helper=（空=禁用），
    优先级高于所有配置文件，覆盖所有子进程（含 Python 脚本内调 git）。
    """
    env = base_env.copy() if base_env else os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "credential.helper"
    env["GIT_CONFIG_VALUE_0"] = ""
    return env
```

### 核心函数：`run_python()`

```python
def run_python(script: Path, *args, capture=False, check=True):
    """运行 scripts/ 下的 Python 辅助脚本"""
    env = _git_env()  # 关键：Python 脚本内调 git 也会继承这个环境
    env["PYTHONUTF8"] = "1"
    cmd = [sys.executable, str(script), *[str(a) for a in args]]
    return subprocess.run(cmd, capture_output=capture, encoding="utf-8",
                         check=check, env=env,
                         stdin=subprocess.DEVNULL)
```

### 正确调用示例

```python
# ✅ 正确：通过 run_git() 调用
r = run_git("remote", "get-url", remote_name, workdir=WORK_REPO, check=False)
raw_url = r.stdout.strip()

r = run_git("push", remote_name, branch, workdir=WORK_REPO, check=False)

r = run_git("pull", remote_name, branch, "--rebase",
              workdir=WORK_REPO, check=False)

# ❌ 错误：直接 subprocess.run(["git", ...]) 会弹窗！
r = subprocess.run(["git", "push", "origin", "main"], ...)  # 会触发 CredentialHelperSelector
```

### 弹窗根因说明

| 原因 | 说明 |
|------|------|
| `credential.helper=helper-selector` | PortableGit system config 自带，GUI 弹窗来源 |
| `GIT_TERMINAL_PROMPT=0` 不够 | 只抑制终端提示，不抑制 GUI 弹窗 |
| per-url 配置 `credential.https://gitee.com.provider=generic` | 优先级高于 global，也会触发弹窗 |
| Python 脚本内调 `subprocess.run(["git", ...])` | 没继承 `-c credential.helper=` 参数 |

---

## 错误码与错误消息说明（AI 必读）

### 为什么需要错误消息标准化

`_push_with_cred_url()` 和 `_pull_with_cred_url()` 返回的错误消息已通过 `_classify_push_error()` 标准化为**中文描述**，不再直接暴露原始 stderr（如 443 超时）。

### 错误消息速查表

| 类别 | 错误消息前缀 | 含义 | AI 建议 |
|------|-------------|------|---------|
| 网络超时 | `⏱️ 网络超时` | 连接超时（443），常见于 GitHub 被墙 | 询问用户是否重试，或建议使用代理 |
| DNS 失败 | `🌐 DNS 解析失败` | 域名无法解析 | 检查网络，稍后重试 |
| 连接被拒 | `🔒 连接被拒绝` | 服务器端口不可达 | 检查网络/防火墙 |
| 连接重置 | `🔌 连接被重置` | 中间设备中断连接 | 稍后重试 |
| 网络不可达 | `📡 网络不可达` | 无网络连接 | 检查网络 |
| SSH 失败 | `🔑 SSH 密钥认证失败` | 公钥被拒绝 | 检查 SSH 配置 |
| 认证失败 | `🔑 认证失败` | 用户名/密码/Token 错误 | 检查凭证 |
| 推送被拒绝 | `🔄 推送被拒绝` | 远程有未拉取的更新 | 已自动执行 pull --rebase 重试 |
| 未知错误 | `❌ 推送失败` | 未匹配到已知模式 | 查看具体错误文本 |

### AI 处理错误的原则

1. **443 超时 ≠ 不可恢复**：应询问用户"GitHub 推送失败（超时），是否重试？"
2. **认证失败 ≠ 代码问题**：应提示用户检查 `~/.git-credentials`
3. **推送被拒绝 ≠ 数据丢失**：已自动执行 pull --rebase 重试逻辑
4. **不要在日志中记录原始错误码**：使用 `log()` 函数的 `err` 级别记录标准化消息

### 彻底解决方案（三管齐下）

1. **`run_git()` 加 `-c credential.helper=`** — 命令行参数优先级最高，覆盖所有配置层
2. **`_git_env()` 注入 `GIT_CONFIG_COUNT`** — 覆盖所有子进程（含 Python 脚本内调 git）
3. **清除 system/global config 中的 `helper-selector`**（一次性操作）：
   ```bash
   git config --system --unset credential.helper
   git config --global --unset credential.helper
   git config --global credential.helper store
   ```

### 凭证管理

```python
def _get_cred_url(host: str) -> str:
    """从 ~/.git-credentials 读取指定 host 的凭证，嵌入 URL"""
    cred_file = Path.home() / ".git-credentials"
    if not cred_file.exists():
        return ""
    for line in cred_file.read_text().splitlines():
        if host in line and "@" in line:
            return line.strip()
    return ""

def _push_with_cred_url(remote_name: str, branch: str = "main") -> tuple:
    """用凭证嵌入 URL 直接 push，完全绕开 CredentialHelperSelector"""
    r = run_git("remote", "get-url", remote_name,
                 workdir=WORK_REPO, check=False)
    raw_url = r.stdout.strip()
    parsed = urlparse(raw_url)
    host = parsed.hostname or ""

    cred_url = _get_cred_url(host)
    if not cred_url:
        return False, f"找不到 {host} 的凭证，请检查 ~/.git-credentials"

    # 如果 cred_url 缺少路径，从 raw_url 补全
    parsed_cred = urlparse(cred_url)
    if not parsed_cred.path or parsed_cred.path == '/':
        parsed_raw = urlparse(raw_url)
        cred_url = f"{parsed_cred.scheme}://{parsed_cred.netloc}{parsed_raw.path}"

    # 临时覆盖 remote URL（含凭证），push 完立刻恢复
    run_git("remote", "set-url", remote_name, cred_url,
             workdir=WORK_REPO, check=False)
    try:
        r = run_git("push", remote_name, branch,
                     workdir=WORK_REPO, check=False)
        if r.returncode == 0:
            return True, ""
        return False, r.stderr.strip() or r.stdout.strip()
    finally:
        run_git("remote", "set-url", remote_name, raw_url,
                 workdir=WORK_REPO, check=False)
```

---

## git-sync.py CLI 参数

```bash
python git-sync.py <name> [--skip-market] [--market-only] [--pypi] [--release]
```

| 参数 | 说明 |
|------|------|
| `--skip-market` | 跳过 ClawHub / SkillHub 市场发布 |
| `--market-only` | 仅发布到市场，不执行同步 |
| `--pypi` | 发布到 PyPI（仅 agent 有效） |
| `--release` | 创建 Release：打 tag + 推双平台 + 建 GitHub/Gitee 发行版 |

## manifest.py 子命令速查

`manifest.py` 是独立 CLI，管理维护清单（manifest.json），不污染 git-sync 主流程。

### 清单条目结构（v2.37.0 多仓库）

```json
{
  "repos": {
    "<技能仓库名>": {
      "items": {
        "my-agent": {
          "type": "agent",
          "source_path": "C:/Users/你的用户名/你的开发目录/my-agent",
          "repo_path": "my-agent",
          "added_at": "2026-07-21",
          "uploaded": true,
          "gitee_ok": true,
          "github_ok": true,
          "version": "1.0.0",
          "gitee_version": "1.0.0",
          "github_version": "1.0.0",
          "note": ""
        }
      }
    }
  }
}
```

| 字段 | 说明 | 自动填充 |
|------|------|---------|
| `type` | `skill` 或 `agent` | 必需 |
| `source_path` | 源绝对路径（开发目录） | skill → `$SKILLS_DIR/<name>/`（技能安装目录），agent → 开发目录，可用 `--source-path` 覆盖 |
| `repo_path` | 仓库内相对路径（多仓库模型下为顶层相对路径） | skill → `<name>/`（技能仓库顶层），agent → `<name>/`（智能体仓库顶层），可用 `--repo-path` 覆盖 |
| `added_at` | 添加日期 | 自动 |
| `uploaded` / `gitee_ok` / `github_ok` | 推送状态 | 自动更新 |
| `version` / `gitee_version` / `github_version` | 版本号 | 自动更新 |

### 命令参考

> 仓库名参数：使用 `config.json` 注册表中实际配置的仓库名（v2.37.0 多仓库，下例用 `<repo>` 占位）。

```bash
# ── 查询类 ──
python manifest.py list                              # 列出所有条目
python manifest.py list <repo>                       # 按仓库过滤（如 config 中配置的任意仓库名）
python manifest.py check <repo> my-skill             # 是否在清单内（退出码: 0=双 ok, 1=部分, 2=未找到）
python manifest.py version <repo> my-skill           # 查询版本号

# ── 更新类 ──
python manifest.py add <repo> my-skill --type skill                  # 加入（默认路径自动填充）
python manifest.py add <repo> my-agent --type agent                  # agent 类型
python manifest.py add <repo> my-agent --type agent --source-path "C:/path/to/dev"  # 自定义源路径
python manifest.py add <repo> my-agent --type agent --repo-path "custom"            # 自定义仓库路径
python manifest.py add <repo> my-skill --type skill --uploaded      # 加入并标记已上传
python manifest.py remove <repo> my-skill                           # 从清单删除
python manifest.py version <repo> my-skill 1.9.0                    # 更新版本号（双平台）
python manifest.py version <repo> my-skill 1.9.0 --platform gitee   # 仅更新码云
python manifest.py set-uploaded <repo> my-skill --platform gitee    # 标记平台已上传
python manifest.py set-uploaded <repo> my-skill --platform both     # 标记双平台已上传

# ── 同步类 ──
python manifest.py diff <repo>                        # 对比清单(uploaded=true) vs 仓库实际文件
python manifest.py sync-readme <repo>                 # 根据仓库实际文件全量重新生成 README.md
```

### 三单一致模型

**三单 = 三个"单"：**

| # | 单 | 内容 | 维护方式 |
|---|----|------|---------|
| 第一单 | **本地源文件** | `_meta.json` version + `SKILL.md` frontmatter version | 开发者手动维护（两者必须一致） |
| 第二单 | **远程仓库实际文件** | 推送到 Gitee/GitHub 后，目标仓库 `<name>/_meta.json`（多仓库模型顶层）中的 version | 由 git-sync 推送，与本地一致 |
| 第三单 | **维护清单** | `manifest.json` 中的 `version` / `gitee_version` / `github_version` | 推送成功后自动更新 |

**三单一致的完整语义：**

```
同步前（本地准备阶段）：
  _meta.json version = SKILL.md frontmatter version         ← 本地版本一致
  manifest.json version < 待推送版本                         ← 清单版本低于本地，允许升级

同步中（推送阶段）：
  不需要管版本号 — 仓库实际文件 version = 推送时的本地 version

同步后（推送成功）：
  本地 _meta.json version = 远程仓库 version = 清单 version  ← 三单一致
  README.md = 仓库实际内容（由 sync-readme 全量生成，永远一致）
```

**上传状态标记：**

| 字段 | 含义 |
|------|------|
| `gitee_ok=true` | Gitee 平台三单一致（Gitee 仓库 version = 清单 version = 本地 version） |
| `github_ok=true` | GitHub 平台三单一致（同上） |
| `uploaded=true` | 双平台均已三单一致（`gitee_ok AND github_ok`） |

**结构示意：**

```
本地源文件 (_meta.json + SKILL.md frontmatter version 一致)
    ↓ 推送
远程仓库 (<技能仓库名>/<name>/ 或 <智能体仓库名>/<name>/ 实际文件)
    ↓ 推送成功后更新
维护清单 (manifest.json)
    ├─ gitee_ok=true  → Gitee 三单一致
    ├─ github_ok=true → GitHub 三单一致
    └─ uploaded=true  → 双平台三单一致

README.md（技能列表 + 目录树）
    └─ 由 sync-readme 全量生成，永远 = 仓库实际内容
```

> **不会出现 README 有但仓库没有的情况。**

---

## 路径变量说明（v2.37.0 多仓库）

> **统一管理机制**：所有路径在 `scripts/_paths.py` 统一定义（唯一来源），其他脚本一律 `from _paths import ...` 引用，不各自写死路径。仓库路径（`WORK_REPO` 等）由 `config.json` 的 `repos` 注册表配置 + `get_work_repo(type)` 动态解析。

| 变量 | 来源 | 说明 |
|------|------|------|
| `SKILLS_ROOT` | `_paths.py`（`SKILL_DIR.parent`） | 技能安装根目录（`SKILL_DIR` 即本技能所在目录） |
| `WORK_REPO` | `_paths.py` → `get_work_repo(type)`（从 `config.json` 注册表解析） | Git 工作仓库（推送目标），skill → 技能仓库、agent → 智能体仓库 |
| `DIST_DIR` | `_paths.py`（`SKILLS_ROOT / ".dist"`） | ZIP 统一输出目录 |
| `MANIFEST_FILE` | `_paths.py`（`SKILLS_ROOT/.standardization/git-sync/data/manifest.json`） | 维护清单文件路径 |
| `CONFIG_FILE` | `_paths.py`（`SKILLS_ROOT/.standardization/git-sync/data/config.json`） | 平台配置（repos 注册表） |
| `TEMP_DIR` | `_paths.py`（`STD_DIR / "temp"`） | 决策文件等临时文件目录 |

## ZIP 打包：LLM 动态过滤（v2.26+）

自 v2.26.0 起，ZIP 包的排除列表由 **LLM 文件过滤器**（`step_llm_file_filter()`）动态生成，不再使用硬编码的排除模式列表。仅保留 Windows 保留名 `nul` 的硬排除。

LLM 会在文件同步步骤前审核文件清单，保留核心代码文件（`.py`、`.md`、配置、许可等），排除运行时缓存（`__pycache__`、`*.pyc`）、日志、操作系统元文件（`.DS_Store`、`Thumbs.db`）等非必要文件。

如果需要手动干预排除逻辑，请修改 `step_llm_file_filter()` 的 LLM prompt 模板（`git-sync.py`）。

## Skill 标准目录结构

```
<skill-name>/
├── SKILL.md                  # [必填] 技能主文件
├── _meta.json                # [必填] 元数据（5字段）
├── references/                     # [可选] 渐进式 MD 辅助文档
│   ├── guide.md
│   ├── examples.md
│   ├── reference.md
│   └── ...
├── scripts/                  # [可选] Python/Shell 脚本
│   ├── *.py
│   ├── *.sh
│   └── spec/
├── assets/                   # [可选] 静态资源
└── tests/                    # [可选] 测试文件
```

**根目录仅允许 SKILL.md 和 _meta.json。**

---

## 敏感信息过滤详细规则

### 检测规则完整表

| 类型 | 正则模式示例 | 严重度 | 说明 |
|------|-------------|--------|------|
| 邮箱地址 | `\w+@\w+\.\w+` | 🔴 critical | 任何 email 格式 |
| Token / API Key | `token=`, `api_key=`, `secret=` | 🔴 critical | 键值对形式的密钥 |
| 私钥内容 | `-----BEGIN .* PRIVATE KEY-----` | 🔴 critical | PEM 格式私钥 |
| 内网 IP | `10\.\d+`, `172\.(1[6-9]|2\d|3[01])\.`, `192\.168\.` | 🟡 medium | RFC1918 私有地址 |
| 本地绝对路径 | `[A-Z]:\\Users\\`, `/home/`, `/Users/` | 🟡 medium | 用户主目录路径 |
| 配置用户名 | config.json 中 author/gitee.user/github.user 的值 | 🟢 low | 来自配置的用户名 |

> **注意**：`_meta.json` 的 `author` 字段是署名，默认不脱敏。

### 运行模式（v2.24.2+ — 全自动 LLM 决策）

自 v2.24.2 起，敏感扫描已完全自动化，由 LLM 决策每条敏感信息是否脱敏，无需人工交互。

| 模式 | 配置方式 | 行为 |
|------|---------|------|
| **自动 LLM 决策**（默认） | 不配置或 `prompt` | 扫描后 LLM 自动分类每项发现：public_docs 中的署名/path 保留；Token/私钥 自动脱敏；邮箱/路径 按 context 判断 |
| **总是脱敏** | `GIT_SYNC_SENSITIVE_MODE=always-sanitize` | 自动全部脱敏（非交互，用于 ZIP 包） |

### LLM 自动决策规则

LLM 接收扫描发现列表后，按以下原则自动判断：

| 敏感类型 | LLM 决策倾向 | 示例 |
|----------|-------------|------|
| 邮箱地址 | 公开文档中的署名邮箱 → 保留；代码中的测试邮箱 → 保留；疑似个人邮箱 → 脱敏 | `user@example.com` 在 LICENSE 中 → 保留 |
| Token / API Key | 一律脱敏 | `api_key=sk-xxx` → 替换为 `<REDACTED>` |
| 私钥内容 | 一律脱敏 | PEM 格式密钥 → 替换 |
| 内网 IP | 脱敏 | `192.168.1.1` → `<REDACTED_IP>` |
| 本地绝对路径 | public_docs 中的路径 → 保留；代码中硬编码 → 脱敏 | `C:\Users\USERNAME` 在文档中 → 保留 |
| 配置用户名 | 保留（来自 config.json 的 author/gitee.user） | `wUwproject` → 保留 |

### 打包时行为

```
源文件（$SKILLS_DIR/my-skill/）  ← 不变
     ↓ 复制到临时副本
临时副本（/tmp/xxx/）                     ← 执行脱敏操作
     ↓ 打包
输出 ZIP → .dist/my-skill-v1.0.0.zip
     ↓ 清理
临时副本删除
```

同步到仓库时，脱敏作用于工作仓库副本（目标仓库 `<name>/` 目录，仓库路径由 `config.json` 注册表决定），源文件同样不变。
