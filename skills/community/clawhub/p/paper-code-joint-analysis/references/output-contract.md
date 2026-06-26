# Paper-Code Joint Analysis Output Contract

Use this contract to create or audit artifacts. User-facing analysis output is Chinese by default; keep paper titles, code identifiers, file paths, commands, class names, method names, and standard acronyms in their original form. The deep-reading report is paper-only; companion artifacts perform the paper-code mapping.

## 0. Stable Reader Data Contract

The static reader is reusable page code. A new paper must not require custom JavaScript or custom HTML. The page loads a fixed artifact set:

- `analysis_bundle.json`
- `paper_reading_report.md`
- `paper_questions_for_code.md`
- `paper_code_crosswalk.md`
- `experiment_joint_reading.md`
- `implementation_omissions.md`
- `diagrams.md`
- `modify_method_guide.md`
- `validation_report.md`

Rules:

- Keep these exact filenames.
- Keep `analysis_bundle.json` on `schema_version = paper-code-joint-analysis.v1` unless doing an intentional schema migration.
- Put structured facts in `analysis_bundle.json`: paper questions, mechanisms, formulas, code indices, experiments, omissions, diagrams, modification guide, validation checks.
- Put long narrative explanation in the fixed Markdown files.
- Do not rewrite `site/index.html`, `site/assets/app.js`, or `site/assets/styles.css` for one paper. If display logic needs improvement, update `assets/reader-template/` in the skill and rebuild.
- If a Markdown artifact is modest in size and can be read from disk by Codex, keep it as one fixed file. If it cannot be safely created in one step, create section parts under `_parts/<artifact_name>/` and merge them into the fixed final filename with `scripts/merge_markdown_parts.py`.

## 1. Machine-Readable Bundle

The canonical output is `analysis_bundle.json`. Required top-level keys:

- `schema_version`: exactly `paper-code-joint-analysis.v1`.
- `intake`: paper/repository identity, scope, execution stance, and dependency stance.
- `paper_questions`: PDF ambiguities, underspecified formulas/model steps, missing experiment details, apparent inconsistencies, and code-based answers.
- `domain_critical_execution`: the field-specific execution substrate that makes the method work.
- `mechanisms`: paper mechanisms with formulas, paper evidence, code indices, snippets, relationships, and differences.
- `experiments`: every paper table/figure/ablation/supplement experiment with command status.
- `implementation_omissions`: paper omissions revealed by code.
- `diagrams`: diagrams with type, source, legend, and source-file references.
- `modify_guide`: method-level, architecture-level, and experiment-level edit points.
- `validation`: checks, reruns, unresolved risks, and source files reopened.

Validate it with:

```bash
python scripts/validate_bundle.py analysis_bundle.json
```

The JSON shape is specified in `analysis-bundle.schema.json`. The validator uses only Python standard library checks.

## 2. Complete Paper Reading Report

`paper_reading_report.md` must be a complete Gate-1-level deep-reading report, not a summary, dashboard copy, or collection of cards.

Use the local module `modules/deep-reading-gate1.md` and the overlay in `deep-reading-overlay.md`. This means the report should be as detailed as a Gate-1-level text deep-reading report and teaching-quality, but it must stay paper-only. It must not contain repository paths, source-code line numbers, class/method mappings, or code-disclosed facts, and it must not call `paper-toon-deep-reader` or trigger cartoon image generation or PDF assembly.

Required subsections:

- Problem and assumptions.
- Title interpretation and related-work gap.
- Symbols and client/data/model entities.
- Method components.
- Equations in renderable math form.
- Algorithm steps and control flow.
- Figure/table/chart interpretation.
- Design-choice critique and limitation analysis.
- Domain-critical execution substrate: the concrete loop, protocol, pipeline, scheduler, sampler, retriever, planner, simulator, message-passing system, optimizer, or exchange mechanism that makes the method work.
- Experiments, baselines, ablations, supplementary studies.
- Ambiguities visible from the paper alone.
- Reviewer/defense lens: novelty, significance, technical soundness, methodological rigor, reproducibility, result-to-claim alignment, missing baselines/controls, and limitation honesty.
- Short teaching summary or story without equations.

