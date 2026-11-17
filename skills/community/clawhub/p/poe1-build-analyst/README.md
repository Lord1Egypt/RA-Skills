# PoE1 Build Generator and Verifier

This skill generates reproducible **Endgame-only** Path of Exile 1 analyses for a selected patch or league. It uses a supplied PoE Ninja DB record, public character payload, or complete PoB character code as the fixed source for the passive tree, gems, links, equipment, jewels, and configuration, then runs Path of Building Community calculations through `qpooqp777/pob-cli`. It no longer generates Early or Mid configurations in the active workflow.

The active default language is English. Localized documentation is available in [`README.zh-TW.md`](README.zh-TW.md), [`README.zh-CN.md`](README.zh-CN.md), [`SKILL.zh-TW.md`](SKILL.zh-TW.md), and [`SKILL.zh-CN.md`](SKILL.zh-CN.md).

## Repository version

The release candidate tracked in this repository is **0.1.2**, recorded in [`VERSION`](VERSION). ClawHub remains at `0.1.1` until the updated package is explicitly published; do not infer the registry version from this file.

## What it does

The generator accepts a league, main skill, class or ascendancy, game mode, economy, budget, and goal. It collects or accepts a permitted Ninja JSON snapshot, filters candidates, explains the ranking, and verifies selected PoB XML files when the local PoB Community root and LuaJIT are available.

Each result is delivered as one fixed Endgame record. The imported character data is not silently optimized or rewritten: the supplied passive tree, gems, links, equipment, jewels, and configuration remain authoritative. The report includes source provenance, PoB metrics, defensive thresholds, warnings, and limitations. Early and Mid are intentionally omitted.

## PoE 3.29 example

For a request such as “Recommend a PoE1 build for 3.29”, the generator uses **Curse of the Allflame** as the human-readable league example, then verifies the exact league identifier and retrieves a timestamped snapshot. It must not hard-code a “best build” from a video, search snippet, or popularity chart.

A report may compare candidate families such as `Vortex Occultist`, `Kinetic Fusillade Totems Hierophant`, and `Static Strike Slayer` when those candidates are actually present in the selected 3.29 snapshot. The example names are hypotheses, not a pre-certified tier list. The final choice must reflect the requested mode, budget, main skill, defensive expectations, and PoB verification state.

> The official 3.29.0 announcement identifies the challenge league as Curse of the Allflame and provides Standard, Hardcore, and Solo Self-Found variants.[1]

## Data and verification model

PoE Ninja is treated as statistical evidence. Its public build page is client-rendered, so the generator prefers a permitted JSON endpoint, data dump, user-provided export, public character data, or PoB code. It records the source URL, retrieval time, league, filters, response schema, and sample size. It does not bypass authentication, rate limits, or private-character access.

PoB Community is treated as the calculation authority. The generator first inspects skills, tree, and items, then runs `pob analyze` and `pob calc` with an explicit main skill. Missing LuaJIT, an invalid PoB root, unsupported XML, or a calculation failure produces a warning and an unverified result rather than invented numbers.

## Endgame character-code command

```bash
python scripts/poe1_build_pipeline.py endgame-analyze \
  --pob-code CHARACTER_CODE.txt \
  --pob-root "$POB_ROOT" \
  --skill "Vortex" \
  --class "Witch" \
  --ascendancy "Occultist" \
  --league "Curse of the Allflame" \
  --xml-output endgame_imported.xml \
  --output endgame_report.json
```

The command decodes the complete PoB character code, preserves the imported tree／gems／items, and invokes both `pob analyze` and `pob calc`. A short `https://pobb.in/<id>` URL is not a character code and is rejected; provide the complete code or a text file containing it. The command never uploads a build.

For a private code generated from an existing XML, use:

```bash
pob share BUILD.xml --dry-run
```

A public `pobb.in` link requires a separate, explicit confirmation. “Code generated” and “URL published” are different states.

## Optional passive-tree research utility

A deterministic `optimize-tree` subcommand remains available for offline research and candidate comparison, but it is not called by the Endgame character-code workflow. The active workflow never replaces the imported tree, gems, links, or equipment with an optimizer result.

```bash
python scripts/poe1_build_pipeline.py optimize-tree \
  --pob-root "$POB_ROOT" \
  --tree-version 3_29 \
  --class-id 3 \
  --target-nodes 112 \
  --objective cold-dot \
  --objective energy-shield \
  --objective curse \
  --required-node 32417 \
  --build BASELINE.xml \
  --skill Vortex \
  --output-xml optimized.xml \
  --output-json optimized.json
```

Valid objectives are `cold-dot`, `energy-shield`, `life`, `curse`, `spell`, `defence`, and `damage`. Required-node paths count against the node budget. An impossible required path, a disconnected candidate, or an invalid TreeData version is a hard failure. The command is an objective-weighted frontier search, not a proof of a global optimum; compare multiple objective sets when making a final recommendation.

## Output schema

The machine-readable report contains the league, build concept, source metadata, Ninja candidates, stage records, PoB verification status, character-code state, and warnings. The human-readable report separates four evidence classes: **Ninja observations**, **official PoB calculations**, **manual recommendations**, and **unverified estimates**.

| Active record | Source | Decision gate |
| --- | --- | --- |
| Endgame only | PoE Ninja DB / public character data / complete PoB character code | Preserve imported tree, gems, links and gear; verify with `pob analyze` and `pob calc`. |

## Included resources

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Active English instructions loaded by Manus. |
| `scripts/poe1_build_pipeline.py` | JSON normalization, non-uploading PoB analysis wrapper, and `optimize-tree` subcommand dispatcher. |
| `scripts/poe1_tree_optimizer.py` | Connected passive-tree optimizer with required/excluded nodes and optional PoB calculation. |
| `references/api_reference.md` | API and CLI usage notes. |
| `references/research_notes.md` | Verified limitations and 3.29 notes. |
| `templates/character_build.json` | Machine-readable character/build template. |

## References

[1]: https://www.pathofexile.com/forum/view-thread/3985332 "Content Update 3.29.0 — Path of Exile: Curse of the Allflame"
[2]: https://poe.ninja/poe1/builds "PoE Ninja — Path of Exile 1 Builds"
[3]: https://github.com/qpooqp777/pob-cli "qpooqp777/pob-cli"
