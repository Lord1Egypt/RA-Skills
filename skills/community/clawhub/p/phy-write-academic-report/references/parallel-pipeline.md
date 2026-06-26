# Parallel Agent Pipeline Reference

This document describes the 3-wave parallel agent architecture used by the `write-report` skill to produce 80+ page academic reports in 2-4 hours instead of 8-12.

---

## 1. Why Parallel Agents?

A thesis has **natural parallelism**. Chapters are mostly independent: the literature review does not depend on the results chapter, and the system design chapter does not depend on the conclusion. Sequential writing ignores this structure and forces a single agent to hold the entire document in context — which degrades quality and takes 8-12 hours for an 80-page report.

The parallel pipeline exploits chapter independence:

| Approach | Time for 80 pages | Agents | Bottleneck |
|----------|:-:|:-:|------------|
| Sequential | 8-12 hours | 1 | Context window exhaustion after ~40 pages |
| Parallel (3-wave) | 2-4 hours | 10-12 total | Data must exist before prose, prose before assembly |

The **3-4x speedup** comes from two sources:

1. **Wall-clock parallelism**: 4 chapter agents writing simultaneously finish in the time of 1.
2. **Better quality per agent**: Each agent handles 15-25 pages with focused context instead of 80+ pages with diluted context.

The constraint is **data dependency**. An agent writing the results chapter cannot produce correct numbers if the data has not been consolidated first. An assembly agent cannot merge chapters that do not yet exist. This constraint shapes the three waves.

---

## 2. Wave Architecture

```
Wave 0 (Data)           Wave 1 (Write)          Wave 2 (Assembly)
~30-60 min              ~60-90 min              ~20-40 min

┌─ 0A: Data ────┐       ┌─ 1: Ch1+2 ────┐      ┌─ 6: Merge ────┐
├─ 0B: Code ────┤       ├─ 2: Ch3 ──────┤      └─ 7: Review ───┘
├─ 0C: System ──┤ ────> ├─ 3: Ch4+5 ────┤ ───>
├─ 0D: History ─┤       └─ 4: Ch6+App ──┘
├─ 0E: Stats ───┤
└─ 0F: Figures ─┘

Gate: all files       Gate: all .tex         Gate: compiles
exist + spot-check    files complete         clean + audit pass
```

**Wave boundaries are hard gates.** Do not start Wave 1 until every Wave 0 output has been verified. Do not start Wave 2 until every Wave 1 agent has finished. Violating these gates produces agents that hallucinate numbers or reference nonexistent figures.

---

## 3. Wave 0: Data Preparation

### Purpose

Produce every artifact that chapter-writing agents will reference. The operating principle is: **agents write poorly without concrete numbers.** When a chapter agent needs a statistic, it should read it from a file — never compute it on the fly and never invent it.

### Agent Specifications

| Agent | Reads | Produces | Format |
|-------|-------|----------|--------|
| **0A: Data Consolidation** | Raw result files (JSON, CSV, logs) | `data/final_results.json` | Single JSON with all experiment numbers |
| **0B: Codebase Analysis** | Source code | `data/codebase_analysis.md` | Module map, LOC counts, key algorithms |
| **0C: System Analysis** | Architecture docs, pipeline code | `data/system_analysis.md` | Component diagram, data flow, tech stack |
| **0D: Experiment History** | Experiment logs, git history | `data/experiment_history.md` | Chronological table of what changed and why |
| **0E: Statistics** | `data/final_results.json` | `data/statistics.md` | Aggregate stats, significance tests, distributions |
| **0F: Figure Generation** | All data artifacts + style config | `figures/*.pdf` + `figures/*.png` | Publication-quality matplotlib figures |

### Agent 0A: Data Consolidation (Example)

This agent reads scattered result files and produces a single source of truth:

```python
# What 0A produces — a clean JSON like:
{
    "conditions": {
        "baseline":  {"success_rate": 0.256, "n": 90, "ci_95": [0.17, 0.35]},
        "summary":   {"success_rate": 0.278, "n": 90, "ci_95": [0.19, 0.37]},
        "url_ms10":  {"success_rate": 0.500, "n": 90, "ci_95": [0.39, 0.61]},
        "tools_ms10":{"success_rate": 0.500, "n": 90, "ci_95": [0.39, 0.61]}
    },
    "pairwise_tests": {
        "url_vs_baseline": {"test": "McNemar", "p": 0.001, "significant": true},
        ...
    }
}
```

Every number in the final report traces back to this file.

### Agent 0F: Figure Generation (Special)

Figures get a dedicated agent because they must be:
- **Consistent** across the entire report (same palette, same font sizes)
- **Vector format** (PDF for LaTeX, PNG for preview)
- **Colorblind-safe** (Okabe-Ito palette)
- **Self-contained** (caption tells the full story)

The figure agent reads all other Wave 0 outputs and generates every figure referenced in the plan. This prevents chapter agents from generating their own inconsistent figures.

### Completion Gate

**Do NOT proceed to Wave 1 until all of these are true:**

- [ ] Every file in the agent specification exists and is non-empty
- [ ] All figures compile (PDF + PNG both present)
- [ ] Key numbers in `final_results.json` match known ground truth
- [ ] Each agent's output has been spot-checked by the orchestrator
- [ ] No placeholder text like "TODO" or "TBD" in any data file

**Why this gate matters:** In the validated run (86-page FYP report), skipping spot-checks led to a chapter agent propagating an incorrect success rate through three sections. Fixing it required rewriting those sections. The 10-minute spot-check would have saved 30 minutes of rework.

---

## 4. Wave 1: Chapter Writing

### Chapter Dependency Graph

Not all chapters are equally independent. The dependency structure determines which agents can run in parallel:

```
                    Independent (fully parallel)
                    ============================
                    Ch1 (Introduction)
                    Ch2 (Literature Review)
                    Ch3 (System Design)        needs: 0B, 0C
                    Ch6 (Conclusion)           needs: 0A summary only

                    Sequential (must wait)
                    ============================
                    Ch4 (Experimental Setup)
                         ↓
                    Ch5 (Results)              needs: Ch4 definitions + 0A, 0D, 0E, 0F
```

Ch4 and Ch5 have a dependency: Ch5 references experimental conditions defined in Ch4. Assign them to the **same agent** to avoid cross-agent coordination.

### Agent Assignment Strategy

| Agent | Chapters | Wave 0 Dependencies | Approx Pages | Rationale |
|-------|----------|---------------------|:---:|-----------|
| **Agent 1** | Template + Front matter + Ch1 + Ch2 | Plan only | 15-20 | Intro and lit review need no data |
| **Agent 2** | Ch3 (System Design) | 0B, 0C | 12-18 | Heavy on architecture, code snippets |
| **Agent 3** | Ch4 + Ch5 (Setup + Results) | 0A, 0D, 0E, 0F | 15-25 | Data-heavy; keep sequential pair together |
| **Agent 4** | Ch6 + Appendices | 0A (summary only) | 5-10 | Light dependencies, mostly synthesis |

### How to Pass Wave 0 Data to Chapter Agents

Each chapter agent receives exactly three things:

1. **Chapter template**: The LaTeX skeleton for its assigned chapters (from `templates/`)
2. **Relevant data files**: Only the Wave 0 outputs it needs (see dependency column above)
3. **Shared preamble**: `preamble.tex` with all macro definitions and package imports

Example prompt for Agent 3:

```
You are writing Chapters 4 and 5 of an academic report.

Read these data files:
- data/final_results.json (all experiment numbers)
- data/experiment_history.md (what changed between versions)
- data/statistics.md (statistical tests and distributions)
- figures/ (all pre-generated figures)

Write to:
- chapters/ch4_experimental_setup.tex
- chapters/ch5_results.tex

Use ONLY numbers from the data files. Never compute or estimate.
Reference figures as \ref{fig:ch5:xxx} — always use chapter prefix.
```

### Label Naming Convention

With parallel agents, label collisions are inevitable unless you enforce a naming convention. Every label must carry a chapter prefix:

```latex
% Agent 2 (Chapter 3)
\label{fig:ch3:architecture}
\label{tab:ch3:tech-stack}
\label{sec:ch3:state-abstraction}

% Agent 3 (Chapter 5)
\label{fig:ch5:ablation-bar}
\label{tab:ch5:main-results}
\label{sec:ch5:discussion}
```

This convention eliminates 90% of cross-reference collisions during assembly.

---

## 5. Wave 2: Assembly and Compilation

### Merge Strategy

The main file uses `\input{}` to include chapter files. No chapter text lives in `main.tex` itself:

```latex
\documentclass[12pt,a4paper]{report}
\input{preamble}

\begin{document}
\input{front_matter}
\tableofcontents
\listoffigures
\listoftables

\input{chapters/ch1_introduction}
\input{chapters/ch2_literature_review}
\input{chapters/ch3_system_design}
\input{chapters/ch4_experimental_setup}
\input{chapters/ch5_results}
\input{chapters/ch6_conclusion}

\bibliographystyle{plain}
\bibliography{references}

\appendix
\input{appendices/appendix_a}
\input{appendices/appendix_b}
\end{document}
```

### Cross-Reference Audit (Mandatory)

Run the automated audit script before compiling:

```bash
python scripts/cross_ref_audit.py report_dir/
```

The script checks:
- Duplicate `\label{}` definitions across all `.tex` files
- Undefined `\ref{}` and `\cite{}` targets
- Orphaned labels (defined but never referenced)
- BibTeX key collisions

Fix every issue before compiling. The most common problem is duplicate labels from agents that ignored the chapter-prefix convention.

### Compilation Pipeline

```bash
# Single command — handles BibTeX + multiple passes
tectonic main.tex

# If debugging
tectonic -X compile main.tex 2>&1 | grep -E "(Warning|Error)"
```

### Quality Review Checklist

After successful compilation, verify:

- [ ] No undefined references in the PDF
- [ ] No duplicate labels in the log
- [ ] All figures render at correct size (not clipped, not tiny)
- [ ] Table of Contents matches actual chapter titles
- [ ] List of Figures and List of Tables are complete
- [ ] Page numbers are sequential and correct
- [ ] All bibliography entries resolve
- [ ] Appendices are properly lettered (A, B, C)
- [ ] No major overfull/underfull hbox warnings
- [ ] Consistent formatting across all chapters (fonts, spacing, heading style)

---

## 6. Agent Communication Protocol

### Agents Are Independent

Agents in the same wave **never communicate with each other**. There is no message-passing, no shared memory, no coordination channel. Each agent reads its inputs, writes its outputs, and terminates.

This is a deliberate design choice. Inter-agent communication introduces race conditions, ordering dependencies, and debugging complexity that outweigh any benefit for document writing.

### Shared State Lives in Files

All coordination happens through the filesystem:

```
report/
├── data/                    # Wave 0 outputs (read by Wave 1)
│   ├── final_results.json
│   ├── codebase_analysis.md
│   ├── system_analysis.md
│   ├── experiment_history.md
│   └── statistics.md
├── figures/                 # Wave 0F outputs (read by Wave 1)
│   ├── ablation_bar.pdf
│   ├── ablation_bar.png
│   └── ...
├── chapters/                # Wave 1 outputs (read by Wave 2)
│   ├── ch1_introduction.tex
│   ├── ch2_literature_review.tex
│   └── ...
├── preamble.tex             # Shared by all agents
└── main.tex                 # Wave 2 assembly
```

### Consistency Enforcement

Without communication, consistency is enforced by three mechanisms:

1. **Shared preamble** (`preamble.tex`): All agents include the same preamble, so macros, packages, and formatting are identical.

2. **Shared macro definitions**: Define project-specific terms as LaTeX macros:
   ```latex
   % In preamble.tex — used by ALL chapter agents
   \newcommand{\projectname}{Web UTG Crawler}
   \newcommand{\numstates}{150}
   \newcommand{\successrate}{50.0\%}
   ```