Completeness requirements:

- For a normal computer-science paper, target at least 12,000 characters. If the source is unusually short or incomplete, document why in `validation_report.md`.
- Include enough narrative for the reader to understand the paper without looking at the code.
- Include a learning-oriented narrative: what a reader should understand, what remains confusing from the PDF alone, and which questions are handed to `paper_questions_for_code.md`.
- For central concepts and formulas, use the pattern: intuition -> formula or algorithm step -> concrete example -> limitation -> paper-only open question.
- Interpret important figures and tables in terms of what claim they support and what they leave unclear.
- Formula sections must contain actual renderable math expressions, not prose-only descriptions.
- Raw LaTeX source is allowed inside Markdown `math` fences as storage, but must not be visible as normal reader content when KaTeX rendering succeeds.

## 2.5 Paper Questions For Code

`paper_questions_for_code.md` is mandatory. It is the investigation bridge between the paper-only deep-reading report and repository reading.

For each question include:

| ID | PDF ambiguity/question | Why it matters | Paper evidence | Code evidence | Status | Answer |
| --- | --- | --- | --- | --- | --- | --- |

Question categories to check:

- Missing implementation details: defaults, hidden flags, data split mechanics, optimizer/scheduler, sample counts, thresholds, seeds, augmentations, hardware/runtime assumptions.
- Formula or objective ambiguity: undefined symbols, unclear normalization, unclear loss weighting, missing dimensions, missing training/inference distinction.
- Model or algorithm flow ambiguity: where data enters, which module consumes which output, what is exchanged, what is stored, what is reused across rounds.
- Experiment ambiguity: exact commands, dataset ratios, non-IID settings, baselines, ablation switches, result aggregation, standard deviation source.
- Apparent inconsistency: paper text, figure, table, algorithm, and code disagree or require an inference to reconcile.

Use status labels:

- `answered_by_code`
- `partly_answered_by_code`
- `not_answered`
- `contradiction`
- `reasonable_inference`

## 3. Paper-To-Code Crosswalk

For each mechanism or algorithm step, include:

| Paper step/formula | Paper evidence | Code index | Key code snippet | Relationship | Difference/risk |
| --- | --- | --- | --- | --- | --- |

Rules:

- Include losses and metrics.
- Include data preparation and preprocessing.
- Include control flow and data flow.
- Include the field-specific execution substrate. Examples: communication/model exchange for distributed learning, retrieval/indexing for RAG, decoding/sampling for generative models, environment-action-reward loops for RL/control, graph message passing, agent planning/tool calls, compiler pass pipelines, simulation loops, or systems protocols.
- Use real source paths, class names, method names, arguments, and line ranges.

## 4. Experiment Joint Reading

For every table, figure, ablation, robustness plot, and supplementary experiment:

| Experiment | Paper intent | Settings | Code path | Command/status | Result extraction | Code-disclosed omissions |
| --- | --- | --- | --- | --- | --- | --- |

Use status labels:

- `direct`: command/script exists.
- `manual-matrix`: supported but needs repeated commands.
- `approximate`: close but not exact.
- `requires-code-edit`: branch exists but public args cannot reach it.
- `unsupported`: no reliable implementation found.

## 5. Implementation Omissions

Include a table with:

| Detail | Paper says | Code does | Impact |
| --- | --- | --- | --- |

Check at least:

- Defaults and forced flags.
- Random seeds and uncontrolled randomness.
- Dataset split mechanics.
- Data augmentation.
- Optimizers and schedulers.
- Loss functions.
- Warm-up and sampling schedules.
- Generated sample counts.
- Domain-critical combination/exchange path, such as aggregation, retrieval, decoding, scheduling, planning, simulation, message passing, protocol exchange, or tool orchestration.
- Logging/statistics and standard deviation source.
- Hardware and dependency mismatch.

## 6. Diagrams

Required diagrams when relevant:

