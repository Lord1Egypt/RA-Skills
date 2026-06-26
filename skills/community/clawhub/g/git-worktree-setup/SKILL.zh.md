---
name: git-worktree-setup
description: 用户主动要求「为这个仓库生成 / 更新 git worktree 自动初始化脚本」时调用。这个 skill 本身不在新建 worktree 时被自动触发——它产出的脚本和 hook 才是。流程：先自己 audit 仓库结构推断初步方案，再拿方案找用户确认（只问推不出的关键题），最后生成针对该仓库定制的 setup-worktree 脚本 + 对应 agent 工具（Claude Code / Codex / Gemini CLI 等）的 hook 配置。也用于更新已有脚本。
license: MIT
compatibility: 适配任何支持 Agent Skills 格式的 agent（Claude Code / Codex / Cursor / OpenCode / Gemini CLI 等）。生成的 setup 脚本依赖 bash + git + 标准 POSIX 工具（grep、awk、ln、cp、shasum）。
---

# Git Worktree Setup

> 这是 SKILL.md 的中文审核版。最终发布时 `SKILL.md` 是英文，两份内容等价。

## 这个 skill 是什么 / 不是什么

**产出**：一份针对当前仓库定制的 `scripts/setup-worktree.sh`（或类似名）+ 对应 agent 工具的 hook 配置 + 一个手动入口。

**不是**：每次新建 worktree 时被自动触发的东西。**那是 hook**。这个 skill 只在用户**主动召唤**时跑：
- 「帮我搞一下 worktree 自动 setup」
- 「我这项目每次 `git worktree add` 完都要手动 install / 拷 .env，能不能自动化」
- 「项目结构改了，更新一下 worktree 初始化脚本」

**核心工作方式：先自己 audit 仓库 → 给出初步方案 → 只对推不出的关键问题问用户 → 落盘。**

不要一上来就给用户列 7 个问题让他答，那很烦。先看代码、看配置，能推断的全推断出来，**带方案上桌**，让用户调整即可。

## 4 步工作流

### Step 1：自己 audit 仓库（不问用户）

**这一步是动态推断，不是按死清单打勾。** 下面的表只是**常见信号举例**——你必须根据实际看到的东西展开调研，可能涉及任何工具、任何栈、任何项目特殊约定。看到陌生的配置文件就 Read 它；看到不认识的 CLI 名就 grep 它；看到 README / CONTRIBUTING / Makefile / justfile / Taskfile 提到 "setup" / "bootstrap" / "install" 步骤就读，那里通常藏着仓库自己定义的"新机器要装啥"清单。

**起点信号（举例，远不止这些）**：

| 看什么 | 推断什么 |
|---|---|
| `package.json`（root + workspaces 字段） | npm/pnpm/yarn？是不是 monorepo？workspace glob 是哪些？ |
| `pnpm-workspace.yaml` / `lerna.json` / `nx.json` / `turbo.json` | 进一步确认 monorepo 工具 |
| `pyproject.toml` / `Pipfile` / `uv.lock` / `requirements.txt` | Python 栈？poetry / uv / pip？要 share `.venv`？ |
| `Cargo.toml`（含 workspace 段） | Rust？`target/` 要不要共享？ |
| `go.mod` | Go？基本没东西要 share |
| `Gemfile` / `mix.exs` / `composer.json` / `pubspec.yaml` 等 | 其它语言生态——同理推断各自的 deps 目录 |
| `.gitignore` | 找被忽略的：`node_modules` / `.venv` / `.env` / `dist` / `*.state` 等——这些往往就是要 share/copy 的候选；陌生的忽略项也别跳过，多半是项目特定 cache |
| `.env.example` / `.dev.vars.example` / `apps/*/.dev.vars.example` / `config/*.example` | 提示哪些 secret / config 文件需要 Copy |
| `docker-compose*.yml` / `compose.yml` / `Dockerfile.dev` | stateful 服务清单（pg/redis/mysql）+ volume 路径 + host port 绑定 |
| `wrangler.toml` / `fly.toml` / `serverless.yml` / `terraform/*` 等 | 各 IaC / 平台配置往往关联本地 state 目录 |
| `.claude/` / `.cursor/` / `.codex/` / `.aider*` / `.opencode/` 等存在与否 | 推断用户当前用的 agent 工具 |
| `Makefile` / `justfile` / `Taskfile.yml` / `bin/setup` / `script/bootstrap` | 项目自定义 setup 入口——里面的 install / link / copy 步骤是 worktree setup 的金矿 |
| `README.md` / `CONTRIBUTING.md` / `docs/setup*.md` 中 "Getting started" / "Local dev" 段落 | 人话版的"新机器要装啥"清单 |
| `.github/workflows/*.yml` / `.gitlab-ci.yml` 等 CI 配置 | CI 怎么 setup 环境 = 本地大概也要那些 |
| `scripts/setup-worktree.sh` / `scripts/setup-worktree.sh` / `bin/worktree-*` 等 | 是否已有 → 决定全新 vs 更新模式 |
| 主仓库 `node_modules/`、`apps/*/node_modules/`、`.venv/` 等是否实际存在 | 验证推断 + 知道哪些目前真能 link |
| **任何陌生顶层目录** | 比如 `references/`、`vendor/`、`third_party/`、`fixtures/`——可能是项目刻意维护的共享资源，问之前先 ls 看里面是啥（symlink？大文件？测试数据？） |

