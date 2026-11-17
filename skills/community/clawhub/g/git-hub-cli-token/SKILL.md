---
name: gh-cli-readonly-agent
v: 1.0.0
desc: AI Agent专用GitHub CLI只读Skill。极致省Token，生产级。
triggers: [gh, github, repo, pr, issue, ci, code search]
---

# GitHub CLI 只读 Skill (Agent专用)

## 0. 核心约束 (HARD RULES)
- **只读**：严禁任何写入/创建/合并/评论/删除操作（见§8黑名单）。
- **省Token**：必带 `--json` 裁剪字段，必带 `--limit` (默认≤10)，必用 `| jq -c` 紧凑输出。
- **超时**：所有 `gh api` 必须通过预置函数 `gh_timed` 调用。
- **缓存**：高频查询必须通过预置函数 `gh_cached` 调用。
- **重试**：网络/限流错误必须通过预置函数 `retry` 包裹。
- **缩写**：全篇使用 `O/R` 代替 `owner/repo`。
- **前置自检**：执行前必须通过 `gh auth status || gh auth login`。
- **Windows CMD**：jq 单引号改为双引号，如 `jq ".content | @base64d"`（CMD 双引号内 `|`、`>` 等特殊符需 `^` 转义）。
- **PowerShell**：推荐单引号包裹 jq 表达式（单引号内可直接写双引号，无需转义），如 `jq -c '.content | @base64d'`；单引号内表示单引号本身写作 `''`。

## 1. 预置环境声明 (Sandbox Pre-installed)
以下函数已在Agent运行时环境预置，直接调用，禁止重新实现：

| 函数签名 | 作用 |
|---|---|
| `gh_timed <args>` | 带30s超时保护的gh调用 |
| `gh_cached <args>` | 带30分钟TTL的脚本层缓存 |
| `retry <args>` | 指数退避重试(最多3次) |
| `gh_read O/R path [ref]` | 读取文件内容并自动base64解码 |
| `gh_tree O/R [depth]` | 获取目录树(默认限制3层，输出去重path列表) |
| `truncate_by_quota O/R path` | 根据TOKEN_QUOTA自适应截断大文件 |
| `gh_default_branch O/R` | 获取默认分支(封装 main→master→API 兜底探测) |

```bash
# === 预置函数实现（bash/Linux-macOS，环境启动时自动加载） ===
gh_timed() { timeout "${GH_TIMEOUT:-30}" gh "$@"; }

gh_cached() {
  local h; h=$(printf '%s' "$*" | (sha256sum 2>/dev/null || shasum -a 256) | cut -c1-16)
  local f="/tmp/gh_${h}.json"
  local mtime; mtime=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null || echo 0)
  if [ -f "$f" ] && [ $(( $(date +%s) - mtime )) -lt 1800 ]; then cat "$f"; else gh "$@" | tee "$f"; fi
}

retry() { for i in 1 2 3; do "$@" && return 0; sleep $((i*i)); done; return 1; }

gh_read() { gh_timed api "repos/$1/contents/$2?ref=${3:-main}" | jq -r '(.content // "") | @base64d'; }

gh_tree() {
  gh_timed api "repos/$1/git/trees/main?recursive=1" \
    | jq -c ".tree[] | select(.type==\"blob\") | .path | split(\"/\")[0:${2:-3}] | join(\"/\")" \
    | sort -u | head -100
}

truncate_by_quota() {
  local quota=${TOKEN_QUOTA:-3000}
  local lines=$((quota / 8))
  [ "$lines" -gt 500 ] && lines=500
  [ "$lines" -lt 50 ] && lines=50
  gh_timed api "repos/$1/contents/$2" | jq -r "(.content // \"\") | @base64d | split(\"\n\") | .[0:$lines] | join(\"\n\")"
}

gh_default_branch() { gh_timed api "repos/$1" | jq -r '.default_branch // "main"'; }
```