- Use-case diagram mapping all paper experiments.
- Class diagram with real source class names.
- Sequence diagram for training/control flow.
- Sequence, state, or data-flow diagram for the field-specific execution substrate when it is central to the paper.

Each diagram must have a short Chinese legend:

- Objects/classes.
- Messages and method names.
- Source files.
- Paper section or experiment connection.

## 7. Modify-Method Guide

Follow `modules/modify-method-guide.md`.

The guide is for a reader who wants to propose a new model or algorithm based on the paper's framework. It should identify the compact method-level edit surface, not produce a parameter-tuning checklist.

Focus on:

- core files/classes/functions where the paper's proposed method is implemented;
- what input/output contract a new module must preserve;
- where to add or replace algorithm logic, loss, aggregation rule, sampler, controller, or inference step;
- what minimal smoke test confirms the new method still enters the original pipeline.

Avoid:

- ordinary hyperparameter changes;
- exhaustive CLI flag lists;
- full refactor plans;
- treating a backbone swap as the main guide unless the paper's contribution is the backbone itself.

For each modification:

| Goal | Files/methods | Minimal change | Invariants to preserve | Smoke test |
| --- | --- | --- | --- | --- |

## 8. Validation Report

Must say:

- Which artifacts were checked.
- Which source files were re-opened.
- Which claims remain uncertain.
- Whether every paper experiment is represented.
- Whether every formula/loss has a code mapping.
- Whether `paper_questions_for_code.md` exists, every major PDF ambiguity has a code-evidence status, and unresolved questions are carried into `validation_report.md`.
- Whether every diagram uses real names.
- Whether the domain-critical execution substrate was identified and mapped to code.
- Whether dependency handling matched the user's execution stance: no install for static analysis; explicit environment/version record for reproduction.
- Whether `paper_reading_report.md` is complete enough, paper-only, and not a short summary or code mapping.
- Whether `modify_method_guide.md` focuses on method-level extension points for a new model or algorithm, not ordinary parameter tuning.
- Whether the generated reader uses the reusable template and fixed artifact filenames.
- Whether any chunked artifacts were merged into final fixed filenames before building the reader.
- Whether formulas render as typeset math and raw LaTeX is hidden in normal page display.
- Whether visible Chinese output and reusable reader templates are valid UTF-8 and contain no mojibake or replacement characters.
- Failed checks, fixes made, and final rerun status. If a check still fails, mark it as unresolved and explain why.

## 9. Static Reader

A full analysis must include a static web reader unless the user explicitly opts out.

Required files:

- `site/index.html`
- `site/assets/app.js`
- `site/assets/styles.css`
- `site/vendor/katex/katex.min.js`
- `site/vendor/katex/katex.min.css`
- `site/vendor/mermaid.min.js`

Build it with:

```bash
python scripts/build_static_reader.py <analysis_dir> --force
```

For final visual delivery when network access is available, build with local KaTeX WOFF2 fonts installed into the generated site:

```bash
python scripts/build_static_reader.py <analysis_dir> --force --install-katex-fonts
```

The ClawHub skill package itself must not include KaTeX `.ttf`, `.woff`, or `.woff2` files. Generated reader outputs may contain `site/vendor/katex/fonts/*.woff2` when the font install flag is used.

The reader must:

- Load `analysis_bundle.json`.
- Show the full `paper_reading_report.md`, not only a summary.
- Show `paper_questions_for_code.md` and `analysis_bundle.json.paper_questions` as a separate reader section.
- Show formulas from `analysis_bundle.json` and fenced Markdown blocks such as `math` fences with KaTeX as typeset formulas.
- Hide raw formula source when rendering succeeds; show fallback only on rendering failure.
- Render Mermaid diagrams from `diagrams.md` when Mermaid is available and show source fallback otherwise.
- Show experiment mappings, implementation omissions, modify-method guide, and validation status.
- Use Chinese visible UI labels by default.
- Be openable through a local HTTP server. `file://` may fail because browsers often block JSON/Markdown fetches.
- Pass `scripts/check_reader.py <analysis_dir>` without mojibake, missing asset, comparison-page, formula-renderer, or diagram-renderer failures.
