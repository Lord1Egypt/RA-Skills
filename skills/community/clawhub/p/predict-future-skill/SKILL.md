---
name: predict-future
description: >-
  Predicts what is likely to happen from a user's query by thinking through which
  forecasting theories fit, then applying one or more from references/. Use when
  the user names this skill or asks to forecast the near future.
---

# predict-future

Turn a user query into a forecast by **thinking through which theories fit**,
then applying **one or more** prediction theories from [references/](references/).
**Present each theory's forecast separately** — do not merge them into one
authoritative conclusion. The value is rigor: fight overconfidence and ignoring
base rates.

- **Output language**: respond in the same language the user used in their query.
- **Theories live in [references/](references/)** — think before you select; read
  only the files you chose; follow each file's **"How to apply in this skill"**
  section.

## Workflow

### Step 0: Set up the run folder

Generate a timestamp like `YYYYMMDD-HHmmss` and create `output/{timestamp}/`
(relative to the workspace root).

### Step 1: Restate & clarify

State clearly *what* is being predicted and its current state. If critical
information is missing, **ask 1–3 of the most decisive questions before
forecasting**. For non-critical gaps, proceed using explicit labeled assumptions.

### Step 2: Think through theory selection

**Before reading or applying any reference**, work through theory selection
deliberately. Do not default to any file. Pick the **minimum sufficient set** that addresses
the query's decisive uncertainty; add a second or third theory only when it
materially improves the forecast.

#### Reference library

| File | Thinker | Use when the query involves… |
|------|---------|------------------------------|
| [general_Philip_Tetlock.md](references/general_Philip_Tetlock.md) | Philip Tetlock | Open-ended probabilistic forecasts, triage, Fermi decomposition, dragonfly eye, granular probabilities, Bayesian updating, outside view |
| [finance_howard_marks.md](references/finance_howard_marks.md) | Howard Marks | Consensus vs. price, cycles, second-level thinking, credit/macro sentiment |
| [finance_robert_shiller.md](references/finance_robert_shiller.md) | Robert Shiller | Valuation (CAPE), narratives, bubbles, sentiment contagion |
| [finance_hyman_minsky.md](references/finance_hyman_minsky.md) | Hyman Minsky | Credit fragility, financing regimes, systemic breakdown risk |
| [tech_paul_saffo.md](references/tech_paul_saffo.md) | Paul Saffo | Uncertainty mapping, S-curves, weak signals, when not to forecast |
| [tech_geoffrey_moore.md](references/tech_geoffrey_moore.md) | Geoffrey Moore | Product adoption stage, chasm, beachhead, whole product, GTM |
| [tech_clayton_christensen.md](references/tech_clayton_christensen.md) | Clayton Christensen | Disruption vs. sustaining, industry shift, incumbent response |
| [intl_structural_realism.md](references/intl_structural_realism.md) | Waltz / Mearsheimer | Great-power behavior, balance of power, balancing vs. buck-passing, long-run geopolitical trajectory |
| [intl_bruce_bueno_de_mesquita.md](references/intl_bruce_bueno_de_mesquita.md) | Bruce Bueno de Mesquita | Specific policy/negotiation/power-struggle outcomes via stakeholder bargaining; regime behavior (selectorate) |
| [intl_thomas_schelling.md](references/intl_thomas_schelling.md) | Thomas Schelling | Crisis bargaining, deterrence vs. compellence, credibility, escalation, brinkmanship |

#### When to include each theory (examples, not defaults)

| Include… | When the decisive uncertainty is… |
|----------|-----------------------------------|
| `general_Philip_Tetlock.md` | You need triage, reference-class/base-rate reasoning, decomposition, multi-angle synthesis, or calibrated probabilities — typical for open-ended "will X happen?" questions |
| `finance_*` | Price, narrative, consensus, cycles, or credit structure drive the answer |
| `tech_*` | Adoption stage, uncertainty mapping, disruption, or incumbent dynamics drive the answer |
| `intl_*` | International/state behavior, geopolitics, conflict, deterrence, or policy bargaining drive the answer |

