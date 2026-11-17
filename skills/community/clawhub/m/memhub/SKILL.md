---
name: memhub
version: 0.4.8
description: 使用 MemHub Protocol v0.1 管理用户明确指定的跨 Agent 记忆仓库。用于用户明确要求记住、检索、遗忘、导出上下文或配置 Git 同步时；读取可直接执行，持久写入、自动同步、OAuth、remote 修改和仓库创建必须来自当前用户的明确请求。
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
- 用户明确要求在会话结束前保存关键决策、偏好或事实，或已经明确启用了对应自动记忆策略。

## 环境变量

推荐设置（唯一需要的一项）：

```bash
export MEMHUB_REPO=/path/to/memhub-data
```

GitHub 默认使用官方 Device Flow。Gitee OAuth 可使用内置 Broker，但 CLI 会先展示固定
Broker 域名并要求用户确认；非交互环境必须显式传入可信 Broker 或自己的 OAuth 配置。

可选配置项只写在进程环境或显式 `--env-file` 中，不要写进 Skill、仓库或聊天：

- `MEMHUB_OAUTH_BROKER_URL`：明确选择的通用 Broker；
- `MEMHUB_GITEE_OAUTH_BROKER_URL`：仅用于 Gitee 的可信 Broker；
- `MEMHUB_GITHUB_CLIENT_ID`、`MEMHUB_GITEE_CLIENT_ID`：自有 OAuth App client id；
- `MEMHUB_GITEE_CLIENT_SECRET`：Gitee 直连模式的 client secret；
- `MEMHUB_GITHUB_TOKEN`、`MEMHUB_GITEE_TOKEN`：token fallback。

必须通过 `--repo` 或 `MEMHUB_REPO` 明确指定专用记忆仓库；CLI 不会把当前目录隐式当作记忆仓库。

CLI 不会自动读取当前目录或 home 目录的通用 `.env`。如确需文件配置，显式传入
`--env-file /path/to/memhub.env`；只会加载受支持的 `MEMHUB_*` 键。

## 权限与确认边界

机器可读版本见同目录 `permissions.json`；下面的散文说明与它一致。

- `context`、`search`、`inbox list/show`、`doctor` 是只读操作；`doctor` 默认完全离线，只有显式加 `--network` 才会探测已配置的 broker。
- `remember`、`forget --apply`、`promote --apply`、`init` 会修改记忆仓库；只有用户当前请求明确要求对应写入时才执行。
- `sync`、`sync setup`、`onboard` 会访问网络或修改 Git 状态；只有用户当前请求明确要求同步或配置时才执行。
- `sync setup`/`onboard` 是用户明确发起的同步授权，完成后保留原有节流自动同步；用户可传 `--manual-sync` 关闭。
- 所有 inbox 引用和 canonical target 都限制在指定 MemHub 仓库内；拒绝绝对路径和 `..` 越界。
- HTTPS token 只会发送到所选 Provider 的固定官方 Git/API 主机；目标主机不匹配时拒绝执行。
- 只有 `git` 一个外部命令会被调用，且不经过 shell；凭据只经子进程环境传递，不出现在 argv。
- 远程写入（创建仓库、push）只在 `sync setup` / `onboard` / `sync` 被用户显式调用时发生。
- 没有破坏性操作：`forget` 是软归档，不删文件、不改写 Git 历史。

## 命令

本 Skill 提供一个 Python CLI：`scripts/memhub.py`。

```bash
# 初始化仓库
python scripts/memhub.py --repo ~/memhub-data init --name dateng --role "Product Manager"

# 读取上下文
python scripts/memhub.py --repo ~/memhub-data context
python scripts/memhub.py --repo ~/memhub-data context --pack brief
# 记忆：默认直写 canonical 并本地提交；是否自动推送取决于同步配置
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
python scripts/memhub.py --repo ~/memhub-data onboard gitee --repo-name mymemhub --broker-url https://<trusted-broker>

# 同步 GitHub/Gitee（手动分步）
python scripts/memhub.py --repo ~/memhub-data sync setup github --repo-name mymemhub
python scripts/memhub.py --repo ~/memhub-data sync setup gitee --repo-name mymemhub --broker-url https://<trusted-broker>
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
- doctor 是只读的、默认不联网（只有显式 `--network` 才探测 broker），开销很小；但仍只需每会话首次跑一次即可。
- doctor 会打印凭据存放位置；若仓库里还有旧版 `.memhub/secrets.yaml`，会提示可以删除。

确认就绪后，直接读取 context。仅当用户已通过 setup/onboard 授权自动同步时，
`context` 才会按节流阈值从远端拉取最新记忆：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" context --pack brief
```

- 若距上次拉取超过 `pull_throttle_seconds`，`context` 会自动 `pull --rebase` 再输出。
- 自动拉取失败时，CLI 会用本地记忆并在 stderr 提示“远端同步失败，当前上下文可能不是最新”，
  无需中断；如需强制最新，可显式 `sync` 后再读。
- 将 context 作为可审计上下文，不要当成绝对事实；遇到冲突时优先询问用户。

### 对话中：写入记忆

