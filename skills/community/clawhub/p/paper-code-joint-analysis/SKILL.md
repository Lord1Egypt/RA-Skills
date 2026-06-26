---
name: paper-code-joint-analysis
description: Jointly analyze a research paper and its open-source implementation. Use when a user wants to understand a paper through code, map theory/formulas/algorithms/experiments to real classes and methods, identify implementation details not disclosed in the paper, produce reproducibility commands and gaps, build explanatory diagrams or a static reader, or validate that an analysis covers both the paper and repository.
---

# Paper-Code Joint Analysis

## Purpose

Use this skill to make the code an evidence layer for reading the paper. The output must help a reader answer: what the paper claims, where the code implements it, how each experiment is run, what the paper omits, and what to edit to change the proposed method.

Default user-facing language is Chinese. Keep paper titles, code identifiers, file paths, command names, class names, method names, and standard acronyms in their original form, but write reports, reader labels, explanations, validation notes, diagram legends, and omission analysis in Chinese unless the user explicitly requests another language.

The static reader is reusable code. Do not rewrite page logic for a new paper. New analyses must feed the same reader template through the stable artifact contract: `analysis_bundle.json` plus fixed-name Markdown files. If a new paper needs extra content, add it to the bundle fields or the fixed companion Markdown files rather than creating paper-specific JavaScript or HTML.

Every complete run must produce both human-readable Markdown artifacts and the fixed machine-readable bundle. The Markdown files are the learning record a person reads; `analysis_bundle.json` is the compact structured data that the reader template loads. Do not replace the Markdown reports with a webpage, and do not put long narrative analysis only in JSON.

For long outputs, do not try to bypass hard model/API limits. Prefer single files passed by path when they fit the active model/API budget; do not embed large content in shell commands. Use the chunk workflow in `references/large-artifact-policy.md` only when a file is too large to construct safely in one step or when OS/tool limits such as Windows command-line length are the blocker.

## Module Architecture

This skill is self-contained and module-driven. Do not invoke `paper-toon-deep-reader` at runtime. Its Gate-1 text-report quality bar has been internalized as a local module, so execution depends only on this skill's own `SKILL.md`, `modules/`, `references/`, `scripts/`, and `assets/`.

Use modules by concern:

- `modules/deep-reading-gate1.md`: complete learning report depth for `paper_reading_report.md`.
- `modules/question-led-code-reading.md`: PDF ambiguity ledger and code-evidence status for `paper_questions_for_code.md` and `analysis_bundle.json.paper_questions`.
- `modules/modify-method-guide.md`: method-level extension points for proposing a new model or algorithm based on the paper.
- `modules/fixed-artifacts-and-reader.md`: fixed output files, reusable reader, formula rendering, and validation commands.

Upgrade modules independently. If a future workflow changes only the reading standard, replace `modules/deep-reading-gate1.md`. If it changes output data shape, update `references/analysis-bundle.schema.json`, validators, reader template, and the schema version deliberately.

## Mandatory Workflow

1. **Intake and scope**
   - Verify paper identity, PDF/source availability, repository commit, README, entry scripts, and analysis goal.
   - State the analysis scope and ignore code unrelated to the paper's method or experiments.
   - If training is not requested, do static analysis only and say so.

2. **Paper pass**
   - Apply the local module `modules/deep-reading-gate1.md` plus `references/deep-reading-overlay.md`. The depth of `paper_reading_report.md` should align with a Gate-1-level text report, while excluding cartoon/storyboard/PDF stages.
   - Keep `paper_reading_report.md` paper-only: do not include repository paths, code line references, class/method mappings, or code-disclosed facts in this report. It is the standalone learning-oriented paper deep read.
   - Extract method components, symbols, equations, algorithms, experimental sections, tables, figures, baselines, ablations, and supplementary settings.
   - Before using the code as evidence, follow `modules/question-led-code-reading.md` and write a question ledger from the deep-reading report and PDF: what the paper does not say clearly, where formulas/objectives/model flow are underspecified, where statements appear inconsistent, and which experiment settings are missing. Store the human-readable version in `paper_questions_for_code.md` and the structured version in `analysis_bundle.json.paper_questions`.
   - Preserve equations as renderable math in final outputs, not prose-only paraphrases.
   - When a user asks for "human-readable", "human-written", or Word-like formulas, produce typeset/renderable formulas, not prose descriptions. Put intuition in a separate explanation paragraph.
   - Do not expose raw LaTeX as the normal page content. Markdown may store formulas in fenced `math` blocks, but the static reader must render them as typeset formulas and hide the source unless rendering fails.

3. **Repository pass**
   - Map entry points, configs, datasets, models, training/inference loops, domain-critical execution paths, losses, metrics, and logging.
   - Use real class, function, method, argument, and file names. Do not invent wrappers or parameter names.
   - Record line ranges for every important claim.
   - Use the question ledger to drive repository reading. For each question, mark whether code answers it, partly answers it, contradicts the paper, or still leaves it unresolved.

