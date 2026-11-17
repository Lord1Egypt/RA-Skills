# Browser Deck Workflow

Use this workflow for self-contained 16:9 HTML or PDF slides. Inputs may be local structured data, local Markdown/text, or both. Do not offer native PowerPoint, 4:3 output, speaker-note export, a live data connection, or remote image downloading.

Choose exactly one mode:

| Mode | Source | Default patterns |
|---|---|---|
| Data | CSV/TSV/XLSX/JSON | `executive-brief`, `business-review` |
| Narrative | Markdown/text | `topic-explainer`, `project-update`, `proposal` |
| Hybrid | Markdown/text plus structured data | Any applicable pattern |

## Data Deck

Keep the established data workflow unchanged:

```bash
miao-viz data analyze /path/to/data.csv --intent "request and audience" --output SYSTEM_TEMP/miao-vision/context.json
miao-viz deck instantiate executive-brief --context SYSTEM_TEMP/miao-vision/context.json --output SYSTEM_TEMP/miao-vision/deck.yaml
miao-viz deck validate --spec SYSTEM_TEMP/miao-vision/deck.yaml --context SYSTEM_TEMP/miao-vision/context.json --verify --strict
miao-viz render deck --input /path/to/data.csv --spec SYSTEM_TEMP/miao-vision/deck.yaml --context SYSTEM_TEMP/miao-vision/context.json --strict --output ARTIFACT_PATH
```

Use `business-review` for a longer periodic review. Data and legacy decks require `--input`. Preserve generated evidence metadata, omit blocked slides, and never invent a metric.

## Narrative Deck

Analyze a local Markdown or text document with the user's goal and audience in the intent:

```bash
miao-viz deck analyze /path/to/brief.md --intent "explain the migration plan to engineering leadership" --output SYSTEM_TEMP/miao-vision/deck-context.json
miao-viz deck instantiate topic-explainer --context SYSTEM_TEMP/miao-vision/deck-context.json --output SYSTEM_TEMP/miao-vision/deck.yaml
miao-viz deck validate --spec SYSTEM_TEMP/miao-vision/deck.yaml --context SYSTEM_TEMP/miao-vision/deck-context.json --verify --strict
miao-viz render deck --spec SYSTEM_TEMP/miao-vision/deck.yaml --context SYSTEM_TEMP/miao-vision/deck-context.json --strict --output ARTIFACT_PATH
```

Use `project-update` for status, progress, risks, and next steps. Use `proposal` for problem, approach, trade-offs, decision, and action. Narrative render does not require `--input`.

The analyzer records remote image references but never downloads them. Treat source statements as `source-text` and agent-authored synthesis as `author-claim`; neither is data-verified. Every slide must retain valid source, section, or point references.

## Hybrid Deck

Use the same local data file in analyze and render:

```bash
miao-viz deck analyze /path/to/update.md --data /path/to/data.csv --intent "review progress and decide the next phase" --output SYSTEM_TEMP/miao-vision/deck-context.json
miao-viz deck instantiate project-update --context SYSTEM_TEMP/miao-vision/deck-context.json --output SYSTEM_TEMP/miao-vision/deck.yaml
miao-viz deck validate --spec SYSTEM_TEMP/miao-vision/deck.yaml --context SYSTEM_TEMP/miao-vision/deck-context.json --verify --strict
miao-viz render deck --input /path/to/data.csv --spec SYSTEM_TEMP/miao-vision/deck.yaml --context SYSTEM_TEMP/miao-vision/deck-context.json --strict --output ARTIFACT_PATH
```

Hybrid decks merge narrative structure with grounded data slides. Strict validation must report `objectCoverage: 1` and `claimCheckCoverage: 1` for data-grounded content. If render reports `DECK_DATA_SOURCE_MISMATCH`, use the exact data source recorded during `deck analyze`; do not substitute another file.

## Narrative And Grounding Rules

- Use at most one claim, four metrics, and one chart per main slide. Put detailed tables in an appendix or report.
- Data claims require `claimType`, `evidence`, `derivedFrom`, and `check`. Evaluative claims also require a real benchmark, target, baseline, or historical comparison.
- Every data chart and KPI needs provenance. Strict data/hybrid validation requires both provenance coverage values to equal `1`.
- Block causal and predictive claims. Do not infer strategic decisions, budgets, staffing actions, or forecasts from descriptive data.
- Preserve applicable `sampleWarnings` as caveats. A warning is not evidence and must not be hidden.
- Keep source-derived narrative distinguishable from agent-authored synthesis. Never label an author claim as verified.

## Review And Repair

Review the generated plan and DeckSpec before rendering. Repair the first structured issue, rerun strict validation, and never remove provenance or source references merely to silence a warning.

- Invalid source/section/point reference: select an identifier that exists in the same DeckContext.
- Missing pattern role: add the required role using supported content from the context.
- Narrative content budget: split or shorten the slide.
- Data block without data: remove it or re-analyze with `--data`.
- Evidence id/path error: use an existing evidence id and valid `$evidence:` path.
- Ungrounded numeric claim: add the complete grounding fields or rewrite it as non-numeric source text.
- Trend-period error: rewrite as a delta or remove the trend slide.
- Evaluative claim without benchmark: add a real benchmark or use descriptive language.
- Missing caveat: reference the applicable `sampleWarnings[].code`.
- Data source mismatch: render with the same file used by hybrid analysis.

## Render And Deliver

Resolve `ARTIFACT_PATH` using the shared delivery-directory rule; never pass the placeholder itself. Default to `magazine` when the user has no theme preference. Supported themes are `standard-white`, `magazine`, `standard-dark`, `minimal`, `nyt`, `bloomberg`, and `tableau`.

For PDF, reuse the strictly validated spec with `--format pdf` and a `.pdf` output. Each slide must produce one page. Playwright Chromium is required; surface structured `PDF_*` errors and layout diagnostics.

Prefer `value.delivery`. Show status, preview when available, and the primary HTML/PDF link. Include only claims or metrics present in the manifest, and never reread the full deck to invent a summary.
