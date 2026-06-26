---
name: paper-deep-reading
description: Deep-read research papers into source-aware reports, traceable claim evidence, and research-direction seeds. Use for paper PDFs, LaTeX sources, appendices, code notes, peer reviews, literature-review tasks, novelty audits, and finding new research questions with minimum viable experiments.
license: MIT-0
metadata:
  version: 1.2.0
  openclaw:
    emoji: "📚"
    requires:
      bins:
        - python3
    tags:
      - research
      - papers
      - deep-reading
      - ideation
      - literature-review
---

# Paper Deep Reading: Source-Aware + Research-Generative Direction Mining

Use this skill when the user wants a **deep, paper-grounded, auditable, idea-generative reading report** for one computer-science paper or a small paper batch.

The input may be:

- a user-provided PDF
- a user-provided LaTeX source tree or `.tex` files
- supplementary material, appendix files, code notes, or OpenReview material
- only the paper title, arXiv id, venue page, citation-like paper name, or PDF link

The default output is **text-first, audit-first, formula-preserving, and research-direction-oriented**.
This version does not require a dedicated webpage reader; when search/browsing tools are available, use them to assemble the best source package before writing.

## 1) Core deliverables

1. **Human-readable report**
   - `report.md`

2. **Machine-readable trace artifacts**
   - `traceability_manifest.json`
   - `latex_paragraphs.json`
   - `artifact_index.json`

3. **Machine-readable research artifacts**
   - `research_lens.json`
   - `direction_board.json`

The report is the primary user-facing deliverable.
It must read like a serious research mentor's deep-reading memo, not like a thin checklist dump.
The direction board is the primary idea-mining surface: it converts paper weaknesses, hidden assumptions, evidence gaps, proxy mismatches, successor-paper gaps, and reviewer objections into candidate research directions.

## 2) ClawHub and MIT-0 package discipline

This skill package is intended to stay compatible with **ClawHub / OpenClaw skill packaging**.

Keep the package lean:

- keep `SKILL.md` as the main instruction file
- keep only text-based support files, templates, and scripts that another agent needs to execute the workflow
- do not reintroduce auxiliary docs such as `README.md` or `CHANGELOG.md`
- do not add binary assets, vendored third-party repositories, or cached papers to the skill package
- keep support files focused on execution, validation, and artifact contracts

Keep the package license-safe:

- this package follows ClawHub's `MIT-0` publication model
- keep the local bundle license text in `LICENSE.txt`
- do not add restrictive or conflicting license terms elsewhere in the package
- do not vendor third-party projects or assets into the skill unless their license is compatible with `MIT-0` redistribution expectations
- when external tooling is useful, document it or install it outside the skill instead of copying its source tree into the package

Runtime discipline:

- bundled scripts are local text-processing helpers and should not make network calls
- if external search is needed, use the host agent's approved browsing/search capability rather than hidden scripts
- declare runtime dependencies honestly in frontmatter and metadata

## 3) Non-weakening rule and depth bar

Do **not** treat the OpenClaw / ClawHub version as a lightweight summary mode.
The single-file constraint changes **presentation**, not **analysis quality**.

Never remove, weaken, shorten, or bypass any existing deep-reading requirement, including:

- source acquisition and disambiguation
- LaTeX-first reading when source is available
- PDF-assisted figure/table reading
- formula preservation
- proof-to-practice mapping
- OpenReview / reviewer context when relevant
- reviewer-lens audit
- claim IDs and traceability manifest
- final claim-to-evidence appendix
- research-generative overlay
- language policy
- validation scripts

The report depth bar should stay close to a strong top-conference paper memo:

- cover the full 25-section reading scope
- preserve central equations instead of flattening them into prose
- explain why modules exist, not only what they are called
- reconstruct likely author-side reasoning when the evidence supports it
- connect experiments back to claims, ablations, and alternative explanations
- extract reusable research patterns and future ideas
- produce concrete research seeds with minimum viable experiments, negative-result interpretation, killer objections, and killer results

If a tension appears between a shorter explanation and a more idea-generative one, choose the more useful research-direction analysis while keeping claims grounded.
If a tension appears between speculation about author intent and factual safety, label the reconstruction explicitly as `plausible inference` or `speculation` and anchor it to textual evidence.

## 4) Research-generative overlay

This version keeps the original traceability and formula-preservation bar, but adds a **research-direction mining layer**.