### 1.1 Windows / PowerShell 适配（Agent 运行于 pwsh 7 时）
```powershell
function gh_timed { gh @args }  # gh 无原生超时；超时兜底由 sandbox 层或 §9 curl --max-time 承担

function retry {
  # Exponential backoff retry (max 3 attempts), mirrors the bash version.
  param(
    [Parameter(Mandatory = $true, Position = 0)]
    [scriptblock]$Command,
    [int]$MaxAttempts = 3
  )
  for ($i = 1; $i -le $MaxAttempts; $i++) {
    & $Command
    if ($LASTEXITCODE -eq 0) { return $true }
    if ($i -lt $MaxAttempts) { Start-Sleep -Seconds ($i * $i) }
  }
  return $false
}

function gh_cached {
  $key = (($args -join ' ') | Get-FileHash -Algorithm SHA256).Hash.Substring(0,16)
  $f = Join-Path $env:TEMP "gh_$key.json"
  if ((Test-Path $f) -and ((Get-Date) - (Get-Item $f).LastWriteTime).TotalMinutes -lt 30) {
    Get-Content $f -Raw
  } else {
    $r = gh @args | Out-String; Set-Content -Path $f -Value $r; $r
  }
}

function gh_read { param($or,$path,$ref='main') gh api "repos/$or/contents/$path?ref=$ref" | jq -r '(.content // "") | @base64d' }

function gh_tree {
  param($or,$depth=3)
  gh api "repos/$or/git/trees/main?recursive=1" |
    jq -c ".tree[] | select(.type==\"blob\") | .path | split(\"/\")[0:$depth] | join(\"/\")" |
    Sort-Object -Unique | Select-Object -First 100
}

function truncate_by_quota {
  param($or,$path)
  $quota = if ($env:TOKEN_QUOTA) { [int]$env:TOKEN_QUOTA } else { 3000 }
  $lines = [Math]::Min(500, [Math]::Max(50, [int]($quota / 8)))
  gh api "repos/$or/contents/$path" | jq -r "(.content // \"\") | @base64d | split(\"\n\") | .[0:$lines] | join(\"\n\")"
}

function gh_default_branch { param($or) gh api "repos/$or" | jq -r '.default_branch // "main"' }
```
> Windows 注意：`date` 是 `Get-Date` 别名，取近1年用 `(Get-Date).AddYears(-1).ToString('yyyy-MM-dd')`；临时目录用 `$env:TEMP` 而非 `/tmp`。

### 1.2 Windows CMD 实际示例（jq 双引号 + `^` 转义）
```cmd
:: 读文件并解码（CMD 中 jq 用双引号包裹表达式）
gh api repos/cli/cli/contents/README.md | jq ".content | @base64d"

:: 分页遍历（URL 用双引号，& 等特殊符用 ^ 转义）
gh api "repos/cli/cli/issues?state=open" --paginate | jq ".[].title"
```

## 2. 仓库搜索 (stars>500)
```bash
# 高星Python仓库 (Top 10)
gh search repos --stars:>500 --language=python --sort=stars --order=desc --limit 10 --json fullName,description,stargazersCount | jq -c '.'

# 活跃TypeScript仓库 (近1年有提交)
gh search repos --stars:>500 --language=typescript --pushed:>$(date -v-1y +%Y-%m-%d 2>/dev/null || date -d '-1 year' +%Y-%m-%d) --limit 10 --json fullName,url | jq -c '.'

# 关键词搜索
gh search repos --stars:>500 "fast json parser" --language=rust --limit 5 --json fullName,url | jq -c '.'
```
*限流警告：Search API限流10次/分钟，高频搜索必用 `gh_cached`。*
*限流降级：Search API 触发 403 且缓存未命中时，改用 `gh api repos/O/R` 或 `gh repo view O/R` 直读仓库元数据，避免阻塞等待。*

## 3. 源码读取 (极致省Token)
```bash
# 读文件 (推荐用预置函数)
gh_read O/R src/utils/parser.rs
gh_read O/R config.yaml v2.1.0  # 指定tag/branch

# 读目录树 (直接输出去重path列表，勿再jq二次解析)
gh_tree O/R 3

# 大文件截断 (按行/字符)
gh_read O/R large_file.py | head -200
gh_read O/R large_file.py | sed -n '50,150p'

# 动态截断 (根据剩余配额自动调整)
truncate_by_quota O/R large_file.py

# 敏感信息脱敏 (读取后管道处理)
gh_read O/R config.py | sed -E 's/(api[_-]?key|token|secret|password)\s*[=:]\s*["\x27][^"\x27]+["\x27]/\1="***"/gi'
```
> Note: 读取前先 `gh_default_branch O/R` 获取默认分支（已封装 main→master→API 兜底探测），避免 404；若仍 404 请检查仓库可见性与认证 scope。

