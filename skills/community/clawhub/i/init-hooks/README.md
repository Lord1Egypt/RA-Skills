# init-hooks

> Run scripts automatically every time your OpenClaw agent's container/host boots — survives gateway restarts, container restarts, and container rebuilds. Registry-driven, idempotent, with inline / local-script / remote-CDN hook types.

`init-hooks` solves a common pain point for containerized AI agents: **initialization logic gets lost on container rebuild**. It keeps a persistent hook registry inside your workspace and re-runs your startup hooks on every boot.

## Features

- **Three hook types**
  - `inline` — a few shell commands, no file needed
  - `script` / `python` — a local `.sh` / `.py` file
  - `CDN URL` — a `zip` / `tar.gz` fetched & extracted on first run (auto re-download after container rebuild)
- **Survives rebuilds** — registry + logs live in `workspace/.init-hooks/` (mount your workspace on a persistent volume and hooks persist forever)
- **Idempotent install** — safe to re-run; auto-injects into `post-init.sh` and (optionally) the container start script
- **Lenient execution** — one failing hook never blocks the rest; every run is logged with a success/failure summary
- **Ordered execution** — control run order with `--order`
- **Full CRUD** — add / list / show / edit / enable / disable / delete / run / status
- **Config sync helper** — `sync_openclaw_config.py` keeps `openclaw.json` mirrored to extra persistence paths (configurable, see below)
- **Portable** — no hardcoded absolute paths; uses `$HOME` / `Path.home()` throughout

## Quick Start

```bash
# Clone (or install via clawhub / skills.sh)
git clone https://github.com/Songhonglei/better-agent-skills.git

# Point SCRIPT at wherever the skill landed in your agent, e.g.
#   OpenClaw:     ~/.openclaw/workspace/skills/init-hooks
#   Claude Code:  ~/.claude/skills/init-hooks
#   Cursor:       .cursor/skills/init-hooks
SCRIPT="/path/to/init-hooks/scripts/manage.py"

# 1. Install (idempotent)
python3 $SCRIPT install

# 2. Add a startup hook
python3 $SCRIPT add \
  --name "boot marker" \
  --type inline \
  --content 'echo "[boot] $(date)" >> "$HOME/.openclaw/workspace/.init-hooks/boot.log"'

# 3. Test it immediately
python3 $SCRIPT run

# 4. See what's registered
python3 $SCRIPT list
```

## Environment variables (deployment-specific)

Different deployments persist config in different places. These are optional:

| Variable | Purpose | Default |
|---|---|---|
| `INIT_HOOKS_SYNC_PATHS` | Extra `openclaw.json` mirror targets for `sync_openclaw_config.py` (colon-separated; missing paths skipped). Leave empty on plain local setups. | *(empty)* |
| `INIT_HOOKS_START_SH` | Container start-script path to inject the dispatcher into | `/app/start.sh` |

Example for a K8s / container deployment (replace with your own mount layout):

```bash
export INIT_HOOKS_SYNC_PATHS="/app/clawconfig/openclaw.json:/app/k8s-config/clawconfig/openclaw.json"
```

## Usage

Full command reference and hook-authoring best practices live in
[SKILL.md](./SKILL.md) and [references/best-practices.md](./references/best-practices.md).

## Install in your AI agent

| Agent | Install |
|---|---|
| OpenClaw | `clawhub install init-hooks` |
| Claude Code | Manual: copy to `~/.claude/skills/` |
| Cursor | Manual: copy to `.cursor/skills/` |

## License

MIT (see [LICENSE](./LICENSE))

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

### v1.0.4 (2026-11-14)

- **Fix（文档示例，真问题）**：`best-practices.md` 的 python 示例原本对每个持久化目标**各自打补丁**，目标文件里的旧值不会消失，重建后会把过期配置带回来——等于假同步。改为"只改 runtime，然后把 runtime 整份复制到各目标"，与 `sync_openclaw_config.py` 的实际语义一致
- **Fix（文档示例）**：示例里的 patch 不再写死键值，改由调用方通过环境变量传入，脚本本身不预设任何改动
- SKILL.md / 脚本 docstring 的 `--patch` 示例统一改成从用户给的文件读取，不再出现字面 JSON
- 无运行时逻辑变更

### v1.0.3 (2026-11-14)

- **Docs**：去掉 `acp` 相关示例（`--patch '{"acp": {"enabled": true}}'`、`enable-acp.py` 样例），改成中性的 `<section>/<field>/<value>` 占位写法。此前安全扫描据此判定"skill 主动开启 ACP 且未披露"（`TP4` HIGH），实际脚本只是原样透传用户给的 patch
- **Docs**：SKILL.md 与脚本 docstring 都写明能力边界——不预设默认值、不主动开启/关闭任何配置项，只写用户明确给出的字段并复制到配置的持久化路径
- 无代码逻辑变更

### v1.0.2 (2026-11-14)

- **Fix（安全）**：URL 钩子在 sha256 校验失败后不再执行上一轮遗留的脚本 —— dispatcher 的下载 / 解包 / 执行改为单条 `&&` 条件链，并在每次执行前删掉旧入口，任一步失败即"失败关闭"（此前会静默跑旧脚本，还把结果记成"成功"）
- **Fix（安全）**：解包不再调用 `tarfile.extractall` / `zipfile.extractall`，改为逐成员落盘：拒绝符号链接、硬链接、设备文件与 FIFO，拒绝绝对路径与 `..` 穿越，文件以 `O_NOFOLLOW` 写入，父目录逐级校验不跟随链接
- **Fix**：解包按内容识别格式（`zipfile.is_zipfile` / `tarfile.is_tarfile`），修复下载文件无扩展名导致压缩包被当成普通脚本拷贝、`*.zip` / `*.tar.gz` 分支永远走不到的问题
- 入口文件解析后校验必须仍在解压目录内
- `references/best-practices.md` 的环境变量示例改为写独立 env 文件，不再演示追加 `~/.bashrc`
- 新增 `tests/test_init_hooks_security.py`：覆盖校验失败失败关闭、链接/穿越/绝对路径/残留链接越界写入等 12 条用例

### v1.0.0 (2026-07-13)

- Initial public release
- Registry-driven startup hooks with inline / script / python / CDN-URL types
- Idempotent install, lenient ordered execution, run logging
- `sync_openclaw_config.py` config mirroring, now configurable via `INIT_HOOKS_SYNC_PATHS`
- Container start-script path configurable via `INIT_HOOKS_START_SH`