The report must help the user answer not only:

- what the paper did
- whether the evidence supports the claims

but also:

- how the authors may have found the direction
- what hidden assumption `C` broke
- what unavailable mechanism `Y` had to be replaced
- what surrogate mechanism `Z` the paper constructed
- how each module maps to a failure mode
- why key citations matter in the story
- what hidden assumption can seed the next paper
- which new research directions are worth testing first

Use [references/research-generative-methodology.md](references/research-generative-methodology.md) and [references/research-direction-mining-best-practices.md](references/research-direction-mining-best-practices.md) whenever the user wants:

- author-perspective reading
- idea mining
- reverse story construction
- module-level design logic
- citation-function analysis
- reviewer-grade critique
- minimum viable experiment design
- boundary-pushing future directions

## 5) Research-direction mining three-pass method

Read each paper in three direction-mining passes.
These passes are adapted for discovering new research points, not merely for comprehension.

### Pass 1: Five-C triage + direction promise

Quickly inspect title, abstract, introduction, section headings, conclusion, references, and visible figures/tables.
Answer the five triage questions:

1. `Category`: What type of paper is this: method, benchmark, theory, measurement, system, dataset, analysis, survey, or position?
2. `Context`: What field conversation, assumptions, and ancestor methods does it sit inside?
3. `Correctness`: Do the core assumptions, data, metrics, and comparisons look initially plausible?
4. `Contributions`: What are the claimed contributions and how strong do they look before deep verification?
5. `Clarity`: Is the argument organized well enough that the method and claims can be audited?

Then add a **direction-promise note**:

- what hidden assumption seems most likely to be attackable
- what omitted setting or stress condition appears promising
- whether the paper is worth a full second and third pass

### Pass 2: Evidence / method / figure chain reconstruction

Read the paper carefully but keep the goal causal:

`problem -> assumption break -> design principle -> module -> formula -> figure/table -> experiment -> claim`

During this pass:

- inspect key figures, diagrams, graphs, and tables as evidence, not decoration
- preserve central equations and explain their role
- build the challenge-to-module table
- map each result to the claim it supports
- mark missing controls, weak baselines, noisy metrics, unclear error bars, and unsupported narrative jumps
- identify the `available proxy` that replaces an `unavailable ideal mechanism`

### Pass 3: Virtual reimplementation + hidden-assumption attack

Recreate the work as if you had to implement, prove, or reproduce it.
Ask:

- What exact assumptions must be made for each module to work?
- Where would the method fail if one assumption were dropped?
- What tiny example, special case, or counterexample exposes the key idea or fragility?
- What proof step, algorithm step, data preprocessing choice, or metric definition carries the argument?
- What implementation details are missing but necessary for reproduction?
- What would a stronger, cleaner, or more decisive experiment look like?

This pass must produce future-work triggers.
A trigger is not a generic suggestion; it is a statement of the form:

`current method works if H -> under not-H it breaks -> new mechanism needed -> minimum experiment to test the opportunity`

## 6) Successor-paper and reverse-citation reading

When the user asks for new research directions, do not stop at the paper's own related work.
If tools are available and time permits, inspect a small set of successor papers, citation trails, follow-up discussions, code repositories, or public review threads.

Use successor reading to answer:

- how later papers describe this paper's real contribution
- what later work treats as the bottleneck or limitation
- what claims were ignored, weakened, or reframed by the community
- which open gap remains after follow-up papers
- which direction is already saturated and which remains underexplored

If successor-paper search was not possible, say so and keep direction confidence lower.
Do not fabricate citation trends.

## 7) Critical + creative reading rule

Every report must combine critical and creative reading.

Critical reading asks:

- Is the paper solving the right problem?
- Are the assumptions reasonable?
- Are the data, metrics, baselines, and controls sufficient?
- Are the conclusions stronger than the evidence?
- Are there simpler alternatives the authors did not rule out?
- What limitations are admitted, hidden, or structurally unavoidable?

Creative reading asks:

- What good idea can be transplanted elsewhere?
- What stronger setting makes the idea newly important?
- What generalization or simplification would be more elegant?
- What proxy can be replaced by a more direct signal?
- What negative result would change community understanding?
- What is the next research question a strong PhD student should test?

The final directions must be creative **and** falsifiable.

## 8) Reviewer-grade audit integrated with direction mining

Use reviewer thinking not just to judge acceptance, but to discover research seeds.