**主动展开**：以上每一项都可能引出新的调研。比如读 `package.json` 发现用了 `husky` → 看 `.husky/` 是否要共享；发现用了 `playwright` → 看是否要共享 browser cache（`~/.cache/ms-playwright`）；读 `pyproject.toml` 发现 `[tool.uv]` → uv 的本地 cache 在哪。**别因为表里没列就跳过**。

audit 结束你应该手里已经有：
- 一份**资源候选清单**（按 Share / Copy / Generate 三档预分），含每项的来源依据
- **推断的 agent 工具**（基于配置目录存在性）
- **是否已有脚本**（决定下一步是建新 vs 改）
- **该问的开放性问题**（audit 推不出但对决策必要的项）

### Step 2：拿初步方案找用户确认（带方案上桌）

把 audit 结果归并成一份**资源清单提案**，三档分类摆出来。**对推得出的项直接给方案**，**对推不出的项标明"待确认"**。例：

> 我审了一遍仓库，看起来是 npm workspaces monorepo（apps/api、apps/web、packages/*），用 Cloudflare Workers + Vite。`.claude/settings.json` 已存在，看来用 Claude Code。
>
> 我准备这样配 worktree 自动初始化：
> - **Share（symlink）**：`node_modules`、`apps/*/node_modules`、`packages/*/node_modules`
> - **Copy**：`apps/api/.dev.vars`（看到 `.dev.vars.example`）
> - **Hook**：`.claude/settings.json` 加 `SessionStart`，调 `bash $(...)/scripts/setup-worktree.sh`
> - **手动入口**：`bash scripts/setup-worktree.sh` 始终可用
>
> 还有几个待确认的：
> 1. **`.wrangler/state`**（Cloudflare 本地 D1/R2 state）：要在 worktree 间共享吗？共享 = 多 worktree 看同一份本地 DB；隔离 = 各自独立。**取决于你会不会同时开多个 worktree 跑 dev**。
> 2. 除了 Claude Code，团队 / 你还用别的 agent 工具吗（Codex / Cursor / Gemini CLI）？要不要给它们也挂 hook？
> 3. 我没看到自定义 reference 仓库 / build 产物 share 需求，确认一下没有？
>
> 这套方案对吗？

### Step 3：基于回答收口，再补 1-2 个澄清

用户答完后，根据他的回答**只补必要的追问**。常见追问：

- 用户说"会并发跑多个 worktree" → 追问：「stateful 服务（`pgdata`、SQLite WAL）你希望并发隔离（Copy）还是共享（Share）？默认建议 Copy 防写花。」
- 用户说还用 Codex/Cursor/Gemini → 追问：「我对 X 的 hook 机制不熟，你贴下文档 / 你期望它怎么自动跑？最低我可以挂个 git `post-checkout` hook 兜底。」
- 用户提到自定义资源 → 追问：「这资源是 Share 还是 Copy？写得多吗？」

**不要再开新一轮问题列表**——能直接定的就直接定。

### Step 4：生成 + 验证

1. 拷 [`setup-worktree.sh`](setup-worktree.sh) 模板进 `<repo>/scripts/`
2. 按对齐结果填底部"资源声明"块（helper 函数那块原样）
3. 把对应 hook 配置（[`hook-config.json`](hook-config.json) 中选）合进 `.claude/settings.json`（多工具就多挂几个）
4. **跑两遍验幂等**：第一遍 link，第二遍全部 skip
5. 在新 worktree 真跑一次 `dev` / `test` 走端到端
6. 给用户汇报：装了什么、改了哪些文件、怎么手动跑

**更新已有脚本时**：用 Edit 工具 diff 式改资源声明块，**不动 helper 函数那段**（除非真的过时）。

## 三档策略（agent 用的判断框架）

| 档 | 例子 | 为什么 | 怎么做 |
|---|---|---|---|
| **Share**（symlink） | `node_modules`、包管理器缓存、跨 worktree 共享的 stateful DB | 省磁盘 + 省 install 时间；多 worktree 看同一份数据 | `ln -s $MAIN/<path> $WORKTREE/<path>` |
| **Copy** | secrets / env 文件、签名密钥、并发使用的 stateful 文件 | 各 worktree 可能调整；不能因 main 删了就烂；不能在并发写时撕裂 | `cp -R` 一次（再跑 skip） |
| **Generate** | dev 端口、`COMPOSE_PROJECT_NAME`、本地 socket | 每 worktree 必须不同 | `hash(branch) % range` 算端口；`clean_branch_name` 算容器名 |

**Stateful 数据**：单写者并发模式下必须 Copy（Postgres、SQLite WAL 都是单写者）；顺序使用可 Share。**这一项一定要在 Step 2 的"待确认"里列出来**，不能替用户拍。

## Agent 工具触发机制速查

| Agent 工具 | 触发机制 |
|---|---|
| Claude Code | `SessionStart` hook（最通用）/ `WorktreeCreate` hook（仅 `claude --worktree` 触发，stdout 契约严格：只 print path，进度走 `/dev/tty`） |
| Codex | 目前**没有等价 hook 机制**，建议手动脚本 + `post-checkout` git hook |
| Cursor | 同上 |
| Gemini CLI | **不熟，问用户文档** |
| Aider / 其它 | **不熟，问用户文档** |
| 多工具混用 / 不用 agent 工具 | 通用 fallback：`post-checkout` git hook + 手动 `bash scripts/setup-worktree.sh` |

**关键原则**：
- 不熟的工具**不要瞎编 hook 配置**。问用户。
- **永远保留手动入口** `bash scripts/setup-worktree.sh`。任何 hook 失效或换工具都不抓瞎。
- 多工具混用就**多挂几个 hook 调同一个脚本**。脚本本身已经是幂等的。

## 速查：常见资源 → 默认档

| 资源 | 默认档 | 备注 |
|---|---|---|
| 根 `node_modules/` | Share | npm workspaces hoist 处 |
| `apps/*/node_modules/`、`packages/*/node_modules/` | Share — **不能省** | bundler 从 workspace 内只往上找一层；`zod/v3` 这种 subpath exports 只在 workspace local |
| `.venv/`、`venv/` | Share（半只读） | shebang 有绝对路径；同机 OK |
| build cache（`.next/`、`target/`、`dist/`） | 跳过 或 Share | 通常重建够快 |
| `.env*`、`.dev.vars` | Copy | secret 不能 share |
| `*.wrangler/state`、`pgdata/`、`redis-data/` | **依并发模式，列入待确认** | share/copy 取决于并发 |
| dev 端口 | Generate | hash branch |
| `COMPOSE_PROJECT_NAME` | Generate | clean branch name |
| 自定义（reference 仓库 symlink、build 产物等） | **audit 时找，找不到就在 Step 2 列入待确认** | |

## 常见错误（写脚本时自查）

- **只链根 `node_modules`，漏了 workspace**：症状 `Could not read from file: .../zod/v4`。`apps/*` 和 `packages/*` 一起循环。
- **`git worktree add` 污染 stdout**（`WorktreeCreate` hook 下）：要 `>/dev/null 2>&1`，进度走 `/dev/tty`。
- **symlink 单写者 stateful 目录**：并发跑 dev 写花。Step 2 必须列入待确认让用户拍。
- **不幂等**：重跑必须全部 skip。模板 `link_resource` 已处理。
- **死链接**：`[ -e "$target" ]` 检查存在再链。
- **硬编码主仓库路径**：用 `git rev-parse --git-common-dir` 自动算。
- **`.env` 用 symlink**：必须 Copy（symlink 一改全改）。
- **跳过 audit 直接列问题轰炸用户**：先 audit，能推的推；问用户的是判断题，不是事实题。
- **替用户决定 stateful 怎么处理**：Step 2 必须问。

## 实现资源

- 脚本模板：[`setup-worktree.sh`](setup-worktree.sh)
- Hook 配置候选：[`hook-config.json`](hook-config.json)
- 各栈代码块：[`recipes.md`](recipes.md)

## 验证清单（生成 / 更新完跑一遍）

- [ ] fresh `git worktree add` 上跑脚本，exit 0
- [ ] 重跑 = no-op（全 "skip — already linked"）
- [ ] `npm run dev`（或对应栈命令）能起，无 "module not found"
- [ ] 测试 / typecheck 在新 worktree 通过
- [ ] 删主仓库 optional 资源 → log "skip" 不报错
- [ ] 用 `WorktreeCreate` 时：stdout 只有 worktree path
- [ ] **手动入口**（`bash scripts/setup-worktree.sh`）也能跑
- [ ] 用户对齐过的资源清单和实际生成一致