## 4. 代码搜索
```bash
# 仓库内搜索
gh search code "def parse_config" --repo O/R --limit 10 --json path,snippet | jq -c '.'

# 跨仓库/限定语言
gh search code "class HttpClient" --language=python --limit 5 --json repository,path | jq -c '.'

# 限定扩展名
gh search code "TODO" --repo O/R --ext=ts --limit 10 --json path,snippet | jq -c '.'
```

## 5. PR / Issue / CI 只读查询
```bash
# PR 列表与详情
gh pr list --repo O/R --limit 10 --json number,title,state | jq -c '.'
gh pr view NUM --repo O/R --json title,body,author,reviewDecision | jq -c '.'
gh pr diff NUM --repo O/R | head -100
gh pr checks NUM --repo O/R

# Issue 列表与详情
gh issue list --repo O/R --state open --limit 10 --json number,title,labels | jq -c '.'
gh issue view NUM --repo O/R --json title,body,state | jq -c '.'

# CI 运行状态与失败日志
gh run list --repo O/R --limit 10 --json databaseId,status,conclusion | jq -c '.'
gh run view RUN_ID --repo O/R --log-failed | head -200
```

## 6. gh api 高频只读模板 (GET only)
```bash
# Repo Meta
gh_timed api repos/O/R | jq -c '{stars:.stargazers_count,forks:.forks_count,default_branch}'

# Commit Detail
gh_timed api repos/O/R/commits/main | jq -c '{sha,message,author:.author.login,stats}'

# Rate Limit 观测
gh_timed api rate_limit | jq -c '.resources | {core,search}'

# 分页遍历 (自动处理Link头)
gh_timed api repos/O/R/issues?state=open --paginate | jq -c '.[].title'
```

## 7. 错误自愈与熔断规则 (Agent自动执行)
| 错误码/条件 | 自动动作 |
|---|---|
| `401` | 触发 `gh auth login` 重新认证 |
| `403` (限流) | `retry` 指数退避，连续3次则暂停5分钟 |
| `404` | 检查仓库名拼写/可见性，及 `gh auth status` 认证与 scope；**勿主动 `gh auth refresh --scopes repo`**（避免授予写权限） |
| `5xx` | `retry` 指数退避，连续5次则暂停10分钟并告警 |
| 返回文本 > 5000字符 | 自动截断并标注 `[已截断]` |
| 单轮工具调用 > 20条 | 暂停30s防Token爆炸 |

## 8. 写入类 API 黑名单 (严禁调用)
**正则拦截**：`gh (pr|issue|repo|release|workflow|gist) (create|merge|comment|edit|close|delete|fork|run|disable|review)`
**API拦截**：`gh api -X (POST|PUT|DELETE|PATCH)`
**文件写入**：`gh api repos/O/R/contents/PATH` (PUT/POST/DELETE 方法)

> 只读白名单澄清：`gh run list` / `gh run view` / `gh pr checks` / `gh pr diff` 属只读，可正常使用（黑名单正则仅拦截第二组动词，不误伤 `gh run list`）。

## 9. 降级方案 (gh不可用时)
```bash
curl -s --max-time 30 -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/O/R/contents/README.md" \
  | jq -c '.content | @base64d'
```

## 10. 验证与测试 (Validation & Testing)
> 纯静态断言 + 单行命令 + 预期锚点；Agent 自检 / CI 集成两用，零额外运行时 Token。exit 0 = 通过。

