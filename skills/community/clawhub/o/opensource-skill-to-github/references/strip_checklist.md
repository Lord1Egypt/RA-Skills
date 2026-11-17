# 11 条剔除清单 + 字面替换映射

> 完整清单，Step 3 字面层 grep 命中后逐项处理参考。
> 复杂或大量字面替换的细节场景，引用既有 skill `openclaw-skill-opensource-fork-strip-internal-and-token-hygiene` 做深度处理。
>
> ⚠️ **保持一致**：`scripts/strip_scan.sh` 的 KEYWORDS 默认词表与本表「必删/必改」+「字面替换映射」对齐。修改任一处时另一处同步更新；用户可通过 `OSG_STRIP_KEYWORDS` 覆盖默认词表。

## 必删 / 必改 11 条

| # | 项 | 处理 |
|---|---|---|
| 1 | `sign.key`、`skill_meta.json`、`*.json.md` | 删（内部签名 / agent 产物，`fork.sh` 已自动删） |
| 2 | `.install-source.json` | 删（内部安装来源标记，`fork.sh` 已自动删） |
| 3 | `__pycache__/`、`*.pyc`、`.skill-data/` | 删（agent 运行时缓存，`fork.sh` 已自动删） |
| 4 | `USAGE.md`（若与 SKILL.md 内容重复） | 删（避免双语维护成本，glic-check 实证） |
| 5 | 硬编码内网 host（`fe.devops.xiaohongshu.com` / `codewiz.devops.xiaohongshu.com` / `xhscdn.com`） | 改运行时拼接或环境变量 |
| 6 | 硬编码内网路径（`/home/node/.openclaw/workspace` / `/home/node/sso.json` / `~/.openclaw/`） | 改 `pwd` 或用户传参或环境变量 |
| 7 | 内网概念引用（`Agent` / `OpenClaw` / `小红书` / `XHS_*`） | 改通用名（`PROJECT_NAME` / `<your-tool>`），但 `OpenClaw` 作为公开品牌名可保留 |
| 8 | 内网邮箱示例（`@xiaohongshu.com`） | 换 `user@example.com` |
| 9 | 内网 gitignore 产物路径（`.skill-data` / `.clawhub` / `.http`） | 删，改通用 `id_rsa` / `*.p12` / `certs/*.key` |
| 10 | 内网用户姓名 / 花名 / UID | 删，统一为用户拍板的对外身份（通过 `OSG_AUTHOR_NAME` / `OSG_STRIP_WHITELIST` 注入） |
| 11 | 业务系统兼容兜底（`XHS_ENV` / `REGION` / `NAMESPACE`） | 不保留，改成用户可配置清单（`--probe-env "A,B,C"`） |

## 字面替换映射（强约束 2）

| 内网字面 | 开源替换 | 位置 |
|---|---|---|
| `~/.openclaw/workspace` 默认路径 | `${WORKSPACE_DIR:-$PWD}` | 路径解析段 |
| `/home/node/.token/sso_token.json` | `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` 环境变量 | 身份读取段 |
| `.redInfo` 读取 | 删整段 | 身份读取段 |
| `IDENTITY.md` 解析 | 删，改 `basename "$WORKSPACE_DIR"` | 项目名探测 |
| `AGENT_NAME` 变量 | `sed -i s/AGENT_NAME/PROJECT_NAME/g` | 全文 |
| `"OpenClaw Agent"` 文案 | `"project"` 或 `"workspace"` | 所有 echo/info |
| `.skill-data` / `.clawhub` / `.http` / `hub-skill-query` | 通用 `id_rsa` / `*.p12` / `*.keystore` / `**/certs/*.key` | `.gitignore` + `SENSITIVE_PATTERNS` |
| `Linux 容器 CRLF` 等内部语境 | 通用化 | autocrlf 提示 |
| `name@xiaohongshu.com` | `jane@example.com` | 用户提示 |
| `signed_by: <internal-name>` | 删 `sign.key` 整文件 | skill 根 |
| `codewiz.devops.xiaohongshu.com` | 删 `.install-source.json` | skill 根 |

## 通用化关键代码片段

### 路径优先级

```bash
WORKSPACE_DIR="${WORKSPACE_DIR:-$PWD}"
# 不假设 OpenClaw 路径
```

### 项目名探测

```bash
# 旧（内网）:
PROJECT_NAME=$(grep '^name:' IDENTITY.md | awk '{print $2}')

# 新（开源）:
PROJECT_NAME="${PROJECT_NAME:-$(basename "$WORKSPACE_DIR")}"
```

### git 身份读取

```bash
# 旧（内网）: 从 sso_token.json 读
# 新（开源）: 优先 git config，回退环境变量
USER_NAME="${GIT_AUTHOR_NAME:-$(git config user.name 2>/dev/null || echo '')}"
USER_EMAIL="${GIT_AUTHOR_EMAIL:-$(git config user.email 2>/dev/null || echo '')}"
if [[ -z "$USER_NAME" || -z "$USER_EMAIL" ]]; then
  echo "请设置 git user 或 GIT_AUTHOR_NAME/EMAIL 环境变量" >&2
  exit 1
fi
```

### locale 探测（rename-session 实证）

```bash
# 不写死 zh，按 $LC_ALL / $LC_MESSAGES / $LANG 探测
detect_lang() {
  local raw="${LC_ALL:-${LC_MESSAGES:-${LANG:-en_US.UTF-8}}}"
  case "$raw" in
    zh*) echo "zh" ;;
    *)   echo "en" ;;
  esac
}
LANG_DEFAULT="$(detect_lang)"
```
