---
name: pixelkiln
description: Use PixelKiln to plan, generate, review, recover, audit, pack, and export manifest-driven pixel-art projects. Apply when a task uses the PixelKiln CLI, manifest, lockfile, or generated asset workflow; do not use for unrelated one-off image generation.
---

# PixelKiln

Treat generated pixel art as build output. Read the manifest, report the cost
before submission, stop for human review, and record the source and output
hashes.

## Working rules

- Locate `pixelkiln.manifest.json` first. Paths are manifest-relative.
- Give every new asset a descriptive `id` (`oak_tree`, `iron_sword`, not
  `asset_3` or `object1`). A vague id is cheap to write and expensive the
  moment another asset needs to reference it (`state.of`, `animation.of`,
  `revision.from`, `mirror`) or a person asks which one it was.
- Treat `style.extends` as a source-level variant, not a reason to copy the
  parent. Keep every child `outDir` explicit, inspect the resolved plan, and
  remember that a pixel-affecting parent edit intentionally makes children stale.
- Never inspect, print, or commit provider credentials. Read the top-level
  provider default and every style override, then load the matching provider
  references below.
- Run `pixelkiln doctor --dry-run` and `pixelkiln plan` before paid work. Report
  actionable, recoverable, and estimated cost figures with their provider unit.
- Do not regenerate recoverable work. Follow the exact zero-cost action printed
  by `plan`: `poll`, `pick`, `fetch`, or `restore`.
- Submit paid work only when the user has authorized generation. Always pass an
  explicit `--budget` no higher than the authorized estimate. For mixed work,
  pass one `--budget provider=amount` ceiling for every paid provider in the plan.
- Leave visual selection to the local `pixelkiln pick` review page unless the
  user explicitly provides a selection rule. Closing it applies nothing.
- To answer "what has this project generated?", use `pixelkiln gallery --json`
  for the offline provenance snapshot, or open `pixelkiln gallery` for the
  person to browse it. Both are read-only and contact no provider. Leave
  `gallery --edit` and `gallery --budget` to the person: an agent changes the
  manifest directly and spends only through `gen` with an explicit `--budget`.
- When a selected style declares `quality`, run manifest-mode `pixelkiln refine`
  after its source is accepted and downloaded. Read the quality reference below.
  Do not copy manifest-owned palette, path, interpreter, or threshold settings
  into flags.
  Never record approval without the named person's completed 1× review.
- When an asset declares `revision`, read the revision reference, require its
  parent gate to pass, and never bypass a `blocked` plan. Generate or approve
  the parent explicitly before re-planning the child.
- A character `state`, `animation`, `portrait`, `outfit`, `mirror`, or pro
  `styleCharacter` is a dependent asset the same way: one `pixelkiln gen` runs the waves in order
  and stops when the budget cannot cover the next one. Before declaring the
  east-facing loop of a character, check whether a `mirror` of the west one
  does the job for nothing (an animation's `directions` list declares the
  generated sides once and mirrors the rest; `--only <shorthand id>`
  selects the whole family); before drawing a base from text, ask whether the
  user has a south-facing sprite to `reference` instead (1 generation on
  `pro-flash` at 64px). Mirrors swap handedness.
- Outside art leaves this machine: `unzoom`, `pixelate`, and any `reference`
  or `styleImages` file are uploaded to PixelLab. Before the first upload, name
  the file(s) to the person and get their go-ahead, especially for unreleased
  or confidential art. Approving the generation budget is not consent to
  upload the source image, so ask for both.
- Before an outside or upscaled sprite becomes a `reference` or `styleImages`
  path, run `pixelkiln unzoom --from <file> --out <file>` to bring it back to
  its native pixel grid. Upscaled input degrades every PixelLab endpoint that
  takes a reference, and the unzoomed result is opaque. For outside art that
  was never pixel art (a photo, painting, or render), `pixelkiln pixelate
  --from <file> --out <file>` converts it with PixelLab's Image to Pixel Art
  Pro Flash for 6 generations and asks first. The result is opaque on
  near-white, so remove its background before using it as a cut-out.
- For a spell, hit, explosion, aura, pickup, projectile, or other animated
  effect, read the VFX reference below before choosing how to make it. Try
  the free sources first: PixelLab's workbench (`pixelkiln vfx --preset`,
  built around a `--sprite` when the effect must fit one) or the local
  pixelfx library (`pixelkiln vfx --lib pixelfx --effect <id>`, placed by its
  pivot). Keep the `.vfx.json` each run writes: its recipe renders the same
  effect again with `--recipe`.
- Treat every ComfyUI output as source material until it passes the native-grid,
  final-palette, prompt-coverage, and human 1× checks in the ComfyUI reference.
  A successful PNG or high-confidence grid result is not quality approval.
- Treat a ComfyUI `frames` asset as indivisible. Review its animated strip,
  refine and approve the complete set, and never package a subset of its roles.
- When the project commits a PixelKiln quality baseline, run `pixelkiln quality
  check --from <baseline>` before packaging. Treat a pass as structural
  continuity, never as human approval or proof that the prompt was satisfied.
- A regeneration keeps the generation it replaces: `pixelkiln history` lists
  them and `pixelkiln restore --only <asset> --style <style> --generation <n>`
  brings one back at no cost. When the person wants the previous result back,
  restore it; never regenerate to get there.
