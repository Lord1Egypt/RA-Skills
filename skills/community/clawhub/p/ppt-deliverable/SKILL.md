---
name: ppt-deliverable
description: Turn financial-services outputs into slides or a PowerPoint deck. Use when the user wants a strip, teaser, pitch material, refreshed deck, or a banker-ready .pptx generated from this plugin.
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


# PPT Deliverable

Use this skill when the final output should be a PowerPoint artifact.

## Best-fit cases

- single-slide strip profile
- teaser or process letter deck
- refreshed deck after number changes
- customer or deal summary slides
- packaging analysis into presentation-ready pages

## CN target pre-flight (MANDATORY when target is a Chinese-market entity)

Before touching any pptxgenjs slide code, check whether the target company is a China-market entity. If the context mentions any of the following triggers:

- **Market/regulator**: 中国 / A股 / 港股 / 科创板 / 创业板 / 北交所 / 中概股 / H股 / 证监会 / 上交所 / 深交所 / 港交所
- **Source systems**: 巨潮资讯 / cninfo / Tushare / 天眼查 / 企查查
- **Common China-market tickers**: `*.SH` / `*.SZ` / `*.BJ` / `*.HK`

...then you MUST load and follow the [`cn-client-investigation`](../cn-client-investigation/SKILL.md) skill before generating any slides. That skill enforces:

- **Rule 1**: write Chinese in UTF-8 literal, NEVER as `\uXXXX` escape sequences — MiniMax-M2.7 has documented character-level drift on long Chinese escapes (e.g. 寒武纪 → 宽厭谛79)
- **Rule 2**: for company names / section headers / financial line items / investment ratings, require the `cn-lexicon.js` literal dictionary instead of inline-typing Chinese
- **Rule 3**: cover pages use English 44pt as hero title + Chinese ≤28pt as subtitle (English ASCII has zero escape-typo risk)
- **Rule 4**: tier-ordered China-market data sources (Tushare / CNINFO / 交易所 / 天眼查 / FMP)
- **Rule 5**: every hard number in the analysis.md must have a matching row in `data-provenance.md` — verified via `provenance_verify.py`
- **Rule 6**: no fabrication on missing data — label "数据不可得" / "N/A" instead
- **Rule 7**: `cn_typo_scan.py` is a **mandatory compile-time gate** — your `slides/compile.js` must be based on `references/compile_with_typo_gate.template.js.txt` (strip the `.txt` suffix on copy) so a scan hit blocks the pptx from shipping

For non-CN targets, skip this pre-flight and use the regular `ppt-deliverable` routing below.

## Tooling preference

Route PPT generation through the host's MiniMax PPT stack. On `macmini`, that means:

- `pptx-generator` for create/read flows
- `slide-making-skill` for single-slide implementation details
- `ppt-orchestra-skill` for multi-slide planning
- `ppt-editing-skill` for editing existing decks safely

If that PPT stack is not exposed on the host, fall back to the standard `pptx` workflow already available in the environment.

> **Note on removed path (0.1.17)** — versions 0.1.13 through 0.1.16 shipped an embedded `aigroup-mdtopptx-mcp` stdio server that converted markdown to `.pptx` via `pptxgenjs` with a banker template derived from the NVIDIA sample. In practice the MiniMax host PPT skill suite produces noticeably better banker decks, so 0.1.17 removed the embedded server to let routing converge on a single good path. Archive of the `scripts/mdtopptx/` directory is retained in the repository for reference but is no longer registered in `.mcp.json`.

Do not treat shell discovery as the source of truth. Avoid `which`, PATH checks, or binary-name probes for PPT routing because these capabilities may exist only as host skills.

The core rule is:

- ship a real `.pptx`
- preserve template structure when one exists
- keep slides concise and presentation-native
- prefer editable text/table/chart objects over flattened screenshots

Preferred routing order:

1. host MiniMax PPT skills — `pptx-generator`, `slide-making-skill`, `ppt-orchestra-skill`, `ppt-editing-skill`
2. environment `pptx` fallback when the MiniMax stack is not exposed

**CN exception (overrides order above):** For any company matched by the CN pre-flight above, the pptxgenjs route (`slides/slide-NN.js` + `node slides/compile.js`) is MANDATORY — not optional, not a fallback. The MiniMax PPT stack does not integrate the compile-time typo gate required by `cn-client-investigation`. Do NOT use python-pptx for slide generation under any circumstances; it produces unthemed white-background slides. See `cn-client-investigation/SKILL.md` Phase 4 for the required steps.

**CN deck-numbers flow (v0.9.0+):** Before writing `slides/slide-NN.js`, run `extract_deck_numbers.py <deliverable_dir>` to emit `deck-numbers.json`. Each slide module should import numbers from that lookup rather than re-typing values from analysis.md prose. `slide_data_audit.py` (Gate 2b) remains the post-compile enforcement — every number on a slide must map to a provenance row. Combined with `raw_data_check.py` (Gate 3c), this closes the loop `raw-data/*.json → data-provenance.md → deck-numbers.json → slides/*.js → pptx`.

## Workflow

### Step 1: Decide whether this is create vs refresh

Use the smallest path that matches the job:

- new deck / new slide
- refresh an existing deck
- fill a template

### Step 2: Start from existing plugin skills

Prefer these building blocks:

- `strip-profile`
- `teaser`
- `pitch-deck`
- `deck-refresh`
- `process-letter`
- `competitive-analysis`
- `customer-analysis-pack`

If the user already has source tables in Excel or text in Word/markdown, consume those as inputs rather than recreating the analysis.

If the source is already markdown or markdown-like analysis output, feed it to the host's MiniMax PPT skills (`pptx-generator` / `slide-making-skill`) rather than trying to script the conversion manually — MiniMax preserves banker-style layout far better than a hand-rolled pptxgenjs pipeline.

### Step 3: Build the deck

Requirements:

- use real slide structure, not giant paragraph dumps
- keep numbers synced with underlying models
- match the provided template or established banker style
- use tables/charts where they communicate better than prose
- keep the output editable in PowerPoint / Keynote
- do not stop just because no same-named PPT executable exists in the shell

### Step 4: Review before delivery

Check:

- no text overflow
- slide titles are meaningful
- numbers and dates are internally consistent
- all placeholders are removed

If the user also needs a PDF review copy, generate the PPT first, then hand off to `pdf-deliverable`.

## Output standard

Deliver:

1. a `.pptx`
2. a quick description of slide coverage
3. any data points that still need verification before external use

## Quality checklist

- final artifact is a real `.pptx`
- the final artifact remains editable rather than being flattened into image-only slides
- slides are presentation-ready, not document pages pasted into PowerPoint
- formatting is consistent with the source template or banker style
- charts/tables reflect current numbers
- no placeholder or draft scaffolding remains
