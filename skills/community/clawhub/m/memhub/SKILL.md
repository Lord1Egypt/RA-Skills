---
name: memhub
version: 0.4.4
description: 使用 MemHub Protocol v0.1 读写用户的跨 Agent 统一记忆仓库。当用户要求记住信息、检索/遗忘记忆、读取个人/项目上下文、生成 chatbot 注入文本、同步 Git 记忆仓库时使用。
tags:
  - memory
  - memhub
  - github
  - gitee
  - sync
  - agent-memory
license: MIT-0
---

# MemHub Skill

MemHub 是一个无服务端、Git-first 的个人 AI 记忆协议。本 Skill 让 Agent 能够读取、写入和同步符合 MemHub Protocol v0.1 的记忆仓库。

## 触发场景

使用本 Skill 当：

- 用户说“记住这个”、“帮我记一下”、“以后记得”。
- 用户问“我的偏好是什么”、“当前项目上下文是什么”。
- 用户需要把记忆注入到 Gemini/元宝/豆包/Cursor/Claude Code。
- 会话开始时需要读取用户长期记忆。
- 会话结束时需要把关键决策/偏好/事实写入记忆并同步。

## 环境变量

推荐设置（唯一需要的一项）：

```bash
export MEMHUB_REPO=/path/to/memhub-data
```

OAuth 同步**开箱即用**：GitHub 和 Gitee 都默认走内置的 MemHub Auth Broker，
普通用户无需设置任何 OAuth 相关环境变量。以下全部为可选的高级覆盖：

```bash
# 覆盖内置 broker（自建 broker 时）
export MEMHUB_OAUTH_BROKER_URL=https://<your-broker-host>
export MEMHUB_GITEE_OAUTH_BROKER_URL=https://<your-broker-host>   # 仅覆盖 Gitee

# 开发者直连模式（不经 broker，自己保管 Gitee secret）
export MEMHUB_GITEE_CLIENT_SECRET=...

# 覆盖内置 OAuth App client id
export MEMHUB_GITHUB_CLIENT_ID=...
export MEMHUB_GITEE_CLIENT_ID=...

# Token fallback
export MEMHUB_GITHUB_TOKEN=...
export MEMHUB_GITEE_TOKEN=...
```

如果未设置 `MEMHUB_REPO`，脚本默认使用当前工作目录下的 `./memhub-data`。

CLI 会自动读取当前目录 `.env` 和用户 home 目录 `.env`，且不会覆盖已经存在的进程环境变量。不要把 `.env` 提交到 Git。

## 命令

本 Skill 提供一个 Python CLI：`scripts/memhub.py`。

