# OpenClaw Encyclopedia Workflow

## Core stance

Use official OpenClaw docs plus local observed state together.

Default order:
1. check `.OpenClaw-Encyclopedia/` cache/notes
2. check official docs when needed
3. inspect live environment state
4. answer or act
5. record durable learnings

## When docs lookup is mandatory

Do a docs lookup before answering or acting when any of these are true:
- the user asks about OpenClaw command syntax, feature semantics, or configuration behavior
- the task involves gateway config, auth/security, skills, plugins, sessions, channels, nodes, messaging, automation, cron, heartbeat, pairing, or sandboxing
- the task involves a version-sensitive feature or a behavior you are not highly confident about
- the task involves live CLI/config work and the command path or safety boundaries matter

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/...`
- `.OpenClaw-Encyclopedia/notes/components/...`
- `.OpenClaw-Encyclopedia/notes/patterns/...`
- `.OpenClaw-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the official docs and then cache what you used.

## How to cache docs

Use `scripts/cache_doc.py`.

Typical usage:

```bash
python3 scripts/cache_doc.py \
  --url 'https://docs.openclaw.ai/tools/skills' \
  --root '<workspace>/.OpenClaw-Encyclopedia'
```

The script will:
- fetch the page
- convert it into a normalized markdown-ish cache file
- place it under `.OpenClaw-Encyclopedia/docs/docs.openclaw.ai/...`
- add metadata such as source URL and fetch timestamp

## How to store local knowledge

### Component notes

Use `.OpenClaw-Encyclopedia/notes/components/<component-name>.md` for:
- component purpose
- access path
- role in deployment
- sensitive boundaries
- discovered quirks

### Pattern notes

Use `.OpenClaw-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring command/config patterns
- repeated gotchas
- safe operational sequences
- environment-specific design conventions

### Inventory files

Use `.OpenClaw-Encyclopedia/inventory/` for:
- deployment/access inventory
- topology/runtime layout
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Official docs** — from OpenClaw documentation
- **Observed local state** — from live environment inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## Recommended answer style

When it helps, mention whether your answer is based on:
- cached official docs
- freshly checked official docs
- live environment inspection
- best-practice inference

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- gateway config and auth/security changes
- channel/messaging behavior changes
- automation, cron, or heartbeat behavior
- skills/plugins/tool exposure changes
- pairing or remote-access changes
- changes that could break access, routing, or message delivery

For these, prefer docs lookup even if you think you remember the command or config key.
