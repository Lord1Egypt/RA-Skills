---
name: pixel-asset-compiler
description: Compile AI-generated pixel character references and separately named action sheets into deterministic, validated game assets. Use when Codex needs to inspect sprite actions, build or verify a sprite-asset manifest, remove flat backgrounds, slice and align frames, preserve detached effects, audit cross-frame consistency, request targeted regeneration for failed actions, package generic assets, or export a Godot 4 AnimatedSprite2D scene. Trigger for PNG sprite sheets, action strips, animation consistency checks, game-ready sprite exports, and AI-to-game asset workflows.
---

# Pixel Asset Compiler

Turn upstream AI sprite outputs into deterministic game assets. Keep semantics with the user or upstream generator; keep image processing and packaging with `pixel-asset`.

## Required Inputs

Require this package shape:

```text
character-source/
├── reference.png
├── actions/<action>.png
└── sprite-asset.manifest.json
```

Require one image per named action plus explicit `fps`, `loop`, and expected frame count when known. Read [references/manifest-v1.md](references/manifest-v1.md) before creating or changing a manifest.

Never invent action names, direction, FPS, loop behavior, or missing actions. Ask for missing semantics. Do not redraw supplied content or use normalization to hide identity, scale, weapon, or costume drift.

## Resolve The CLI

Prefer `pixel-asset` from `PATH`. If developing inside this repository, run `npm run cli:build` and use `packages/pixel-asset-cli/dist/pixel-asset.cjs`.

If unavailable, install the published CLI from npm:

```bash
npm install --global pixel-asset-compiler
```

## Workflow

1. Inspect the target game project and identify its engine and intended asset destination.
2. Verify that the reference is the sole character identity baseline and each action file contains exactly one named action.
3. Create or validate `sprite-asset.manifest.json`; keep fidelity options off unless the user explicitly requests reduced pixel scale or palette.
4. Run `pixel-asset inspect --input <input-dir>`. Stop on ambiguity and request the exact missing override or a regenerated action.
5. Run `pixel-asset compile --input <input-dir> --output <asset-dir>`.
6. Run `pixel-asset audit --input <asset-dir>` and read [references/quality-gates.md](references/quality-gates.md).
7. If any action fails, preserve the reference and all passed actions. Request or perform regeneration only for the named failed action, using the same reference and unchanged semantics. Recompile the full package after replacing it.
8. Run `pixel-asset validate --input <asset-dir>`.
9. For Godot, run `pixel-asset export --target godot --input <asset-dir> --output <godot-dir>`.
10. When Godot is installed, load the generated `.tscn` headlessly or in the target project before claiming completion.

For a deterministic end-to-end run, execute:

```bash
node <skill-dir>/scripts/run-workflow.mjs \
  --input <character-source> \
  --output <generic-asset-dir> \
  --target godot \
  --target-output <godot-asset-dir>
```

The script writes a workflow report and exits `0` only when all quality gates and the requested export pass. Exit `2` means user input or targeted regeneration is required.

## Failure Handling

Treat deterministic failures as evidence, not permission to guess.

- Structural ambiguity: ask for frame count/layout clarification or regenerate that action with clearer spacing.
- Visual consistency failure: keep passed actions and regenerate only the failed action.
- Background residue: retry deterministic cleanup once; if the audit still fails, regenerate that action on a flat solid background.
- Package or path failure: fix the manifest or filesystem issue; do not modify image content.
- Engine import failure: keep the generic package and fix only the exporter or destination path.

Do not report success from GIF appearance alone. Require `audit.passed`, `validation.passed`, the requested exporter result, and real engine loading when the engine is available.

## Final Report

Report:

- reference and action inputs used;
- manifest path and confirmed semantics;
- generic asset output;
- target-engine output;
- passed and failed actions;
- warnings or regeneration requests;
- whether engine loading was actually verified.