```bash
# 初始化仓库
python scripts/memhub.py --repo ~/memhub-data init --name dateng --role "Product Manager"

# 读取上下文
python scripts/memhub.py --repo ~/memhub-data context
python scripts/memhub.py --repo ~/memhub-data context --pack brief
# 记忆：默认直写 canonical 并本地提交（不自动推送）
python scripts/memhub.py --repo ~/memhub-data remember "用户偏好结构化直接的回答" --type preference --source agent
python scripts/memhub.py --repo ~/memhub-data remember "MemHub 采用 Git-first 架构" --type decision --project memhub --source agent
# 低置信/待人工复核的内容才进 inbox 审计缓冲
python scripts/memhub.py --repo ~/memhub-data remember "也许该支持 Notion 导出" --type fact --inbox --source agent

# 检索与遗忘
python scripts/memhub.py --repo ~/memhub-data search "Git-first"
python scripts/memhub.py --repo ~/memhub-data search "决策" --type decision --project memhub
python scripts/memhub.py --repo ~/memhub-data search "旧偏好" --include-archived   # 含已归档
python scripts/memhub.py --repo ~/memhub-data forget "过时的偏好"            # 预览
python scripts/memhub.py --repo ~/memhub-data forget "过时的偏好" --apply     # 软归档（status=archived）

# 将 inbox 缓冲项归档到 canonical（仅 --inbox 写入的内容才需要）
python scripts/memhub.py --repo ~/memhub-data promote --dry-run
python scripts/memhub.py --repo ~/memhub-data promote --apply
python scripts/memhub.py --repo ~/memhub-data promote --status all --apply   # 扫全部 inbox 项

# 检查 inbox
python scripts/memhub.py --repo ~/memhub-data inbox list
python scripts/memhub.py --repo ~/memhub-data inbox list --status all
python scripts/memhub.py --repo ~/memhub-data inbox show <filename-or-id-fragment>

# 将 inbox 半自动归档到 canonical memory
python scripts/memhub.py --repo ~/memhub-data promote --dry-run
python scripts/memhub.py --repo ~/memhub-data promote --apply
python scripts/memhub.py --repo ~/memhub-data promote <filename-or-id-fragment> --apply

# 导出给 chatbot 的上下文
python scripts/memhub.py --repo ~/memhub-data export chatbot

# 首次接入（推荐）：授权 + 自动判断拉取已有记忆 / 初始化新仓库
python scripts/memhub.py --repo ~/memhub-data onboard github --repo-name mymemhub
python scripts/memhub.py --repo ~/memhub-data onboard gitee  --repo-name mymemhub

# 同步 GitHub/Gitee（手动分步；默认 OAuth 走内置 broker）
python scripts/memhub.py --repo ~/memhub-data sync setup github --repo-name mymemhub
python scripts/memhub.py --repo ~/memhub-data sync setup gitee --repo-name mymemhub
python scripts/memhub.py --repo ~/memhub-data sync setup github --auth token --repo-name mymemhub
python scripts/memhub.py --repo ~/memhub-data sync setup github --auth ssh --remote-method ssh --owner <login> --repo-name mymemhub --no-create
python scripts/memhub.py --repo ~/memhub-data sync status
python scripts/memhub.py --repo ~/memhub-data sync

# 自检：确认本机/本仓库的自动同步是否就绪（remote/token/merge driver/MEMHUB_REPO 等）
python scripts/memhub.py --repo ~/memhub-data doctor
```

## Agent 行为协议

### 上下文 pack 分级

`context --pack` 有四档,逐档累加内容:

- `brief`:用户画像、最重要的偏好、当前项目及最近决策(用于注入 chatbot)。
- `standard`(默认):brief + 约束、惯例、未完成任务。
- `project`:聚焦默认/指定项目,决策与任务更全。
- `full`:standard + knowledge、relations、最近 timeline。

`export chatbot` 默认用 brief;若存在 `.memhub/templates/context-pack.md.j2`,则用该模板渲染(支持 `{{ name }}` 等占位符)。

### 总原则

- `MEMHUB_REPO` 是用户记忆仓库；不要把用户记忆写入代码仓库。
- GitHub/Gitee remote 只是同步后端；YAML/Markdown 文件仍是可信源数据。
- 自动写入默认进入 canonical 记忆（本地提交，不自动推送）；低置信或需人工复核的才用 `--inbox`。
- `sync setup` 会触发授权、创建仓库、修改 remote；**只有用户明确要求配置/切换同步时才执行**。
- OAuth/token/SSH 凭据、authorization code、client secret、access token 都属于敏感信息；不要在回答中复述。

### 对话开始：读取上下文

**本会话首次涉及记忆时**，先跑一次自检确认自动同步就绪（每个会话只需一次，不要每轮都跑）：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" doctor
```

- 若 doctor 报 `NOT ready`（有 ✗），说明自动同步未生效。按提示补齐：缺 remote → 提示用户
  `sync setup`；缺 token（常见于新机器）→ 引导用户重新授权；其余 ✗ 同理。**不要静默忽略**，
  否则用户会误以为在自动同步，实际没有。
- 若全绿或只有 `!` 提示，继续正常流程。
- doctor 是只读的、不联网，开销很小；但仍只需每会话首次跑一次即可。

确认就绪后，直接读取 context——`context` 会按节流阈值**自动从远端拉取**最新记忆，通常无需先手动 `sync`：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" context --pack brief
```

- 若距上次拉取超过 `pull_throttle_seconds`，`context` 会自动 `pull --rebase` 再输出。
- 自动拉取失败时，CLI 会用本地记忆并在 stderr 提示“远端同步失败，当前上下文可能不是最新”，
  无需中断；如需强制最新，可显式 `sync` 后再读。
- 将 context 作为可审计上下文，不要当成绝对事实；遇到冲突时优先询问用户。

### 对话中：写入记忆