- Preserve manual edits and ownership errors. Inspect the difference before any
  `--force` operation. When the person wants to touch art up by hand, use
  `pixelkiln edit --only <asset> --style <style> --no-open`: it copies the
  generated PNG to `edits/` (one file per member for a frame or tile set) and
  declares it as the asset's source, so the generated file and lockfile stay
  the record and `plan` stays `ok`. The gallery's in-browser editor is for the
  person; `pixelkiln tools install editor` prefetches it without opening
  anything. Art changed in PixelLab's own editor comes back with
  `pixelkiln fetch --refresh`, never by regenerating.
- For ground, terrain, roads, or any set of tiles that must join, read the
  tiles reference below before picking a generator or exporting. Never read a
  tile's adjacency from its file name: the rule is in the lockfile entry, and
  `export --format generic` keeps all of it. Export to an engine only from
  generated, `ok` sets. `--merge-connected` is opt-in: offer it when the person
  wants one brush across sets that share a terrain, and never add it to an
  existing export command unasked.
- A `.glb` under a style's `outDir` is a 3D model, not a manifest asset. Its
  fixes go to an edited copy under `edits/` through `pixelkiln model`; the
  model as built is never written. Read the models reference below before
  listing, exporting, importing, or adopting a model's textures, before
  starting Blender for the person, and before `pixelkiln model normal-map`,
  the one model command that spends PixelLab generations.
- Commit the manifest, lockfile, generated outputs, and derived artifact
  companions. Never commit `.env.local` or `.pixelkiln/` cache data.

## Choose the smallest workflow

For ordinary work, prefer:

```bash
pixelkiln doctor --dry-run
pixelkiln plan
pixelkiln gen --budget <approved-provider-units>
pixelkiln audit --check
```

For a mixed plan, replace the single ceiling with repeated provider-keyed
ceilings copied from each plan group.

Use the staged `submit` → `poll` → `pick` → `fetch` commands when resuming or
debugging one phase. Use the plan's printed stage for paid work and `restore`
for missing downloaded bytes, `adopt` for exact matches
already in the provider account, and `salvage` for reviewed unclaimed objects
and characters.
Use `pack`, `mount`, or `export` only for the artifact format the project needs.
Prefer a manifest quality profile when a whole style shares the final-art rule.
Use `refine --from` only for a one-off candidate outside that contract, after
composition review and, for an isolated asset, background removal.

## Provider routing

Read only the reference needed for the current decision:

- For PixelLab configuration, generators (including `uiElement` for single UI
  pieces, `imageProFlash` for styled stills, and `vfx` for animated effects), costs, alpha behavior,
  account operations, or the `unzoom`, `pixelate`, `normal-map`, `vfx`, `font`, `estimate-skeleton`, and
  `skeleton-preview` utilities, read [references/pixellab.md](references/pixellab.md). For a
  PixelLab style aimed at a specific resolution or fidelity tier (retro,
  high-detail, or matching an existing set's look), read
  [references/pixellab-fidelity.md](references/pixellab-fidelity.md) first.
  Before proposing new PixelLab-backed work, check
  [references/pixellab-roadmap.md](references/pixellab-roadmap.md) for
  whether it is a confirmed gap or already covered and undocumented.
- For any animated effect, a `vfx` block, or the `pixelkiln vfx` command
  (PixelLab's workbench and paid artist, or the local pixelfx library), read
  [references/vfx.md](references/vfx.md). It covers which source to pick,
  every control, the files written, and how a game plays them.
- For ground, terrain, roads, connected tile sets, or exporting a tileset to
  Tiled, Godot or LDtk (`pixelkiln export`, including `--merge-connected`),
  read [references/tiles.md](references/tiles.md). It covers which generator
  to pick, how sets connect, every export format and what it refuses, and
  what has and has not been checked in an engine.
- For a scrolling background in layers, looping a background sideways, or
  parallax settings for Tiled, Godot, Phaser or LDtk, read
  [references/parallax.md](references/parallax.md).
- For Retro Diffusion styles, USD budgets, environment assets, animation, or
  experimental limits, read
  [references/retro-diffusion.md](references/retro-diffusion.md).
- For a self-hosted ComfyUI workflow, node bindings, local cost semantics, or
  portable output recovery, read [references/comfyui.md](references/comfyui.md).
- For Scenario models, Compute Unit ceilings, two-part credentials, or durable
  hosted-asset recovery, read [references/scenario.md](references/scenario.md).
- When a bundled or installed recipe can supply the workflow, model hashes, or
  quality contract, read [references/recipes.md](references/recipes.md).
- When an asset declares `revision`, read
  [references/revisions.md](references/revisions.md).
- When the person wants swappable outfits, hats, hair or held items on a
  character, or an asset declares `layer`, read
  [references/paperdoll.md](references/paperdoll.md).
- When a manifest style declares `quality`, or packaging is blocked on derived
  approval, read [references/quality.md](references/quality.md).
- When one game or repository needs more than one provider, read
  [references/mixed-providers.md](references/mixed-providers.md).
- When the project holds `.glb` models, or the person wants to fix a model's
  texture, see where a body part sits on its unwrap, bring paint back from
  Blender, or add normal map detail with PixelLab, read [references/models.md](references/models.md).

`FakeProvider` is the deterministic test adapter. Describe Scenario as
experimental: one BFL Flux 2 Dev profile is live-tested, while other model
schemas and broader batches are not. Do not describe Retro Diffusion as production-ready until representative
multi-candidate, tileset, GIF, and spritesheet live smoke tests pass.

When working in the PixelKiln repository, consult `docs/GETTING_STARTED.md` for
the full workflow, the matching provider setup guide, `docs/CLI.md` for flags,
`docs/MANIFEST.md` for the schema, and
`docs/RECOVERY.md` before account adoption, salvage, discard, or purge.