3. **Terminology glossary**: Define key terms once in the plan file. Every agent receives this glossary. Example:
   ```
   GLOSSARY (use these exact terms):
   - "state" (not "page" or "node" when referring to UTG states)
   - "transition" (not "edge" or "link")
   - "exploration" (not "crawling" when referring to strategy)
   - "success rate" (not "accuracy" or "pass rate")
   ```

   Without this, Agent 1 might write "crawling" while Agent 2 writes "exploration" for the same concept — confusing readers.

---

## 7. Error Recovery

### Agent Failure

If a single agent fails (crashes, produces garbage, or times out):

1. **Identify the failed agent** from logs or missing output files.
2. **Rerun that agent only.** No other agent is affected because agents are independent.
3. **Do not rerun the entire wave.** Successful agents' outputs are already on disk.

```
Example: Agent 0D (Experiment History) crashes after 20 minutes.
Fix: Rerun Agent 0D. Agents 0A, 0B, 0C, 0E, 0F are unaffected.
Total cost: 20 minutes wasted + 1 rerun, not 60 minutes of full-wave restart.
```

### Numbers Do Not Match

If a chapter agent produces text with numbers that contradict `data/final_results.json`:

1. **Check Wave 0 first.** Is the data file itself correct?
   - If the data file is wrong: fix it in Wave 0, then rerun affected Wave 1 agents.
   - If the data file is correct: the chapter agent misread it. Rerun that agent with clearer instructions.

2. **Never hand-edit numbers in `.tex` files.** The data file is the source of truth. Editing the prose directly creates a drift that will resurface when the chapter is regenerated.

### Cross-Reference Collisions

If the audit script reports duplicate labels:

1. **Rename with chapter prefix.** Change `\label{fig:architecture}` to `\label{fig:ch3:architecture}`.
2. **Update all `\ref{}` calls** that point to the renamed label.
3. **Rerun the audit** to confirm zero collisions.

This is the most common Wave 2 issue and takes 5-10 minutes to fix manually. The chapter-prefix naming convention (Section 4) prevents most collisions proactively.

### Compilation Errors

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| `Undefined control sequence` | Missing package in preamble | Add to `preamble.tex`, recompile |
| `File not found` | Wrong figure path | Check `figures/` directory matches `\includegraphics` paths |
| `Missing \begin{document}` | Syntax error in a chapter file | Check the last-modified `.tex` file for unclosed environments |
| `Citation undefined` | BibTeX key mismatch | Verify keys in `.bib` file match `\cite{}` calls |

---

## 8. Scaling the Pipeline

The 3-wave architecture scales to different document sizes by adjusting the number of Wave 1 agents:

### FYP / MSc Thesis (60-80 pages)

The default configuration. 3-4 Wave 1 agents, 5-6 Wave 0 agents.

```
Wave 0: 5-6 agents (30-60 min)
Wave 1: 3-4 agents (60-90 min)
Wave 2: 1-2 agents (20-40 min)
Total:  2-4 hours
```

### PhD Dissertation (150-300 pages)

More chapters, possibly more data sources. Scale Wave 0 and Wave 1:

```
Wave 0: 6-8 agents (45-90 min)
  - Split 0A into 0A-data and 0A-literature (systematic review data)
  - Add 0G: Related work matrix (for 30+ page lit review)
Wave 1: 5-8 agents (90-150 min)
  - Ch1 alone (15-20 pages with extended background)
  - Ch2 alone (25-35 pages literature review)
  - Ch3 alone (20-30 pages methodology)
  - Ch4+5 together (30-50 pages experiments + results)
  - Ch6+7 together (discussion + conclusion, 15-25 pages)
  - Appendices (separate agent, 20-40 pages)
Wave 2: 2-3 agents (30-60 min)
  - Merge + cross-ref audit
  - Compile + format review
  - Final bibliography check
Total:  4-8 hours
```

### Technical Report (20-40 pages)

Lighter configuration. Wave 0 can be compressed:

```
Wave 0: 2-3 agents (15-30 min)
  - Combine data + stats into one agent
  - Figures still get their own agent
Wave 1: 2 agents (30-60 min)
  - Agent 1: Intro + Background + Methods
  - Agent 2: Results + Discussion + Conclusion
Wave 2: 1 agent (15-20 min)
Total:  1-2 hours
```