当用户明确要求记忆，或对话中形成稳定偏好/决策/事实时，默认**直写 canonical**：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" remember "内容" --type fact --source agent
```

- 直写会按 type 路由到对应 canonical 文件、去重后追加，并**本地提交但不自动推送**。
- 重复内容会被自动跳过。
- 只有低置信、需人工复核或批量待整理的内容，才加 `--inbox` 进审计缓冲，之后再 `promote`。

类型建议：

- `decision`：明确决策
- `preference`：稳定偏好
- `fact`：事实
- `knowledge`：可复用知识/结论
- `event`：重要事件
- `relation`：人物/组织/工具关系
- `constraint`：约束
- `convention`：惯例

### 同步：自动节流，无需每次手动 sync

配置了 remote 后，同步是**自动**的，Agent 通常无需显式调用 `sync`：

- **写入即同步（节流）**：每次 `remember` / `forget --apply` / `promote --apply` 后，CLI 会
  自动尝试推送。距上次推送不足 `sync.push_throttle_seconds`（默认 3600 秒）时只在本地提交，
  超过阈值才真正 pull+push。**记忆始终立即落本地，绝不丢失。**
- **读取即拉取（节流）**：`context` 命令会在 `sync.pull_throttle_seconds`（默认 3600 秒）阈值外
  自动 `pull --rebase` 拉取其它设备的最新记忆；拉取失败则用本地并在 stderr 提示可能不是最新。

显式 `sync` 命令**忽略节流，立即** pull+push，适合在对话收尾兜底，确保本次所有记忆都已上远端：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" sync
```

节流阈值与开关都在 `.memhub/config.yaml` 的 `sync` 段（`auto_push`/`auto_pull` /
`push_throttle_seconds` / `pull_throttle_seconds`）；节流时间戳记在本机 `.memhub/cache/sync.yaml`
（git 忽略，每台设备独立）。单次写入若想跳过自动推送，加 `--no-sync`。

`init`/`sync` 会自动注册结构化 merge 驱动（local git config 不随 clone 走，故每台设备首次
`sync` 会自愈补注册），多设备对同一记忆文件的并发追加可自动合并，不会冲突。

> **换新机器/新 Agent 时**：凭据（token）存在本机 `.memhub/secrets.yaml` 且不随 git 同步，
> 所以新机器即使 clone 了记忆仓库也需要**重新授权一次**。先跑 `doctor` 自检，按提示补齐
> remote/token 即可——全绿后自动同步即就绪。

### 检索与遗忘

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" search "关键词" --type decision --project memhub
python scripts/memhub.py --repo "$MEMHUB_REPO" forget "过时内容"          # 预览
python scripts/memhub.py --repo "$MEMHUB_REPO" forget "过时内容" --apply   # 软归档
```

- `forget` 默认 dry-run；`--apply` 把命中条目 `status` 置为 `archived`，使其从 context pack
  消失但保留在 Git 历史中，可审计、可回滚。
- 纠正一条记忆 = `forget` 旧条目 + `remember` 新条目。

### 首次接入：用 onboard（推荐）

新 agent / 新机器第一次接入时，**用 `onboard` 一条命令完成全流程**，它会自动判断该
"拉取已有记忆"还是"初始化新仓库"，避免用默认数据污染你已有的真实记忆：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" onboard gitee --repo-name mymemhub
python scripts/memhub.py --repo "$MEMHUB_REPO" onboard github --repo-name mymemhub
```

onboard 的流程：

1. 授权（默认走内置 broker，见下）。
2. **探测远端**是否已有 MemHub 记忆仓库（含 `.memhub/config.yaml`）：
   - **已有** → 以远端为准拉取到本地，**不写入任何默认数据**（你的真实记忆直接到位）；
   - **为空** → 初始化默认记忆并推送，建立远端仓库。
3. 注册 merge 驱动、确保 auto-sync 就绪。
4. 打印 `doctor` 自检结果。

之后写入即自动推送、读取即自动拉取，无需再手动 sync。新机器换设备时**总是优先用
onboard**，不要先 `init` 再 `sync setup`（那会先播种默认数据，可能污染远端真实记忆）。

### 同步 setup：手动分步配置（高级）

`onboard` 内部会调用 setup。只有当你想单独配置/切换 remote、且明确知道本地数据状态时，
才直接用 `sync setup`。当用户说“配置同步”、“连接 GitHub/Gitee”、“换成 Gitee/GitHub 同步”时，
优先用 `onboard`。

