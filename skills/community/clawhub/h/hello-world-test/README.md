# openclaw-hello-world

Minimal OpenClaw plugin for ClawHub testing. Registers a single `hello` tool and ships a matching skill.

## Files

```
hello-world/
├── package.json              # openclaw metadata (extensions, runtimeExtensions, compat)
├── openclaw.plugin.json      # plugin manifest
├── tsconfig.json
├── src/index.ts              # TypeScript source
├── dist/index.js             # built JS (runtimeExtensions target)
├── dist/index.d.ts
├── skills/hello-world/
│   └── SKILL.md              # tells the agent when to call `hello`
└── README.md
```

## Build

```bash
npm install
npm run build
```

## Install locally

```bash
openclaw plugins install -l ./hello-world
```

Then enable it in your OpenClaw config:

```json
{
  "plugins": {
    "entries": { "hello-world": { "enabled": true } }
  },
  "tools": { "allow": ["hello"] }
}
```

## Use

Ask your agent for a greeting. The bundled skill will route it to the `hello` tool:

> hi, give me a hello

→ `Hello, world!`

## Publish to ClawHub

```bash
clawhub package publish . --dry-run
clawhub package publish .
```

Note: ClawHub treats this as a **code plugin** (published with `clawhub package publish`), not a standalone skill package. The `SKILL.md` here ships *inside* the plugin to teach the agent when to call the tool — it's not what gets registered with ClawHub's skill registry.
