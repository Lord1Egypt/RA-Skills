# Munin Adapter for OpenClaw

## Install

```bash
pnpm --filter munin/openclaw build
```

## Run

```bash
MUNIN_BASE_URL=http://localhost:4000 \
MUNIN_PROJECT=default \
munin-openclaw capabilities
```

```bash
MUNIN_BASE_URL=http://localhost:4000 \
MUNIN_PROJECT=default \
munin-openclaw search '{"query":"munin"}'
```