Audit at least these dimensions when evidence allows:

- novelty and relation to prior work
- significance and likely community use
- technical soundness
- methodology rigor
- statistical validity and uncertainty reporting
- baseline and control completeness
- reproducibility and implementation sufficiency
- result-to-claim alignment
- clarity of figures/tables/formulas
- limitation honesty
- ethics, safety, or societal concerns when relevant
- specific constructive critique

Convert reviewer objections into direction candidates:

`reviewer objection -> why it matters -> what evidence would resolve it -> minimum viable experiment -> possible new paper`

## 9) Full-loop research seed discipline

The skill does **not** replace the researcher or claim to have completed experiments.
It turns a paper into candidate directions that a researcher can test.

Every strong candidate direction must include:

- `seed_type`: one of assumption violation, unavailable mechanism, proxy mismatch, evidence gap, tiny example, successor-paper gap, reviewer objection, negative result, or cross-domain transfer
- `paper_anchor`: claim IDs and source evidence that triggered it
- `research_question`: a question that can be answered
- `hypothesis`: what might be true
- `minimum_viable_experiment`: the smallest decisive test
- `negative_result_interpretation`: what it would mean if the hypothesis fails
- `killer_objection`: the strongest reason the idea might be uninteresting or invalid
- `killer_result`: the result that would make the direction worth pursuing
- `first_week_plan`: practical steps for a researcher's first week
- `risk_level` and `expected_value`

Generic future-work lists are not enough.
A direction without a test plan is an inspiration note, not a research seed.

## 10) Verification surface: body first, appendix last

The report itself remains the primary verification surface, but the detailed evidence placement is:

1. **Main body**
   - readable section-by-section analysis
   - `### Anchored Points` blocks near the relevant discussion
   - concise claim bullets in the form `- [C5.2][evidence-backed interpretation] ...`

2. **Final appendix**
   - detailed claim-by-claim evidence records
   - exact source files
   - section paths
   - line spans
   - page hints when available
   - quote snippets and excerpt windows
   - notes that help a human verify the claim quickly

Do **not** clutter the main narrative by inserting long locator bullets immediately after every claim.
Keep the main body readable, and move detailed original-paragraph explanation to the final `# Appendix: Claim -> Evidence Index`.

Use [scripts/render_inline_trace_report.py](scripts/render_inline_trace_report.py) after drafting the report and manifest to materialize or refresh that appendix.

## 11) Formula-first preservation

When the paper contains key formulas, the report must **not** compress them into prose-only summaries.

For each central equation, objective, theorem statement, update rule, estimator, metric, loss, or constraint, explicitly include:

1. the equation itself in readable math form
2. symbol-by-symbol explanation
3. what optimization / estimation / filtering / proof role it plays
4. why the authors likely wrote it in this form instead of a nearby alternative
5. how it connects to the previous and next module
6. what may be brittle, heuristic, under-justified, statistically weak, or computationally expensive about it
7. how changing the equation creates possible new research directions

Do not weaken equation detail for the sake of shorter presentation.

## 12) Source acquisition policy

Always assemble the **best available evidence package** before writing.

Preferred reading order:

1. **arXiv LaTeX/source package**
2. **user-provided LaTeX**
3. **best available PDF**
4. **supplementary material / appendix**
5. **official code or implementation notes when the user asks for reproducibility**
6. **OpenReview thread / rebuttal / meta-review when relevant**
7. **successor papers or citation trails when the user asks for new research directions**

### 12.1 When LaTeX is available

Treat LaTeX as the primary structural source.

Use PDF only as a visual and pagination aid for:

- figure interpretation
- table reading
- page-local narrative flow
- page anchors
- visual sanity checks that cannot be recovered from source text

### 12.2 When only PDF is available

Do not stop at PDF summarization immediately.

First check whether the same paper has a matching arXiv LaTeX/source package.
If it exists and matches the same paper, switch to **LaTeX-primary + PDF-assisted** reading.

If not, continue with the PDF and say explicitly that the reading is **PDF-primary**.

### 12.3 When only title is available

Search for the paper and collect:

1. arXiv source package if available
2. the best PDF
3. supplementary PDF or appendix if available
4. OpenReview forum if venue is ICLR or otherwise OpenReview-hosted
5. official code, successor papers, or citation context when needed for direction mining

