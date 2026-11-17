# 🦞 OpenClaw Unreal Skill

OpenClaw skill for Unreal Engine integration. Works with the [OpenClaw Unreal Plugin](https://github.com/openclaw/openclaw-unreal-plugin).

## ⚠️ Disclaimer

This software is in **beta**. Use at your own risk.

- Always backup your project before using
- Test in a separate project first
- The authors are not responsible for any data loss or project corruption

See [LICENSE](LICENSE.md) for full terms.

## Installation

```bash
# Clone or copy to OpenClaw workspace
cp -r openclaw-unreal-skill ~/.openclaw/workspace/skills/unreal-plugin
```

## Structure

```
openclaw-unreal-skill/
├── extension/
│   ├── index.ts       # Tool definitions, handlers, safety gate
│   ├── dist/index.js  # Compiled bundle
│   ├── openclaw.plugin.json
│   └── package.json   # Extension metadata
├── tests/
│   └── gate.test.mjs  # Safety-gate tests (no Unreal needed)
├── SKILL.md           # Skill documentation
├── README.md          # This file
└── LICENSE.md         # Apache-2.0
```

## Safety

Read-only tools (`level.getCurrent`, `actor.find`, `transform.get*`,
`debug.hierarchy`, `debug.screenshot`, `console.getLogs`, ...) run as they always
have. Every project-changing tool — `actor.create`/`delete`, `level.save`,
`asset.import`, `console.execute`, `input.simulate*`, PIE control — is **refused
by default** and needs two independent opt-ins:

```bash
# 1. the operator enables project changes on the gateway process
OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1 openclaw gateway restart
```

```
# 2. the call confirms that specific change, after asking the user
unreal_execute: actor.delete {name: "Cube_01"}, confirm: true
```

`dryRun: true` previews any call without sending it. `openclaw unreal status`
shows whether project changes are currently enabled. Full details in
[SKILL.md → Safety and permissions](SKILL.md#safety-and-permissions).

## Development

```bash
# Run the safety-gate tests (Node 22.18+ / 24 — no Unreal Editor required)
node --test --test-force-exit tests/*.test.mjs

# Rebuild extension/dist/index.js after editing extension/index.ts
npx --yes esbuild@0.21.5 extension/index.ts --bundle --format=esm \
  --platform=node --target=esnext --external:openclaw \
  --outfile=extension/dist/index.js
```

## Usage

Once installed, the skill is automatically loaded by OpenClaw. Use natural language to interact with Unreal Editor:

- "Show me the level hierarchy"
- "Create a cube at position 100, 200, 50"
- "Start play mode"
- "Take a screenshot"
- "Move the player start to the origin"

## Requirements

1. OpenClaw Gateway running
2. Unreal Engine project with OpenClaw Plugin installed
3. Plugin connected to gateway

## Tools

See [SKILL.md](SKILL.md) for complete tool documentation.

## License

MIT License

## License

This project has been licensed under [Apache-2.0](LICENSE) since its initial release.
Copyright 2026 Tom Lee (TomLeeLive)