### Scaling Heuristic

A rough formula for planning:

```
Wave 1 agents = ceil(total_pages / 25)
Wave 0 agents = max(3, number_of_distinct_data_sources)
Estimated hours = 0.5 + (Wave_1_agents * 0.5) + 0.5
```

---

## 9. Implementation Notes

### Launching Agents in Claude Code

Use the Agent tool with `run_in_background=true` to launch parallel agents:

```
# Wave 0 — launch all 6 agents simultaneously
Agent(task="Consolidate experiment data into data/final_results.json...", run_in_background=true)
Agent(task="Analyze codebase and produce data/codebase_analysis.md...", run_in_background=true)
Agent(task="Analyze system architecture into data/system_analysis.md...", run_in_background=true)
Agent(task="Compile experiment history into data/experiment_history.md...", run_in_background=true)
Agent(task="Compute statistics and write data/statistics.md...", run_in_background=true)
Agent(task="Generate all figures as PDF+PNG in figures/...", run_in_background=true)
```

Wait for all background tasks to complete before proceeding to Wave 1.

### Monitoring Progress

Use TodoWrite to track agent completion:

```
Wave 0 Progress:
- [x] 0A: Data consolidation     (completed 14:32)
- [x] 0B: Codebase analysis      (completed 14:28)
- [x] 0C: System analysis        (completed 14:35)
- [ ] 0D: Experiment history      (running...)
- [x] 0E: Statistics              (completed 14:30)
- [ ] 0F: Figure generation       (running...)
```

### File Organization

Each agent should produce a **standalone `.tex` file** that compiles when included via `\input{}`. The file must:
- Not contain `\documentclass` or `\begin{document}` (those live in `main.tex`)
- Not define packages (those live in `preamble.tex`)
- Use only macros defined in the shared preamble
- Reference figures with paths relative to the project root

### What NOT to Pass to Chapter Agents

**Never pass the raw codebase** to a chapter agent. Raw source code is too large, too detailed, and will consume context window capacity that the agent needs for writing. Instead, pass only the processed Wave 0 artifacts:

| Pass This | Not This |
|-----------|----------|
| `data/codebase_analysis.md` (500 lines) | `src/` directory (5,000+ lines) |
| `data/final_results.json` (100 lines) | 90 raw result files (10,000+ lines) |
| `figures/ablation_bar.pdf` (reference path) | Raw matplotlib script |

The Wave 0 agents exist precisely to compress raw project artifacts into chapter-agent-ready summaries.

### Prompt Template for Chapter Agents

A proven prompt structure for Wave 1 agents:

```
ROLE: You are writing [Chapter X: Title] of an academic report.

CONTEXT:
- Project: [one-sentence description]
- Core contribution: [one sentence]
- Report structure: [list of all chapters with one-line descriptions]

DATA FILES (read these first):
- [list of relevant Wave 0 outputs with file paths]

CONSTRAINTS:
- Use ONLY numbers from the data files. Never compute or estimate.
- Use labels with chapter prefix: fig:chX:, tab:chX:, sec:chX:
- Follow the terminology glossary below.
- Target length: [N-M] pages.
- Write to: chapters/chX_title.tex

GLOSSARY:
- [term definitions]

TEMPLATE:
[paste the chapter skeleton from templates/]
```

This template has been validated across multiple report-writing sessions. The key elements are: explicit data file references, the label convention reminder, and the length target.

---

## Summary

The 3-wave parallel pipeline turns a serial 8-12 hour writing marathon into a 2-4 hour parallel execution. The architecture is simple:

1. **Wave 0**: Prepare all data. Gate: every file exists and is verified.
2. **Wave 1**: Write chapters in parallel. Gate: every `.tex` file is complete.
3. **Wave 2**: Merge, audit cross-references, compile, review.

The key insight is that **data dependency is the only real constraint**. Chapters are independent once they have their data. Agents are independent because they communicate only through files. And the pipeline scales linearly — more chapters means more Wave 1 agents, not more complexity.