4. **Theory-to-code crosswalk**
   - For each paper mechanism, produce: paper formula/step, code entry, key code excerpt, implementation relationship, and paper-code difference.
   - Include losses, metrics, data flow, control flow, and the domain-critical execution substrate.
   - Choose that substrate from the paper's actual field: examples include communication/model exchange for FL or distributed systems, retrieval and indexing for RAG, decoding/sampling for generative models, environment-action-reward loops for RL/control, message passing for graph methods, planning/tool-use loops for agents, compiler passes for compiler papers, and scheduler/protocol paths for systems papers.

5. **Experiment-by-experiment joint reading**
   - For every table/figure/ablation/supplement experiment, produce: paper intent, exact setting, code path, runnable or near-runnable command, result extraction method, and undisclosed implementation details.
   - Distinguish "directly supported by command" from "requires code edit or wrapper".

6. **Unreported implementation details**
   - Compile paper omissions revealed by code: defaults, hidden forced flags, random seeds, data splits, augmentations, optimizer details, warm-up schedules, sample counts, aggregation formulas, logging/statistics, unsupported ablations, and hardware/version mismatches.

7. **Diagrams and change guide**
   - Produce UML/use-case/class/sequence diagrams only after code names are verified.
   - Sequence diagrams must include real method/class names and annotated messages.
   - Follow `modules/modify-method-guide.md` for the "modify the proposed method" guide. Focus on where to implement a new model or algorithm based on the paper framework, not on ordinary parameter tuning.

8. **Validation and iteration**
   - Validate outputs against `references/output-contract.md`.
   - Validate the reusable reader data contract in `references/reader-data-contract.md`.
   - For reports built from chunks, verify the merged final Markdown exists and run `scripts/check_outputs.py <analysis_dir>`.
   - Run `scripts/check_outputs.py` on generated Markdown/JSON artifacts when available.
   - Re-open source files for any weak claim.
   - If validation fails, correct the artifacts or the skill, rerun validation, and repeat until checks pass or the remaining failure is explicitly documented as unresolvable with current artifacts.
   - Check generated reports and reader templates for mojibake or encoding damage. Visible Chinese UI and report text must be valid UTF-8, not garbled Chinese or replacement characters.

9. **Static reader**
   - For every full analysis deliverable, build a static web reader unless the user explicitly opts out.
   - Follow `modules/fixed-artifacts-and-reader.md`.
   - Use `scripts/build_static_reader.py <analysis_dir> --force` instead of hand-writing a new page. For final visual delivery when network access is available, use `scripts/build_static_reader.py <analysis_dir> --force --install-katex-fonts` so the generated `site/` includes local KaTeX WOFF2 fonts.
   - Do not customize `site/index.html`, `site/assets/app.js`, or `site/assets/styles.css` for the specific paper unless the reusable template itself is being improved for all future papers.
   - The reader must expose the complete `paper_reading_report.md`, `paper_questions_for_code.md`, formulas, theory-to-code mappings, experiment mappings, omissions, diagrams, modify guide, and validation status.
   - The reader's visible UI and analysis text must be Chinese by default. Raw LaTeX source must not be visible when KaTeX rendering succeeds.
   - Reader templates and generated sites must not contain mojibake markers. If `scripts/check_reader.py` or `scripts/check_outputs.py` reports encoding damage, fix the source artifact or template and rebuild before finalizing.
   - Provide the reader path or local HTTP URL in the final response.

## Dependency And Environment Policy

- The skill's bundled Python scripts must run with the Python standard library only; do not require users to install package dependencies just to validate bundles or build the static reader.
- ClawHub skill packages must remain text-only. Do not bundle KaTeX `.ttf`, `.woff`, or `.woff2` font binaries in `assets/reader-template/`. When full local KaTeX typography is needed, install fonts into the generated output with `scripts/build_static_reader.py <analysis_dir> --force --install-katex-fonts`. This downloads WOFF2 files into `site/vendor/katex/fonts/`, outside the uploaded skill package.
- The static reader template bundles local KaTeX and Mermaid JavaScript/CSS assets, but not KaTeX font binaries. If those assets or fonts are missing or damaged, the reader must still work with formula and diagram fallbacks instead of failing blank, but final deliverables should be checked in a browser to confirm formulas render as typeset math rather than visible LaTeX source.
- Do not install dependencies for the target paper repository unless the user explicitly asks to run experiments or reproduce results.
- When reproduction is requested, derive dependency installation steps from the target repository README, lock files, environment files, or official paper instructions, and record exact versions, hardware assumptions, and any deviations.
- When only static analysis is requested, report the target repository's dependencies and likely blockers, but do not mutate the environment.

