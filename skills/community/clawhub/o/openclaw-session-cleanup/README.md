# OpenClaw Session Cleanup Skill

An OpenClaw-native operations skill for diagnosing and stabilizing long-running OpenClaw deployments. It targets session buildup, gateway instability, browser-control timeouts, websocket `1006` closures, and small-VPS resource exhaustion.

Chinese README:
[README.zh-CN.md](https://github.com/NeoCh3n/openclaw-session-cleanup-skill/blob/main/README.zh-CN.md)

## OpenClaw-Native Layout

This repo now follows the OpenClaw skill model:

- the skill entrypoint is [`SKILL.md`](./SKILL.md)
- the repo can be copied directly into `~/.openclaw/skills/`
- it can also be published with `clawhub publish`

OpenClaw’s docs describe a skill as a folder with `SKILL.md`, loaded from `~/.openclaw/skills` or `<workspace>/skills`, and ClawHub can publish/install those folders directly. Source docs:
[Skills](https://docs.openclaw.ai/tools/skills),
[Creating Skills](https://docs.openclaw.ai/tools/creating-skills),
[ClawHub](https://docs.openclaw.ai/tools/clawhub)

## Repository Layout

```text
.
├── SKILL.md
├── LICENSE
├── README.md
├── README.zh-CN.md
├── docs/
│   └── openclaw.session_cleanup_v1.md
├── scripts/
│   ├── install-cron-prune.sh
│   ├── install-to-openclaw.sh
│   ├── install-watchdog.sh
│   └── render-openclaw-config.sh
└── templates/
    ├── openclaw-watchdog.service
    ├── openclaw-watchdog.timer
    └── openclaw.json
```

## One-Command Install For New Users

Install directly from GitHub into shared OpenClaw skills:

```bash
curl -fsSL https://raw.githubusercontent.com/NeoCh3n/openclaw-session-cleanup-skill/main/scripts/install-to-openclaw.sh | bash
```

This installs the skill to:

```bash
~/.openclaw/skills/openclaw-session-cleanup
```

Then start a new OpenClaw session, or restart the gateway so the skill is indexed.

Manual alternative:

```bash
git clone https://github.com/NeoCh3n/openclaw-session-cleanup-skill.git
cd openclaw-session-cleanup-skill
bash ./scripts/install-to-openclaw.sh
```

Workspace-only install:

```bash
mkdir -p <your-workspace>/skills
cp -R ./openclaw-session-cleanup-skill <your-workspace>/skills/openclaw-session-cleanup
```

## What The Skill Does

Use it when an OpenClaw deployment shows:

- too many active sessions
- `browser control service timeout`
- `gateway 1006 abnormal closure`
- repeated disconnects after long uptime
- memory pressure on `1 vCPU / 2 GB RAM` hosts

It packages:

- the native skill definition in [`SKILL.md`](./SKILL.md)
- the runbook in [`docs/openclaw.session_cleanup_v1.md`](./docs/openclaw.session_cleanup_v1.md)
- runtime and watchdog templates in [`templates/`](./templates)
- installation helpers in [`scripts/`](./scripts)

## Usage Examples

After installation, ask OpenClaw things like:

- `My OpenClaw gateway starts closing with 1006 after a few days. Diagnose it.`
- `Sessions: 16 active, Agents: 6, browser control timeout. Stabilize this runtime.`
- `Give me a safe OpenClaw config for a 2 GB VPS.`

## Included Resources

- [`SKILL.md`](./SKILL.md): native OpenClaw skill entry
- [`docs/openclaw.session_cleanup_v1.md`](./docs/openclaw.session_cleanup_v1.md): detailed troubleshooting playbook
- [`templates/openclaw.json`](./templates/openclaw.json): recommended runtime defaults
- [`templates/openclaw-watchdog.service`](./templates/openclaw-watchdog.service): watchdog service
- [`templates/openclaw-watchdog.timer`](./templates/openclaw-watchdog.timer): watchdog timer
- [`scripts/install-cron-prune.sh`](./scripts/install-cron-prune.sh): install recurring prune
- [`scripts/install-watchdog.sh`](./scripts/install-watchdog.sh): install watchdog unit files
- [`scripts/render-openclaw-config.sh`](./scripts/render-openclaw-config.sh): render runtime config JSON

## Publish To ClawHub

OpenClaw’s ClawHub docs show these publish/install flows:

```bash
clawhub login
clawhub publish . --slug openclaw-session-cleanup --name "OpenClaw Session Cleanup" --version 1.0.0 --tags latest,openclaw,ops
```

Later updates:

```bash
clawhub sync --all
```

For users, the standard install flow is:

```bash
clawhub install <skill-slug>
```

## License

MIT. See [`LICENSE`](./LICENSE).