Never silently analyze the wrong paper.
Disambiguate by title, authors, abstract, year, venue, and method keywords.

### 12.4 OpenReview policy

If the paper is an ICLR or OpenReview-hosted paper, look for:

- reviewer comments
- meta-review or area-chair summary
- author rebuttal or response
- revision signals relevant to acceptance

Use them to enrich:

- reviewer-lens audit
- confidence in claimed contributions
- limitations and unresolved doubts
- candidate directions derived from reviewer objections

### 12.5 Missing source policy

If some sources cannot be found, do not abort.
State clearly what was attempted, what was found, what was missing, and how that affects confidence.
Then continue with the best grounded report possible.

If LaTeX cannot be found after an explicit search, say so clearly and use PDF-oriented evidence rows in `traceability_manifest.json` instead of pretending paragraph anchors exist.

## 13) Language policy

Write the **skill instructions, internal prompts, and template skeletons in English**.
Choose the **report language** from the user's current request language by default.

- if the user's current request is primarily in Chinese, write the report in Chinese
- if the user's current request is primarily not Chinese, write the report in English
- if the user explicitly requests another language, follow that explicit instruction
- if the request is mixed-language, follow the dominant user language in the current request

When writing the report in Chinese:

- keep proper nouns and fixed technical identifiers in English
- this includes paper titles, method names, module names, datasets, baselines, theorem or object names, citation names, equation symbols, claim IDs, filenames, and JSON keys
- translate section headings and explanatory prose into Chinese, but do not translate artifact filenames, schema fields, or claim IDs

## 14) Mandatory artifacts

### 14.1 `report.md`

The report must cover, whenever the evidence supports it:

1. paper identification and source package used
2. one-sentence thesis and research equation
3. title interpretation
4. what problem the paper really solves
5. scientific problem ladder
6. how the authors may have found the direction
7. how the authors built the story
8. related work, key citations, and what was still missing
9. main idea
10. symbols, assumptions, and notation
11. key formulas and equation-by-equation explanation
12. theory / proof / practice mapping
13. algorithm or module walkthrough with concrete example
14. method deep reading: the author-thinking behind each module
15. figure explanation
16. experimental design
17. experiments as story evidence and claim alignment audit
18. reviewer-lens audit
19. innovation points and claim-by-claim support audit
20. story-making pattern worth learning
21. weaknesses and limitations
22. innovation type and scientific-boundary judgment
23. future directions and stronger idea paths
24. vivid plain-language story summary
25. exact sources used

Use [templates/report_template.md](templates/report_template.md) as the default skeleton.

For each numbered section:

- start with `### Anchored Points`
- add one or more claim bullets in the exact form `- [C<section>.<index>][label] claim text`
- keep the bullets concise
- follow the bullets with a real explanatory section, not just more bullets
- add tables, formulas, examples, reviewer-style critique, or story reconstruction when they help understanding

### 14.2 `traceability_manifest.json`

This is the claim-to-evidence map.

Rules:

- every claim id in the main report body must appear in the manifest
- one bullet must not hide multiple independent claims under one id
- if a claim depends on multiple paragraphs, equations, tables, appendix passages, figures, or reviews, list them separately
- each claim entry should include `interpretation_type`
- each claim entry should preferably include `research_role`
- each claim entry should include human-friendly locator data when possible

### 14.3 `latex_paragraphs.json`

This is the stable LaTeX anchor index.

Each entry must keep:

- `paragraph_id`
- `source_path`
- `line_start`
- `line_end`
- `section_path`
- `kind`
- `text`

### 14.4 `artifact_index.json`

A compact index for the generated text-first bundle.

It should list the locations of:

- `report.md`
- `traceability_manifest.json`
- `latex_paragraphs.json`
- `research_lens.json`
- `direction_board.json`
- main PDF if any
- supplementary PDF if any
- source package path if known

### 14.5 `research_lens.json`

This is the compact idea-mining artifact.
Use [templates/research_lens.template.json](templates/research_lens.template.json) and [references/artifact_contract.md](references/artifact_contract.md).

It should capture:

- the paper's research equation
- the likely direction-finding path
- challenge-to-module mapping
- per-module hidden assumptions
- citation logic
- reviewer-lens summary
- reusable story pattern
- strongest future idea directions
- links to the most important direction seeds

### 14.6 `direction_board.json`

This is the structured research-direction board.
Use [templates/direction_board.template.json](templates/direction_board.template.json).