## Output Contract

Read `references/output-contract.md` when creating final artifacts or auditing an existing analysis. Use its section names unless the user asks for another format.

Canonical machine-readable artifact:

- `analysis_bundle.json`: must follow `references/analysis-bundle.schema.json` and validate with `scripts/validate_bundle.py`.

Human-readable companion artifacts:

- `paper_reading_report.md`
- `paper_questions_for_code.md`
- `paper_code_crosswalk.md`
- `experiment_joint_reading.md`
- `implementation_omissions.md`
- `diagrams.md` or equivalent Mermaid/SVG assets
- `modify_method_guide.md`
- `validation_report.md`
- `site/index.html`: generated by `scripts/build_static_reader.py`; this is a view over the bundle and Markdown artifacts.

The web page is mandatory for complete analysis outputs unless the user explicitly asks not to create it. The page should be a view over `analysis_bundle.json` and the Markdown artifacts, not a replacement for them.

Stable reader data contract:

- Keep the exact filenames listed above. The reader loads these filenames directly and must not need paper-specific fetch paths.
- Keep `analysis_bundle.json` on schema version `paper-code-joint-analysis.v1` until a deliberate schema migration is made.
- Put short structured facts, formulas, paper questions, code indices, experiments, diagrams, omissions, modification points, and validation checks in `analysis_bundle.json`.
- Put long narrative explanation in the fixed Markdown files. `paper_reading_report.md` must be a complete paper-only learning report, not a short summary, dashboard copy, or code mapping. `paper_questions_for_code.md` must list the concrete questions raised by that deep read and how code evidence answers or fails to answer them.
- If a Markdown file is modest in size, write the fixed file directly. If it is too large to construct safely in one step, use `_parts/<artifact_name>/` plus `scripts/merge_markdown_parts.py`; the final output filename must still be the fixed filename consumed by the reader.
- If the reader lacks a display affordance for a generally useful new field, update the reusable template and contract, then rebuild all affected readers.

Internalized Gate-1 reading standard:

- Use the local module `modules/deep-reading-gate1.md` for rigorous text-report style: knowledge-dependency order, intuition -> formula/algorithm -> concrete example -> limitation, module input/output, figure/table interpretation, experiment-purpose analysis, reproducibility gaps, reviewer/defense lens, and teaching summary.
- Do not call `paper-toon-deep-reader`, and do not import cartoon-image, storyboard, or PDF assembly gates into this skill. If the user explicitly asks for a separate visual-storyboard workflow, treat that as a different skill workflow.

## Quality Bar

- Prefer fewer, verified claims over broad but ungrounded coverage.
- Treat "paper says X" and "code does Y" as separate evidence. Keep code evidence out of `paper_reading_report.md`; use `paper_questions_for_code.md`, crosswalk, experiment reading, omissions, and diagrams for code evidence.
- Mark unsupported or approximate reproductions explicitly.
- Never hide a missing command, missing ablation switch, or code override behind a polished diagram.
- If a user is trying to understand the method, avoid dashboard decoration and prioritize readable formulas, code snippets, experiment mapping, and sequence flow.
- Do not label prose columns or sections as "human-readable formulas"; formula sections must contain actual renderable math expressions with code evidence nearby.
- Before finalizing a generated reader, verify in a browser or DOM check that KaTeX nodes exist and raw formula source such as `\frac`, `\lambda`, or `\mathcal` is not visible in normal rendered formula blocks.
- Before packaging or shipping the skill, scan `assets/reader-template/`, scripts, README, and generated reader files for mojibake. Do not treat console encoding artifacts as success; read files as UTF-8 and inspect actual file bytes/text. Also scan the uploaded skill folder for `.ttf`, `.woff`, and `.woff2`; KaTeX fonts belong only in generated reader outputs, not in the ClawHub skill package.
- Treat `paper_reading_report.md` as the full Gate-1-level paper-only learning report. It should usually be at least 12,000 Chinese/English characters for a normal research paper and must cover problem, assumptions, symbols, formulas, method components, algorithm/control flow, figures/tables, experiment design, paper-only ambiguities, reproducibility gaps visible from the paper, reviewer/defense lens, and teaching summary. If the paper is genuinely too short for that threshold, say why in `validation_report.md`.
- Treat `paper_questions_for_code.md` as mandatory investigation scaffolding, not optional commentary. It must start from questions raised by the deep-reading report, including missing implementation details, ambiguous formulas/objectives, model/data-flow uncertainty, experiment settings, and apparent paper inconsistencies, then resolve or flag those questions with code evidence.
- Treat `modify_method_guide.md` as a research-extension guide. It should say which core files/classes/functions define the method boundary for adding a new model or algorithm; it should not be a parameter-tuning guide.
