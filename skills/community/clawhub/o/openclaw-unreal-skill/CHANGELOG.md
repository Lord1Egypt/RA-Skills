# Changelog

All notable changes to OpenClaw Unreal Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-09-08

### Added
- Runtime confirmation gate in the gateway extension: project-changing tools
  (`actor.create`/`delete`/`setProperty`, `transform.set*`, `component.add`/`remove`,
  `level.open`/`save`, `asset.import`, `console.execute`, `input.simulate*`, PIE
  control) are refused unless the gateway was started with
  `OPENCLAW_EDITOR_ALLOW_DESTRUCTIVE=1` (or `OPENCLAW_UNREAL_ALLOW_DESTRUCTIVE=1`)
  **and** the call passes `confirm: true`. Unknown tool names fail closed.
- `dryRun: true` on `unreal_execute` — reports the classification and what would be
  sent, without sending it
- `destructiveOperations` state reported by `GET /unreal/status` and by
  `openclaw unreal status`
- `tests/gate.test.mjs` and `tests/dist.test.mjs` — gate behaviour, tool wiring and
  compiled-bundle parity, runnable without an Unreal Editor
- SKILL.md / SKILL_KO.md "Safety and permissions" section; README safety and
  development notes

### Changed
- Read-only tools (`level.getCurrent`, `actor.find`, `transform.get*`,
  `component.get`, `editor.getState`, `asset.list`, `blueprint.list`,
  `debug.hierarchy`, `debug.screenshot`, `console.getLogs`, `debug.log`) are
  unaffected — same behaviour as before
- Security & Privacy Disclosure now describes the gate instead of guidance alone

## [1.0.1] - 2026-07-08

### Added
- Frontmatter metadata (name, version, description, `disableModelInvocation: true`)
- Security & Privacy Disclosure section — HTTP server auth limitation, destructive-operation confirmation guidance, screenshot/log data visibility, safety defaults
- License section (Apache-2.0)

### Changed
- Description now discloses full capability surface (actor deletion, console commands, input simulation, captures) and trusted-project guidance

## [1.0.0] - 2026-02-15

### Added
- MCP Direct mode support (embedded HTTP server on port 27184)
- Claude Code / Cursor integration guide (`claude mcp add unreal`)
- Editor Panel documentation (Window → OpenClaw Unreal Plugin)
- MCP connection test cases (Mode A: Gateway, Mode B: Direct)

### Changed
- Synchronized with Unreal Plugin v1.3.0
- Updated tool count to 36 (from 40+)
- actor.create now defaults to StaticMeshActor (Cube, Sphere, Cylinder, Cone)
- actor.setProperty implemented via UE reflection system
- console.getLogs implemented with count/filter params
- editor.play uses RequestPlaySession (UE 5.7)
- editor.stop uses RequestEndPlayMap (fixes TaskGraph crash)

### Fixed
- Transform tools now work on dynamically created actors (StaticMeshActor has RootComponent)
- component.get accepts both `name` and `actor` params

## [0.9.4] - 2026-02-10

### Documentation
- Synchronized with Unreal Plugin v0.9.4
- Added UE 5.7 compatibility notes
- Added macOS Gatekeeper troubleshooting guide

## [0.9.3] - 2026-02-10

### Changed
- Synchronized with Unreal Plugin v0.9.3

## [0.9.2] - 2026-02-10

### Changed
- Rewrote extension to use OpenClaw Gateway SDK pattern
- Changed to `/unreal/*` endpoint structure
- Added toolCallId/arguments pattern (unified with Unity/Godot)
- Added 204 response for empty poll
- Added GetToolCount for registration

## [0.9.1] - 2026-02-10

### Added
- Added `disableModelInvocation` security documentation
- Added Korean documentation (SKILL_KO.md, README_KO.md)

### Fixed
- Added `openclaw.plugin.json` for gateway extension loading

## [0.9.0] - 2026-02-10

### Added
- Initial release
- Extension for OpenClaw Gateway integration
- Support for 40+ Unreal Editor tools
- HTTP endpoint handlers for plugin communication