| Domain signal | Typical starting candidates (still justify each) |
|---------------|--------------------------------------------------|
| Equities, bonds, credit, rates, macro, housing, sentiment | `finance_howard_marks.md`, `finance_robert_shiller.md`; `finance_hyman_minsky.md` if leverage/credit stress matters |
| Product launch, SaaS, platforms, startups, adoption, "will X disrupt Y?" | `tech_geoffrey_moore.md`, `tech_clayton_christensen.md`, `tech_paul_saffo.md` — pick by which uncertainty dominates |
| Great-power rivalry, war/crisis, deterrence, sanctions, treaties, foreign policy | `intl_structural_realism.md` for long-run structure; `intl_bruce_bueno_de_mesquita.md` for specific negotiated outcomes; `intl_thomas_schelling.md` for escalation/deterrence — pick by which uncertainty dominates |
| Elections, geopolitics, sports, one-off events | Often `general_Philip_Tetlock.md` alone — but only if probabilistic forecasting is appropriate; add `intl_*` when state-level strategy dominates |

Write `output/{timestamp}/theories-selected.md` **before reading any reference file**:

- Per-file fit assessment (all ten files)
- Final list of selected references with rationale
- Explicit list of **excluded** references with rationale

Only then proceed to evidence gathering and application.

### Step 3: Gather evidence

**This step requires live research** — do not rely on memory alone. Call at least
one tool before applying theories

| Tool | Use for |
|------|---------|
| **Search** | Discover sources, base rates, recent news, and comparable cases |
| **Web extraction** | Full text of a specific URL from search results |
| **Control browser** | Pages that need interaction or JS rendering (e.g. X/Twitter, Reddit, TikTok, Xiaohongshu)，please close web tabs after you use this tool |

Save every fetched/derived artifact as an intermediate file in the run folder.
Do not fabricate facts; if something can't be verified, label it an assumption.
Examples:

- `output/{timestamp}/research-base-rates.md`
- `output/{timestamp}/research-scheduled-events.md`
- `output/{timestamp}/sources.md` (URLs + key extracts)

### Step 4: Apply selected theories

Apply **each selected reference** in turn. For every theory, produce a **complete,
standalone forecast** — reasoning plus a clear **prediction conclusion** (outcome,
probability or qualitative call, horizon, falsifiable triggers). **Do not blend
theories into one answer** while applying them; disagreements between theories
are a feature, not a bug.

### Step 5: Final output file

Write `output/{timestamp}/output.md` with this structure (translate headings into
the user's language). **One section per applied theory**, each ending with that
theory's own prediction. Omit sections for theories you did not select. **No
merged "final verdict"** — if theories disagree, present each view and optionally
add a short **cross-theory comparison** noting agreements and tensions without picking a winner.

```
# Forecast: [subject]

## Original input
[User's query verbatim]

## Theory selection (reasoning)
- Decisive uncertainty: …
- Selected: [filename] — rationale
- Not selected: [filename] — rationale

## Selected forecasting theories
- [filename] — selection rationale
- …

## Evidence gathered
- [Key fact] — source / or labeled as assumption

## [Theory one, e.g. Tetlock]
[Reasoning per that reference's apply steps]

### [Theory one] — prediction
- Forecast: …
- Probability / qualitative call: …
- Confidence: …
- Falsifiable conditions: …

## [Theory two, e.g. Howard Marks]
[Reasoning per that reference's apply steps]

### [Theory two] — prediction
- Forecast: …
- …

## [Theory three, e.g. Geoffrey Moore]
…

## Cross-theory comparison (optional)
- Points of agreement: …
- Points of disagreement: …
(Compare only — do not merge into a single conclusion)
```

Tell the user the path to `output/{timestamp}/output.md` when done.
