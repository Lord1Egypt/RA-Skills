# Publishing `offlyn-clipper` to ClawHub

Updated: 2026-06-03

## Prerequisites

- [OpenClaw](https://docs.openclaw.ai) with `openclaw` CLI
- ClawHub CLI: `npm i -g clawhub` (or use `npx clawhub`)
- Skill verified locally:

```bash
openclaw skills install ./OpenClawPlugin/skills/offlyn-clipper --global
openclaw skills list --eligible | grep offlyn-clipper
bash OpenClawPlugin/skills/offlyn-clipper/scripts/setup.sh
```

## Publish

From this skill directory:

```bash
cd OpenClawPlugin/skills/offlyn-clipper
clawhub publish
```

Or sync all skills in a workspace:

```bash
clawhub sync --all
```

See [ClawHub publishing](https://docs.openclaw.ai/tools/creating-skills#publishing-to-clawhub).

## Keeping `mcp-bridge` in sync

The skill bundles `mcp-bridge/` for self-contained installs. After changing `OpenClawPlugin/mcp-bridge/`, refresh the copy:

```bash
rm -rf OpenClawPlugin/skills/offlyn-clipper/mcp-bridge
cp -R OpenClawPlugin/mcp-bridge OpenClawPlugin/skills/offlyn-clipper/mcp-bridge
```

## User install (post-publish)

```bash
openclaw skills install offlyn-clipper
# or
npx clawhub@latest install offlyn-clipper
```

Then run setup via the agent (`/offlyn-clipper`) or:

```bash
bash ~/.openclaw/skills/offlyn-clipper/scripts/setup.sh
```
