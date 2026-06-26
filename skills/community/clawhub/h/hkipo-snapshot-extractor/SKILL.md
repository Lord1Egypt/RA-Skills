---
name: hkipo-snapshot-extractor
description: Extract a structured Hong Kong IPO snapshot with company fields, offer mechanics, timing, source provenance, and field-level quality signals. Use when the user asks about one IPO symbol, wants normalized facts, or needs machine-readable IPO data before scoring.
version: 0.1.0
metadata: {"openclaw":{"emoji":"🧾","requires":{"bins":["uv"]},"install":[{"id":"install-uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv with Homebrew","os":["darwin","linux"]}]}}
---

# HK IPO Snapshot Extractor

Use this skill for read-only single-symbol analysis.

## Runtime

This publish bundle includes the required CLI runtime under `runtime/hkipo-next`.

From the skill folder:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next ...
```

## Workflow

1. Run `snapshot` for the target symbol.
2. Use `--format json` when another skill will consume the result.
3. Check `issues`, `quality.missing_fields`, `quality.conflicts`, and `quality.overall_confidence` before making strong claims.
4. Build human summaries from the normalized fields instead of paraphrasing raw upstream pages.

## Commands

Machine-readable snapshot:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next snapshot 2476 --format json
```

Readable markdown snapshot:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next snapshot 2476 --format markdown
```

Export a snapshot file:

```bash
cd <skill_dir>
uv run --directory runtime/hkipo-next hkipo-next snapshot 2476 --format markdown --output /tmp/2476-snapshot.md
```

## Output Cues

- `field_sources` shows which upstream source won per field.
- `quality.conflicts` exposes alternate values when sources disagree.
- `meta.degraded` or `meta.data_status=partial` usually means the snapshot is usable with caveats, not unusable.

## Companion Skills

- Use `$hkipo-parameter-manager` before scoring if the user wants to tune rules.
- Use `$hkipo-decision-engine` when the user wants a participation recommendation.
