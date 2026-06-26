# Artifact Contract

## `artifact_index.json`

Top-level index for all outputs that belong to one paper reading bundle.

Required keys:

- `schema_version`
- `paper_id`
- `report`
- `traceability_manifest`
- `latex_paragraphs`
- `research_lens`
- `direction_board`

Optional keys:

- `source_package`
- `pdfs`
- `notes`

## `traceability_manifest.json`

Maps report claims to source evidence.

Each claim entry should include:

- `claim_id`
- `section_id`
- `report_anchor`
- `statement`
- `interpretation_type`
- `confidence`
- `evidences`

Recommended extra fields:

- `research_role`
- `human_locators`

Each evidence entry may include:

- `evidence_id`
- `source_kind`
- `source_file`
- `paragraph_id`
- `page`
- `line_start`
- `line_end`
- `locator_method`
- `synctex`
- `quote_text`
- `notes`

## `latex_paragraphs.json`

Stable anchor list extracted from LaTeX.

Each paragraph entry should include:

- `paragraph_id`
- `source_path`
- `line_start`
- `line_end`
- `section_path`
- `kind`
- `text`

## `research_lens.json`

This is the compact idea-mining layer.
It should capture:

- research equation
- direction reconstruction
- challenge-to-module map
- module hidden assumptions
- citation logic
- reviewer-lens summary
- reusable story pattern
- strongest future directions
- links to top direction seeds

Every `claim_ids` entry inside `research_lens.json` must point to a real report claim.
Every seed referenced in `top_direction_seed_ids` should exist in `direction_board.json`.

## `direction_board.json`

This is the structured research-direction board for finding new research points.
It should rank testable directions derived from the paper.

Required top-level keys:

- `schema_version`
- `paper_id`
- `purpose`
- `source_confidence`
- `direction_seeds`
- `ranking_notes`
- `search_limitations`

Each `direction_seeds` entry should include:

- `seed_id`
- `title`
- `seed_type`
- `trigger_interpretation_type`
- `paper_anchor_claim_ids`
- `trigger_evidence_summary`
- `hidden_assumption_or_gap`
- `research_question`
- `hypothesis`
- `proposed_mechanism`
- `minimum_viable_experiment`
- `negative_result_interpretation`
- `killer_objection`
- `killer_result`
- `first_week_plan`
- `score`
- `risk_level`
- `expected_value`
- `confidence`

Allowed `seed_type` values:

- `assumption_violation`
- `unavailable_mechanism`
- `proxy_mismatch`
- `evidence_gap`
- `tiny_example`
- `successor_paper_gap`
- `reviewer_objection`
- `negative_result`
- `cross_domain_transfer`

Allowed `trigger_interpretation_type` values:

- `evidence-backed interpretation`
- `plausible inference`
- `speculation`

Recommended `score` fields:

- `novelty`
- `significance`
- `testability`
- `feasibility`
- `evidence_anchor`
- `risk_adjusted_value`
- `overall`

Each score should be on a 0-5 scale, with a short reason when possible.

## Report requirement

In `report.md`, every main-body claim bullet should appear in the form:

- `[C<section>.<index>][interpretation label] statement`

The detailed locator material should live in the final `# Appendix: Claim -> Evidence Index`, not inside the middle of the narrative body.

For each claim entry in the appendix, provide enough detail for a human verifier to know:

- which source file to open
- which section / subsection to inspect
- which line span or page span to inspect
- what quote snippet or excerpt window to look for
- what note or role explains why that evidence matters

## Claim typing

Allowed interpretation labels:

- `evidence-backed interpretation`
- `plausible inference`
- `speculation`

## Direction-board honesty

Do not label a direction as high confidence unless it is grounded in specific paper evidence or verified successor/reviewer context.
If successor-paper search was not performed, state this in `search_limitations` and avoid claiming novelty beyond the current source package.
