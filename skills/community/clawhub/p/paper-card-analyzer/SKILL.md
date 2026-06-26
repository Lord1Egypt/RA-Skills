---
name: paper-card-analyzer
description: Analyze `paper-parse` outputs and generate a research-oriented paper card directly in natural language. Use this skill after paper parsing when you need a structured summary of contributions, method, experiments, limitations, reproducibility notes, and future work without running any extra script.
metadata:
  {
    "openclaw":
      {
        "emoji": "🧪",
      },
  }
---

# Paper Card Analyzer

Generate a research-oriented `paper-card` from `paper-parse` results using direct natural-language analysis.

## Input Expectations

Read artifacts produced by `paper-parse`:

- `*_content.md` (full parsed paper content in markdown)
- `*_parsed.json` (metadata and figures)

## Output

Produce the paper card in English by default, with balanced depth, and always save outputs in the same folder as the selected `*_content.md` and `*_parsed.json`.

Always save:

- `paper-card.md`
- `paper-card.json`
- `paper-card-feedback.md` (feedback log and revision history)

The generated card uses this fixed section order:

1. Paper Snapshot
2. Research Problem and Motivation
3. Core Contributions
4. Method Overview
5. Experimental Setup
6. Main Results and Evidence
7. Ablation and Analysis Findings
8. Limitations and Threats to Validity
9. Reproducibility Notes
10. Open Questions and Future Work

## Workflow

1. Identify the target pair of files:
   - Preferred: one `*_content.md` and one `*_parsed.json` in the same folder.
   - If multiple candidates exist, ask user to pick one pair.
2. Read parsed metadata from `*_parsed.json`:
   - `title`, `paper_name`, `num_pages`, `figures`.
3. Read `*_content.md` and extract evidence by section:
   - abstract/introduction/method/experiments/results/ablation/limitations/conclusion.
4. Write a research-oriented card:
   - Prioritize scientific novelty, methodological logic, evidence strength, validity threats, and reproducibility.
5. Save first draft to the same folder:
   - `paper-card.md` and `paper-card.json`.
6. Request human feedback and revise:
   - Ask what to correct, expand, or make stricter.
   - Update card and save again (overwrite current files).
   - Append each round to `paper-card-feedback.md` with: round number, user request, key edits.
7. Repeat revision rounds until the user explicitly confirms satisfaction.
8. Keep uncertainty explicit:
   - If a section is missing, say "Not clearly stated in parsed content."

## Reliability Protocol

For every claim in the paper card:

- Use only evidence from `*_content.md` or `*_parsed.json`.
- If evidence is weak or absent, mark it as "Not clearly stated in parsed content."
- Separate "author-reported result" from "analyst assessment."
- Never infer exact numbers, datasets, or baselines without direct textual support.
- Prefer conservative wording over speculative interpretation.

Before finalizing each round, run a self-check:

1. No unsupported factual claims.
2. All metric numbers appear in source content or are removed.
3. Limitations include at least one explicit validity threat.
4. Reproducibility notes include what is known and unknown.
5. JSON keys and Markdown section order are complete and stable.

## Section Requirements (Detailed)

1. Paper Snapshot
   - Include title, paper_name, venue/year (if detectable), pages, figure count.
   - If venue/year is uncertain, mark as unknown.
2. Research Problem and Motivation
   - State task, real gap in prior work, and why gap matters.
   - Include scope boundaries if described by the authors.
3. Core Contributions
   - List 2-5 explicit novelty points.
   - Each contribution must be independently understandable and non-redundant.
4. Method Overview
   - Explain major components, data/model flow, and design rationale.
   - Avoid implementation-level noise unless necessary for understanding.
5. Experimental Setup
   - Capture datasets, baselines, metrics, and protocol details present in text.
   - Flag missing setup details that hurt comparability.
6. Main Results and Evidence
   - Report strongest outcomes with metrics when available.
   - Distinguish aggregate gains from per-dataset or per-metric gains.
7. Ablation and Analysis Findings
   - Summarize what ablation or analysis proves about component necessity.
   - If absent, explicitly say no dedicated ablation evidence was found.
8. Limitations and Threats to Validity
   - Cover at least: data/benchmark bias risk, method assumptions, external validity risk.
   - Include whether limitation is author-stated or analyst-inferred.
9. Reproducibility Notes
   - Record code/data links, hyperparameter clues, missing artifacts, reproducibility blockers.
   - State expected effort/risk level for independent reproduction.
10. Open Questions and Future Work
   - Provide 2-4 concrete research questions tied to observed evidence gaps.
   - Keep questions falsifiable and experiment-oriented.

## Style Rules

- Use concise, factual scientific writing.
- Do not invent metrics, datasets, or claims not supported by the parsed text.
- Distinguish author claims from your assessment.
- Keep section order fixed for consistency across papers.
- Keep language precise, avoid hype words, and avoid absolute certainty unless directly supported.

## JSON Shape

Use these top-level keys:

- `paper_snapshot`
- `research_problem_and_motivation`
- `core_contributions`
- `method_overview`
- `experimental_setup`
- `main_results_and_evidence`
- `ablation_and_analysis_findings`
- `limitations_and_threats_to_validity`
- `reproducibility_notes`
- `open_questions_and_future_work`
- `figures`

Store `paper-card.json` on every round, not only on request.