It should capture:

- ranked candidate research directions
- the evidence trigger for each direction
- hidden assumption or missing mechanism
- minimum viable experiment
- negative-result interpretation
- killer objection and killer result
- first-week plan
- score breakdown
- relationship to existing paper claims

## 15) Claim discipline

### 15.1 Claim ids

Use stable section-local ids such as:

- `C3.1`
- `C5.2`
- `C14.4`

### 15.2 Claim splitting rule

Do not hide multiple judgments in one claim bullet.

### 15.3 Evidence completeness rule

List all materially relevant evidence for a claim, not just one convenient paragraph.

### 15.4 Interpretation labels

Each claim must declare exactly one of:

- `evidence-backed interpretation`
- `plausible inference`
- `speculation`

### 15.5 Research-generative honesty rule

If the report reconstructs likely author reasoning, it must still point to the exact paragraphs, equations, figures, tables, experiments, reviews, or successor-paper signals that motivate that reconstruction.
Idea generation is required, but fabrication is forbidden.

### 15.6 Direction trigger labels

Each direction seed should also label the trigger as one of:

- `evidence-backed interpretation`
- `plausible inference`
- `speculation`

Do not rank speculative seeds as high-confidence unless the uncertainty is explicit.

## 16) Writing style for verification and idea generation

Prefer a report that is pleasant to read **and** easy to audit.

For every claim, the user should be able to answer:

1. What section-level conclusion is being made?
2. Is it direct evidence, plausible inference, or speculation?
3. Where should I verify it in the appendix?

For the strongest research-direction sections, the report should also answer:

1. What hidden assumption broke?
2. What missing mechanism was replaced?
3. What future paper becomes possible if that assumption fails harder?
4. What minimum experiment would tell us whether this future paper is real?
5. What result would kill the idea?
6. What result would make the idea exciting?

Use phrasing such as:

- "A plausible author-side thinking path is ..."
- "This module is best understood as a surrogate for ..."
- "The citation is not ornamental; it functions as ..."
- "The deepest reusable lesson is ..."
- "This weakness can be converted into a new research direction ..."
- "The minimum viable experiment is ..."
- "The killer objection is ..."
- "A negative result would still be useful if it shows ..."

The report should sound like a research mentor reconstructing how the work may have been invented and how it could become the next project, not like a generic summarizer.

## 17) Grounded workflow

1. Assemble the best source package.
2. If LaTeX is available, extract paragraph anchors with `scripts/extract_latex_paragraphs.py`.
3. Perform Pass 1 five-C triage and decide whether full deep reading is warranted.
4. Perform Pass 2 evidence / method / figure chain reconstruction.
5. Perform Pass 3 virtual reimplementation and hidden-assumption attack.
6. Draft `report.md` using anchored claim IDs in the main body.
7. Keep claim bullets concise and put longer explanation in prose, tables, formulas, examples, and story reconstructions after them.
8. Fill `traceability_manifest.json` so each claim points to one or more paragraph IDs or fallback anchors.
9. Fill `research_lens.json` so the paper's research equation, story structure, module logic, citation functions, reviewer audit, and future directions are captured in structured form.
10. Fill `direction_board.json` so the best candidate research seeds are ranked, testable, and linked to evidence.
11. Fill `artifact_index.json` so the bundle stays portable.
12. Run `scripts/validate_traceability.py`.
13. Run `scripts/validate_direction_board.py` when `direction_board.json` is present.
14. Run `scripts/render_inline_trace_report.py` to append or refresh the final `Claim -> Evidence Index` appendix in `report.md`.
15. Only then finalize the bundle.

## 18) Small-batch policy

For a small paper batch:

- produce one standalone `report.md`-style bundle per paper when the user expects detailed reading
- do not collapse multiple papers into a shallow combined summary
- optionally add a cross-paper direction board if the goal is choosing a new research direction
- rank cross-paper directions by novelty, evidence gap, testability, expected impact, feasibility, and relationship to the user's research interests

## 19) Failure handling

If some sources cannot be found, do not abort.
State clearly:

- what was attempted
- what was found
- what was missing
- how the missing source changes confidence
- which claims or direction seeds are affected

Then continue with the best grounded report possible.

If the evidence does not support strong idea generation, say so and produce a conservative direction board.
Do not invent novelty, successor trends, reviewer objections, or experimental feasibility.
