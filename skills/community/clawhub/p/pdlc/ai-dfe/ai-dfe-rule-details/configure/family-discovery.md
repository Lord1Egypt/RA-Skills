# Stage 1.1 — Family Discovery

> Phase 1 (Configure). Loaded when DFE needs to learn the family layout. Runs in full only on first encounter or `DAT__ discover`.

## Purpose

Learn which family DFE is operating on and the workspace anchors it needs — so gather (2.1) knows where to look. DFE navigates by what is **installed in the destination workspace**; it never decides placement and never depends on build-time registries.

> **Runtime-source rule (field-corrected, DHC-2026-06-23):** DFE does **not** read `FAMILY_TABLE_MAP.md` at runtime. That file is an internal build-time registry (workspace Rule 12) and is **not installed** into destination workspaces. The producer → role-folder mapping is **self-describing**: it comes from each package's own `SOURCE_MAP.md` (read in Stage 1.2). Family identity comes from the install manifest; the project set comes from `PROJECTS.md`.

## Inputs (all present in the destination workspace at runtime)

- `{family}-ws/.ai-family-manifest.json` — family install manifest (family code + installed packages). The family-identity anchor.
- `.kiro/{family}/ai-{pkg}-rule-details/data-schema/SOURCE_MAP.md` (per package) — each declares **its own** source paths (the producer → role-folder mapping, distributed not central).
- `{family}-ws/projects/PROJECTS.md` — the project registry.
- The workspace root and the `{family}-ws/` folder.

## Logic

1. Resolve the family code and workspace anchors:
   - Read `{family}-ws/.ai-family-manifest.json` for the family code + installed-package list. If absent, fall back to detecting the single `{family}-ws/` folder at the workspace root and the installed `.kiro/{family}/` rule-details.
   - Confirm `{family}-ws/` exists.
2. Record the family map in `dfe-state.md` under a `family` key: `{ code, workspaceRoot, dataRoot, projectsRoot, portfolioRoot, ideasRoot }` (derived from the `{family}-ws/` layout, which is fixed by the family workspace contract).
3. **Do not** build a central producer→role-folder table here — each package's `SOURCE_MAP.md` carries its own paths and is read in Stage 1.2 (Package Discovery). Stage 1.1 only establishes family identity + anchors + the project set.
4. Enumerate projects under `{family}-ws/projects/` (read `PROJECTS.md`) so cross-project (2.5) knows the project set.

## Output

`family` block in `dfe-state.md` + the project list. No data files are written in this stage.

## Edge Cases

| Situation | Behaviour |
|-----------|-----------|
| `{family}-ws/` absent | Installer didn't bootstrap; report and stop (nothing to fabric yet). |
| `.ai-family-manifest.json` absent | Degrade gracefully — derive the family code from the single `{family}-ws/` folder + installed `.kiro/{family}/`. Still functional. |
| `FAMILY_TABLE_MAP.md` "missing" | **Expected and correct** — it is a build-time registry, never installed. DFE must NOT require it. (This is why DHC-2026-06-23 PC-5 was reclassified — see `data-fabric-health-check.md`.) |
| `PROJECTS.md` empty | No projects yet — DFE still bootstraps an empty, valid data surface. |
| Multiple families present | Defer to master-mode resolution (`operate/cross-family.md`). |
