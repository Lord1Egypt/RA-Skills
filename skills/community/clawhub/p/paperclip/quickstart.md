# Quickstart — Paperclip

## Fastest Local Start

```bash
npx paperclipai onboard --yes
```

This boots a local instance with the default control plane at `http://localhost:3100`.

## Manual Repo Flow

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

Default local storage paths:

| Item | Path |
|------|------|
| Config | `~/.paperclip/instances/default/config.json` |
| Storage | `~/.paperclip/instances/default/data/storage` |
| Logs | `~/.paperclip/instances/default/logs` |

## Isolated Sandbox Instance

```bash
pnpm paperclipai run --data-dir ./tmp/paperclip-dev
pnpm paperclipai doctor --data-dir ./tmp/paperclip-dev
```

Use this when you want a clean throwaway instance for experiments or demos.

## First Operator Checks

```bash
pnpm paperclipai company list
pnpm paperclipai dashboard get
curl -s http://localhost:3100/api/companies
```

If the local server is not at `localhost:3100`, switch all commands to the configured API base.