**开箱即用**：GitHub 和 Gitee 都默认走内置的 MemHub Auth Broker（`https://oauth.1024hub.cn`），
client_secret 保管在 broker 服务端，**用户无需设置任何环境变量或自建 OAuth 应用**。

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --repo-name mymemhub
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup gitee  --repo-name mymemhub
```

授权流程（两者一致）：

1. CLI 调用 broker 创建授权 session，得到一个 `auth_url`。
2. CLI 打开（或打印）该 URL；Agent 应把 URL 展示给用户，请用户在浏览器完成授权。
3. CLI 轮询 broker 直到拿到 access token，自动存入本机 `.memhub/secrets.yaml`（git 忽略）。
4. 不要要求用户把 access token 发到聊天里。

无浏览器环境：加 `--no-browser`，CLI 会打印 URL 由用户手动打开。

#### 高级 / fallback（仅当用户明确选择时）

- 自建 broker：`--broker-url https://your-broker` 或设 `MEMHUB_OAUTH_BROKER_URL` /
  `MEMHUB_GITEE_OAUTH_BROKER_URL`。
- 开发者直连（不经 broker）：Gitee 用 `--client-secret`（或 `MEMHUB_GITEE_CLIENT_SECRET`）；
  GitHub 会回退到 Device Flow。
- Token / SSH：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --auth token --repo-name mymemhub
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --auth ssh --remote-method ssh --owner <login> --repo-name mymemhub --no-create
```

### 同步失败与冲突处理

- 不要删除本地 `inbox`、canonical 文件或 `.git` 历史。
- 将错误摘要告诉用户，避免泄露 token/header。
- 如果 `git pull --rebase` 冲突，停止自动处理，报告冲突文件，让用户/Agent 单独修复。
- 如果 provider 授权失败，建议用户重新授权或切换 token/SSH fallback。
- 如果远端仓库创建失败但已存在，可以继续配置 remote 并尝试 sync。

### Inbox 归档（promote）

`remember` 默认直写 canonical，无需 promote。只有用 `--inbox` 缓冲过的低置信/待复核内容
才需要 promote。整理 inbox 时先预览：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" inbox list
python scripts/memhub.py --repo "$MEMHUB_REPO" promote --dry-run
```

确认归档目标合理后再执行（默认 dry-run，须显式 `--apply`；`--apply` 后按节流自动推送）：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" promote --apply
```

`promote` 默认只扫 pending 的 inbox 项，可用 `--status all` 扫全部。归档路由规则：

- `decision` → `projects/<project>/decisions.yaml`
- `preference` → `identity/preferences.yaml`
- `constraint` → `identity/constraints.yaml`
- `convention` → `identity/conventions.yaml`
- `knowledge` → `knowledge/product.yaml`
- `relation` → `relations/people.yaml`
- `fact` / `event` → `timeline/YYYY-MM.yaml`

不要写入：

- 临时闲聊
- 未确认猜测
- 敏感信息，除非用户明确授权
- 无新增信息的重复内容

### 对话结束

如果对话中产生重要决策、偏好或事实：

1. `remember` 直写记忆（低置信内容用 `--inbox`，必要时 `promote`）。写入时已按节流自动推送。
2. 收尾执行一次显式 `sync`：它忽略节流、立即推送，确保本次会话即使在节流窗口内产生的
   记忆也全部上远端（兜底，防止刚写完就关闭 Agent 导致最后几条只在本地）。

## 发布与安全约束

- 不要把真实 token、client secret、OAuth code 写进 `SKILL.md`、README、示例或提交历史。
- `.memhub/secrets.yaml` 必须保持本地忽略。
- 发布到 SkillHub/ClawHub 的包应包含：`SKILL.md`、`README.md`、`scripts/memhub.py`、`templates/context-pack.md.j2`。
- 发布包不应包含 `__pycache__`、`.pyc`、`.git` 或用户个人记忆数据。

## 重要原则

- MemHub 只负责存取和同步，智能判断由 Agent 完成。
- 写入必须带 source，便于追溯。
- 默认直写 canonical 记忆；低置信或需人工复核的内容才进 inbox 审计缓冲。
- Git 仓库中的 YAML/Markdown 是唯一可信源数据。