| ID | 测试项 | 命令 | 通过锚点 |
| :--- | :--- | :--- | :--- |
| T1 | 写操作拦截 | `echo "gh pr create" \| grep -Eq 'gh (pr\|issue\|repo\|release\|workflow\|gist) (create\|merge\|comment\|edit\|close\|delete\|fork\|run\|disable\|review)'` | exit 0 |
| T2 | 认证状态 | `gh auth status` | 含 `Logged in to github.com` |
| T3 | 超时机制(本地模拟, Bash侧) | `timeout 1 sleep 2; test $? -eq 124` | exit 0 |
| T4 | 读文件解码 | `gh_read cli/cli README.md \| grep -q 'GitHub CLI'` | exit 0 |
| T5 | 目录树限深 | `gh_tree cli/cli 2 \| head -1 \| awk -F/ '{exit !(NF<=2)}'` | exit 0 |
| T6 | 动态截断 | `TOKEN_QUOTA=400 truncate_by_quota cli/cli README.md \| wc -l` | `49` 或 `50` |
| T7 | 降级 curl | `curl -s --max-time 5 https://api.github.com/rate_limit \| jq -e '.resources.core'` | exit 0 |
| T8 | PowerShell | `pwsh -NoProfile -Command "gh --version"` | 含 `gh version` |
| T9 | 函数加载 | `type gh_timed gh_cached retry gh_read gh_tree truncate_by_quota gh_default_branch >/dev/null 2>&1` | exit 0 |

### 一键自检（Bash，全只读）
```bash
t() { eval "$1" >/dev/null 2>&1 && echo "PASS $2" || echo "FAIL $2"; }
t 'echo "gh pr create" | grep -Eq "gh (pr|issue|repo|release|workflow|gist) (create|merge|comment|edit|close|delete|fork|run|disable|review)"' T1_blacklist
t 'gh auth status' T2_auth
t 'timeout 1 sleep 2; test $? -eq 124' T3_timeout
t 'gh_read cli/cli README.md | grep -q "GitHub CLI"' T4_read
t 'gh_tree cli/cli 2 | head -1 | awk -F/ "{exit !(NF<=2)}"' T5_tree
t 'TOKEN_QUOTA=400 truncate_by_quota cli/cli README.md | wc -l | grep -Eq "^(49|50)$"' T6_truncate
t 'curl -s --max-time 5 https://api.github.com/rate_limit | jq -e ".resources.core"' T7_fallback
t 'pwsh -NoProfile -Command "gh --version"' T8_pwsh
t 'type gh_timed gh_cached retry gh_read gh_tree truncate_by_quota gh_default_branch >/dev/null 2>&1' T9_functions
```

> T1/T9 纯静态（无网络）；T2–T6 需 `gh` 认证；T7 仅验证降级通路。全为只读断言，零写风险。脚本中 `$1`/`$2` 为 `t()` 函数参数，非技能变量。

## 11. 实际使用场景 (Agent 对话示例)
> 展示 Agent 收到任务时如何组合工具，均只读、省 Token。`O/R` 以下以 `cli/cli` 为例。

### 场景A："看看 cli/cli 最近3天的 PR 情况"
```bash
gh pr list --repo cli/cli --limit 10 --json number,title,author,updatedAt,state \
  | jq -c '.[] | select(.updatedAt >= "'"$(date -u -d '-3 days' +%Y-%m-%dT%H:%M:%SZ)"'") | {n:.number,t:.title,a:.author.login,s:.state}'
```

### 场景B："这个仓库用了什么构建工具？找找配置文件"
```bash
# 先取目录树前2层，再定位构建文件
gh_tree cli/cli 2
gh_search() { gh search code "filename:go.mod OR filename:package.json OR filename:Makefile" --repo cli/cli --limit 5 --json path | jq -c '.[].path'; }
```

### 场景C："某次 CI 失败原因"
```bash
gh run list --repo cli/cli --limit 5 --json databaseId,status,conclusion \
  | jq -c '.[] | select(.conclusion=="failure") | .databaseId' \
  | head -1 | xargs -I{} gh run view {} --repo cli/cli --log-failed | head -50
```

> 组合原则：先 `gh_default_branch` 定分支 → `gh_tree` 定文件 → `gh_read` 读内容 → 全程 `--json` + `jq -c` 裁剪，单轮工具调用 ≤20 条。
