# hd2-mod-authoring — an OpenClaw AgentSkill

An [OpenClaw](https://github.com/openclaw/openclaw) **skill** that teaches an AI
assistant how to author, install, and debug **Helldivers 2** mods on Linux.

It encodes the hard-won, field-verified lessons from shipping several real HD2
mods: the exact patch-container format, the memory layouts of the game's
settings tables, and the failure modes that each cost a game test.

## What it covers

- **Install classification** — Lua patch vs Wwise bank vs translation-only addon.
- **Writer-conflict detection** — catch two mods double-applying the same value.
- **Memory-patch discipline** — one scan, cached reads, field-selective maintain.
- **Value-scan safety** — full-signature guards for health/armor patching.
- **Programmable-ammo wheel** — the safe way to add a second selectable round.
- **Packing + deploy** — patch header format, Arsenal folder quirks, Nexus unlink.
- **Field-verified offsets** — ProjectileSettings, DamageSettings, WeaponData,
  WeaponMagazine, ProjectileWeapon, HealthComponentData.

## Layout

- `SKILL.md` — the skill body.
- `references/` — offsets and formats, HUD overlay recipes, and a scanned mod
  catalog.
- `examples/` — the two read-only diagnostics (`refscan` LDLD census, `fmscan`
  fingerprint value-scan) as worked reference implementations.
- `thumbnail.jpg` — repo/package artwork.

## Install

Via ClawHub:

```bash
openclaw skills install @Cavadus/hd2-mod-authoring
```

([ClawHub page](https://clawhub.ai/Cavadus/hd2-mod-authoring)) — add `--global` to
install for all local agents, or `--version <ver>` to pin a release.

Or install manually by copying the `hd2-mod-authoring/` directory into your
OpenClaw skills directory:

```bash
cp -r hd2-mod-authoring ~/.openclaw/agents/main/agent/workshop-skills/
```

## Caveats

Offsets, type hashes, and enum ids drift between game builds. The skill treats
them as verifiable hints, not constants — re-check any layout a game update
could move before trusting it.

## License

MIT