当用户明确要求记忆，或已经明确启用了对应自动记忆策略时，默认**直写 canonical**：

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" remember "内容" --type fact --source agent
```

- 直写会按 type 路由到对应 canonical 文件、去重后追加并本地提交；是否自动推送取决于用户在 setup/onboard 时选择的同步模式。
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

### 同步：显式配置后自动节流，可选择手动模式

只有用户明确执行 setup/onboard 后才会配置 remote；此后保留原有的节流自动同步。
若用户传入 `--manual-sync`，则关闭自动 pull/push，只保留显式 `sync`：

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

> **换新机器/新 Agent 时**：凭据存在记忆仓库**之外**的机器本地目录（macOS 默认
> `~/Library/Application Support/memhub/secrets/`，Linux 默认 `~/.local/state/memhub/secrets/`，
> 可用 `MEMHUB_SECRETS_DIR` 覆盖），因此不随 clone 或同步走，新机器需要**重新授权一次**。
> 先跑 `doctor` 自检，按提示补齐
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
python scripts/memhub.py --repo "$MEMHUB_REPO" onboard gitee --repo-name mymemhub --broker-url https://<trusted-broker>
python scripts/memhub.py --repo "$MEMHUB_REPO" onboard github --repo-name mymemhub
```

onboard 的流程：

1. 授权（GitHub 默认走官方 Device Flow；Gitee Broker 必须显式指定）。
2. **探测远端**是否已有 MemHub 记忆仓库（含 `.memhub/config.yaml`）：
   - **已有** → 以远端为准拉取到本地，**不写入任何默认数据**（你的真实记忆直接到位）；
   - **为空** → 初始化默认记忆并推送，建立远端仓库。
3. 注册 merge 驱动，并按用户选择启用节流 auto-sync 或 `--manual-sync`。
4. 打印 `doctor` 自检结果。

完成 setup/onboard 后，默认维持原有节流自动同步；如果用户选择 `--manual-sync`，则只在
显式执行 `sync` 时联网。新机器换设备时优先用 `onboard`，不要先 `init` 再 `sync setup`
（那会先播种默认数据，可能污染远端真实记忆）。

### 同步 setup：手动分步配置（高级）

`onboard` 内部会调用 setup。只有当你想单独配置/切换 remote、且明确知道本地数据状态时，
才直接用 `sync setup`。当用户说“配置同步”、“连接 GitHub/Gitee”、“换成 Gitee/GitHub 同步”时，
优先用 `onboard`。

GitHub 默认走官方 Device Flow。Gitee 交互式配置会先展示内置 Broker 域名并请求确认；
非交互环境必须通过 `--broker-url` 或 `MEMHUB_GITEE_OAUTH_BROKER_URL` 明确指定，
也可以使用自己的 client secret 直连。

```bash
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup github --repo-name mymemhub
python scripts/memhub.py --repo "$MEMHUB_REPO" sync setup gitee --repo-name mymemhub --broker-url https://<trusted-broker>
```

显式选择 Broker 时的授权流程：

1. CLI 调用 broker 创建授权 session，得到一个 `auth_url`。
2. CLI 打开（或打印）该 URL；Agent 应把 URL 展示给用户，请用户在浏览器完成授权。
3. CLI 轮询 broker 直到拿到 access token，自动存入记忆仓库之外的本机凭据目录（0600，可用 `MEMHUB_SECRETS_DIR` 覆盖）。
4. 不要要求用户把 access token 发到聊天里。

无浏览器环境：加 `--no-browser`，CLI 会打印 URL 由用户手动打开。

#### 高级 / fallback（仅当用户明确选择时）

- 自建 broker：`--broker-url https://your-broker` 或设 `MEMHUB_OAUTH_BROKER_URL` /
  `MEMHUB_GITEE_OAUTH_BROKER_URL`。
- 开发者直连（不经 broker）：Gitee 使用 `MEMHUB_GITEE_CLIENT_SECRET`；
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

确认归档目标合理后再执行（默认 dry-run，须显式 `--apply`；已启用 auto-sync 时才按节流自动推送）：

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

如果用户明确要求保存重要决策、偏好或事实，或已经明确启用了对应自动记忆策略：

1. `remember` 直写记忆（低置信内容用 `--inbox`，必要时 `promote`）。
2. 如果用户已明确启用 auto-sync，按节流策略同步；否则只有用户明确要求时才执行 `sync`。

## 安全模型与机器可读边界

`permissions.json` 是本 Skill 的权限边界声明（文件/网络/凭据/变更），供扫描器与人工复核直接读取：

- 文件写入只落在 `MEMHUB_REPO` 内；绝对路径与 `..` 越界一律拒绝。
- 凭据只写入 `MEMHUB_REPO` 之外的本机目录，文件 0600、目录 0700。
- 默认无自动出网；`sync setup` / `onboard` / `sync` 被显式调用后才访问 github.com / gitee.com。
- GitHub 走官方 Device Flow（scope `repo`）；Gitee 直连 OAuth 每次生成并校验 `state`，防止把别人的账号绑定到本仓库。
- 第三方 broker 不会被隐式使用：必须由用户通过 `--broker-url` 或 `MEMHUB_*_OAUTH_BROKER_URL` 明确指定主机。
- `doctor` 默认离线；需要探测 broker 时显式加 `--network`。

## 发布与安全约束

- 不要把真实 token、client secret、OAuth code 写进 `SKILL.md`、README、示例或提交历史。
- 凭据文件必须留在记忆仓库之外；仓库内的旧 `.memhub/secrets.yaml` 只作为一次性读取的迁移来源。
- 发布到 SkillHub/ClawHub 的包应包含：`SKILL.md`、`README.md`、`permissions.json`、`scripts/memhub.py`、`templates/context-pack.md.j2`。
- 发布包不应包含 `__pycache__`、`.pyc`、`.git` 或用户个人记忆数据。

## 重要原则

- MemHub 只负责存取和同步，智能判断由 Agent 完成。
- 写入必须带 source，便于追溯。
- 默认直写 canonical 记忆；低置信或需人工复核的内容才进 inbox 审计缓冲。
- Git 仓库中的 YAML/Markdown 是唯一可信源数据。
