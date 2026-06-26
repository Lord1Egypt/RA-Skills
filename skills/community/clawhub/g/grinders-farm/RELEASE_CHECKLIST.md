# Grinder's Farm — Release checklist

**Languages:** [English](#english) · [中文](#中文)

---

## English

Goal: verify a fresh install from a stranger’s machine — skill + plugin install, run, and push.

### 1) Code & packages

- [ ] `npm install`
- [ ] `npm run build`
- [ ] `npx tsx src/adapters/oneshot.ts help` prints help
- [ ] `package.json` `main` / `bin` / `types` / `files` / `license` OK
- [ ] Root has `LICENSE`
- [ ] `openclaw-plugin/` has `README.md`, `openclaw.plugin.json`, `LICENSE`

### 2) Paths & env (cross-machine)

- [ ] No hard-coded machine paths (e.g. `/Users/<name>/...`)
- [ ] Plugin resolves runtime without `gameRoot` when possible
- [ ] Fallback: `GRINDERS_FARM_ROOT` or `gameRoot`
- [ ] `OPENCLAW_BIN` can override `openclaw` path (notify/worker)
- [ ] `npm run sync-skill` works outside Homebrew paths

### 3) Gameplay (new user)

- [ ] `reset` still gives an order on day 1
- [ ] `help` matches real commands
- [ ] `shop` shows base price / today price / per-unit profit
- [ ] `sell` shows market feedback

### 4) OpenClaw plugin

- [ ] `openclaw plugins uninstall grinders-farm --force` (clean old)
- [ ] `openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install` works without source
- [ ] `openclaw plugins list` shows `grinders-farm` as loaded
- [ ] `openclaw plugins inspect grinders-farm` OK

### 5) Skill

- [ ] Remove old skill: `~/.openclaw/workspace/skills/grinders-farm/`
- [ ] `openclaw skills install grinders-farm` (ClawHub) works
- [ ] `openclaw skills info grinders-farm` is ready
- [ ] `command-dispatch` + `command-tool` work

### 6) Channels & push

- [ ] Telegram: `/farm farm` returns image + short caption
- [ ] Telegram: `/farm shop` is text-only (no stale image)
- [ ] Each target channel: `/farm ...` once to bind
- [ ] After `/farm start`, push fans out to all bound channels
- [ ] WebChat receives push via `chat.inject`

### 7) Auto-advance & processes

- [ ] After `/farm start`, only one worker
- [ ] `/farm stop` stops workers
- [ ] Gateway restart: `autoBoot` matches config

### 8) Smoke commands

- [ ] `farm`
- [ ] `plant carrot A1`
- [ ] `water`
- [ ] `harvest`
- [ ] `inventory`
- [ ] `sell`
- [ ] `start`
- [ ] `stop`

### 9) Before release

- [ ] `README.md` matches real install steps
- [ ] `SKILL.md` matches game rules
- [ ] Version bumped and matches release notes
- [ ] No secrets committed (tokens, keys, accounts)

---

## 中文

目标：按「外部用户从零安装」视角，确认 skill + plugin 可安装、可运行、可推送。

### 1) 代码与包体

- [ ] `npm install`
- [ ] `npm run build`
- [ ] `npx tsx src/adapters/oneshot.ts help` 可正常输出命令帮助
- [ ] `package.json` 的 `main/bin/types/files/license` 已检查
- [ ] 根仓库包含 `LICENSE`
- [ ] `openclaw-plugin/` 包含 `README.md`、`openclaw.plugin.json`、`LICENSE`

### 2) 路径与环境（跨机器）

- [ ] 全仓无机器私有绝对路径（如 `/Users/<name>/...`）硬编码
- [ ] 插件可在无 `gameRoot` 明确配置时尝试自动探测运行时
- [ ] 失败时可通过 `GRINDERS_FARM_ROOT` 或 `gameRoot` 手动指定
- [ ] `OPENCLAW_BIN` 可覆盖 `openclaw` 可执行路径（notify/worker 场景）
- [ ] `npm run sync-skill` 在非 Homebrew 路径机器可用

### 3) 游戏体验（新用户）

- [ ] `reset` 后首日即有订单（不需等第二天）
- [ ] `help` 文案与真实命令一致
- [ ] `shop` 文案包含原价/今日售价/今日单个利润
- [ ] `sell` 文案包含市场反馈（压价感知）

### 4) OpenClaw Plugin 安装与加载

- [ ] `openclaw plugins uninstall grinders-farm --force`（清理旧安装）
- [ ] `openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install` 可直接安装（无需源码）
- [ ] `openclaw plugins list` 中 `grinders-farm` 状态为 loaded
- [ ] `openclaw plugins inspect grinders-farm` 可正常返回详情

### 5) Skill 安装与加载

- [ ] 清理旧 skill：`~/.openclaw/workspace/skills/grinders-farm/`
- [ ] `openclaw skills install grinders-farm`（ClawHub）可直接安装
- [ ] `openclaw skills info grinders-farm` 状态为 ready
- [ ] `command-dispatch` 与 `command-tool` 配置生效

### 6) 渠道与推送验证

- [ ] Telegram 中执行 `/farm farm` 返回图片 + 精简 caption
- [ ] Telegram 中执行 `/farm shop` 为文本-only（不附旧图）
- [ ] 在每个目标渠道各执行一次 `/farm ...` 完成绑定
- [ ] `/farm start` 后自动推送可 fan-out 到所有已绑定渠道
- [ ] webchat 通过 `chat.inject` 收到推送

### 7) 自动推进与进程治理

- [ ] `/farm start` 后仅 1 个 worker 运行
- [ ] `/farm stop` 可停止全部 worker
- [ ] 重启 Gateway 后 autoBoot 行为符合配置

### 8) 回归命令冒烟

- [ ] `farm`
- [ ] `plant carrot A1`
- [ ] `water`
- [ ] `harvest`
- [ ] `inventory`
- [ ] `sell`
- [ ] `start`
- [ ] `stop`

### 9) 发布前信息

- [ ] `README.md` 安装步骤与实际命令一致
- [ ] `SKILL.md` 与当前玩法逻辑一致
- [ ] 版本号已更新并与发布说明一致
- [ ] 确认不提交本地敏感配置（token、私钥、账号）
