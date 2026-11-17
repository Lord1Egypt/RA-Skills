# Real-Score Benchmark Protocol

Maintenance targets are editorial fingering agreement ≥80% and verified real-score placement ≥90% for an explicitly defined level-5-or-below corpus. Prefer existing private fingered PDFs; keep scores and reference answers outside the package. See benchmark-sources.md.

## Freeze before testing

Assign benchmark_role=development|holdout when freezing each piece. Use development data for diagnosis; run untouched holdouts only at acceptance. Once holdout answers inform a repair, demote that piece to development and reserve new untouched evidence. Formal manifests must set min_holdout_fingering_* and min_holdout_visual_*.

A fingered PDF needs no matching MusicXML: clearly visible editorial digits attached to real heads form partial-label reference anchors. MXL is optional candidate semantics and cannot replace independently transcribed answers.

```bash
python3 scripts/create_private_benchmark_manifest.py \
  --input piece-a=/path/to/fingered-score.pdf \
  --input piece-b=/path/to/another-fingered-score.pdf \
  -o private-benchmark-manifest.json
```

Entries begin diagnostic. Source existence does not mean a measured pass. Installed pdfinfo can record source.page_count; otherwise mark needs-manual-confirmation without installing anything. Unconfirmed page count cannot support whole-score visual acceptance.

Eligible visual entries need source.path/sha256/bytes/page_count, whole_piece_pages, whole_piece_measure_scope including both hands, and four audit files. The evaluator verifies source fingerprints, all pages, and plan scope. Partial pages/measures remain diagnostic. See benchmark-suite.example.json.

Combine nonoverlapping measure comparisons in fingering_comparisons for one piece. Do not disguise fragments as independent pieces or count overlapping anchors twice.

## Separate metrics

1. **Editorial agreement:** exact match only where the source already supplies readable fingers; alternatives may still be playable.
2. **Rule compliance:** simultaneous uniqueness, chord order, tied fingers, repeated-pitch consistency, and other invariants. This is not editorial agreement.
3. **Verified whole-score placement:** independent visual review, real per-note heads, source-anchor, ownership, clearance, and final PNG checks across complete scores.

**Candidate geometry** additionally measures preview coverage, source ink, ownership, clearance, and final label recovery. Use actual pass counts and the minimum of the four audit numerators. Preserve candidate-only/semantics-review-required scope. evaluate_candidate_geometry_suite.py needs at least three pieces; acceptance also requires benchmark_role plus --minimum-holdout-pieces and --minimum-holdout-labels. It cannot establish correct score semantics.

A broad target claim needs adequate external references and verified whole-score evidence. Foundational tests and one editor's labels cannot substitute.

## Visual fixtures

- **Bach/Petzold, Minuet in G BWV Anh.114:** clean grand staff, melody/chords/repeats; test measure segmentation, edges, hand crops, and anchors.
- **Bach, Musette BWV Anh.126:** repeated clef/key prefixes at systems; prevent prefixes from becoming first-beat events and shifting all later heads.
- **Tchaikovsky, Old French Song Op.39 No.16:** held voices, chords, dynamics, and crowded text; positive/negative anchor/clearance checks are engineering tests, not a whole-score accuracy claim.

Always derive systems/measure boxes from the current render, never another edition. Source links are in benchmark-sources.md. MIDI can provide semantic comparison only, never replace visual facts.

```bash
python3 scripts/extract_score_regions.py source-page.png --out-dir crops/page-1 --page 1 --first-measure 1
python3 scripts/create_visual_facts_template.py crops/page-1/proposed-regions.json \
  --source source.pdf --source-type pdf --render-dpi 144 -o visual-facts.json
# Fill and independently verify raw-page facts:
python3 scripts/create_plan_from_visual_facts.py visual-facts.json -o draft-plan.json
```

## Structured editorial tests

Read fingered MusicXML into a reference plan, generate with --ignore-existing, and compare stable note identities:

```bash
python3 scripts/create_plan_from_musicxml.py piece.mxl -o reference.json
python3 scripts/generate_fingering_plan.py reference.json -o generated.json --ignore-existing
python3 scripts/compare_reference_fingerings.py reference.json generated.json -o comparison.json
```

Use run_editorial_mxl_benchmark.py for multiple declared sources. Retain failed samples and each denominator. Ambiguous parts need explicit routing. Duplicate simultaneous voices on one key may merge; contradictory explicit fingers must be rejected.

Historical public Canon/Greensleeves/Fur Elise tests were not certified under this corpus's difficulty definition. Their low agreement remains diagnostic evidence and must not be hidden by easier pieces. Rerun after changes before quoting new figures.

## Whole-score visual acceptance

```bash
python3 scripts/validate_recognition.py locked-plan.json
python3 scripts/generate_fingering_plan.py locked-plan.json -o fingered-plan.json
python3 scripts/validate_fingering_plan.py fingered-plan.json --require-verified-anchors
python3 scripts/audit_annotation_layout.py fingered-plan.json --minimum 0.90 -o layout.json
python3 scripts/audit_source_noteheads.py fingered-plan.json --minimum 0.90 -o anchors.json
python3 scripts/audit_source_clearance.py fingered-plan.json --dpi 144 --minimum 0.90 -o clearance.json
python3 scripts/render_fingering_pdf.py fingered-plan.json -o fingered.pdf
# Render each output page, then audit each one:
python3 scripts/audit_rendered_labels.py fingered-plan.json rendered-1.png --page 1 --minimum 0.90 -o rendered.json
```

Review failed scopes locally. Preserve all four JSON reports and failures. Never replace actual counts with 100% simply because thresholds pass, and never remove a whole piece after a few failures.

Rule changes require frozen real-score net gain, untouched holdout acceptance, and no foundational group below threshold. Revert fixes that merely move failures between pieces.

```bash
python3 scripts/run_level5_regression.py --out-dir regression-output --minimum 0.80
python3 scripts/audit_annotation_layout.py regression-output/placement-regression-plan.json --minimum 0.90
python3 scripts/audit_source_clearance.py regression-output/placement-regression-plan.json --dpi 144 --minimum 0.90
```

Runtime JSON is the authoritative current result. Separate deterministic script time from model transcription/review time.
