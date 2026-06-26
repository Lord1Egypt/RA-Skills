# Phase: Brainstorming & Ideation

## Goal

Generate a ranked set of candidate research directions using a structured
divergence-to-convergence loop that mitigates confirmation bias and premature commitment.

## Entry Conditions

- User has a broad topic area or a specific problem they want to explore
- OR: backtracking from Lit Review because the novelty gap was false

## Ideation Frameworks

This phase uses 12 structured ideation frameworks for candidate generation. Load the full
framework details from [phases/ideation-frameworks.md](ideation-frameworks.md). Each
framework targets a distinct cognitive mode — use 2-3 per session based on the
researcher's situation:

| # | Framework | Best When |
|---|-----------|-----------|
| F1 | Problem-First vs. Solution-First | Orienting: classifying where the idea comes from |
| F2 | Problem Reformulation | Feeling stuck — reframe the question itself |
| F3 | Abstraction Laddering | Have a specific result, need to go broader or deeper |
| F4 | Tension & Contradiction Hunting | Exploring a field — find unresolved trade-offs |
| F5 | Analogical Reasoning & Cross-Pollination | Need genuinely novel angles from other fields |
| F6 | What Changed? + Adjacent Possible | Revisiting old ideas under new conditions |
| F7 | Failure Analysis & Boundary Probing | Challenging popular methods — find where they break |
| F8 | Constraint Manipulation | Want transformational ideas — change the rules |
| F9 | Negation and Inversion | Challenge conventional wisdom — flip assumptions |
| F10 | Composition & Decomposition | Recombining or modularizing existing techniques |
| F11 | Simplicity Test | Suspect a simpler approach would suffice |
| F12 | Stakeholder Rotation | Need multiple perspectives on a system |

**Quick selection** — match the researcher's situation:

| Situation | Start With |
|-----------|------------|
| "I don't know what area to work in" | F4 (Tensions) → F6 (What Changed) |
| "Vague area, no specific idea" | F3 (Abstraction) → F7 (Failure Analysis) |
| "Have an idea, not sure it's good" | Two-Sentence Test → F11 (Simplicity) |
| "Good idea, need a fresh angle" | F5 (Cross-Pollination) → F12 (Stakeholders) |
| "Want to combine existing work" | F10 (Composition/Decomposition) |
| "Found a technique, want to apply it" | F1 (Problem-First Check) → F12 (Stakeholders) |
| "Challenge conventional wisdom" | F9 (Negation) → F7 (Failure Analysis) |
| "Stuck thinking one way" | F2 (Reformulation) → F8 (Constraint Manipulation) |
| "Revisiting an old/failed idea" | F6 (What Changed) → Adjacent Possible mapping |

## Step-by-Step Protocol

### Step 1: Diverge — Generate Candidates (Problem Landscape Map)

Generate 10-30 candidate problems. For each, write a **one-sentence claim** — the
thing you would defend if the research succeeds.

**How to generate candidates:**
- Ask the user about their domain, constraints, and interests
- Select 2-3 ideation frameworks from the table above (see
  [ideation-frameworks.md](ideation-frameworks.md) for full instructions)
- Walk through each framework interactively, asking the researcher for domain-specific inputs
- Additionally:
  - Search recent literature (arXiv, Semantic Scholar, Google Scholar) for active threads
  - Identify gaps: what is assumed but unverified? what fails at scale? what lacks baselines?
  - Check for "obvious baselines" that haven't been tried

**For a deep ideation session** (when the user wants thorough exploration), use the
Integrated Creative Thinking Protocol from ideation-frameworks.md, which chains all 12
frameworks across four phases (~90 min).

**Output format:**
```
| # | One-sentence claim | Domain | Source framework | Source of idea |
|---|-------------------|--------|-----------------|----------------|
| 1 | "Fine-tuning on X improves Y by Z%" | NLP | F7 (Boundary Probing) | Gap in [paper] |
| 2 | "Applying auction theory to..." | ML Systems | F5 (Cross-Pollination) | Econ analogy |
| 3 | ... | | | |
```

### Step 2: Trajectory Sketching + Two-Sentence Pitch

For the top ~10 candidates, apply the **Two-Sentence Pitch Test** and outline 2-3
plausible research arcs.

**Two-Sentence Pitch** (quick filter before investing in trajectory sketching):
> **S1** (Problem): "[Domain] struggles with [problem], which matters because [consequence]."
> **S2** (Insight): "We [approach] by [mechanism], which works because [reason]."

If a candidate cannot pass this test, it is not yet clear enough — return to Step 1 with
a specific framework (F1 for unclear problem, F11 for unclear mechanism, F4 for unclear
significance).

**Trajectory arcs** for candidates that pass:
```
Idea: [one-sentence claim]
Two-sentence pitch: [S1] [S2]
Arc A: [baseline] → [method improvement] → [generalization test]
Arc B: [baseline] → [different method] → [ablation study]
Arc C: [theoretical analysis] → [empirical validation] → [limits characterization]
```

This step forces you to think about what the *whole project* looks like, not just the
first experiment.

### Step 3: Feasibility & Ethics Gate

Quickly eliminate directions that fail hard constraints:

**Feasibility filters:**
- Data: does the required data exist and is it accessible?
- Compute: is the compute budget realistic for the timeline?
- Skills: does the team have (or can quickly acquire) needed expertise?
- Time: can a meaningful result be obtained in the available window?

**Ethics filters:**
- Does it involve human subjects? → need IRB/ethics review path
- Does it use identifiable private data? → need consent/de-identification plan
- Could the output be misused? → need risk mitigation discussion
- Are there unsafe deployment contexts? → need safety constraints

Mark each candidate: PASS / CONDITIONAL (with mitigation) / FAIL.

### Step 4: Convergent Scoring

Score remaining candidates using the rubric from
[templates/scoring-rubric.md](../templates/scoring-rubric.md).

Use a 1-5 scale per criterion. Present results as a table:

```
| Idea | Feasible | Interesting | Novel | Ethical | Relevant | Evaluable | Reproducible | Robust | Risk-Ctrl | Mean |
|------|----------|-------------|-------|---------|----------|-----------|-------------|--------|-----------|------|
| #1   | 4        | 5           | 4     | 5       | 4        | 4         | 5           | 3      | 4         | 4.2  |
```

**Decision rule**: select ideas scoring ≥ 3.5 mean. If none qualify, return to Step 1
with refined scope.

### Step 5: Prototype & Falsify

For top 1-3 ideas, run **fast falsification** experiments:
- Implement the simplest possible version (hours, not days)
- Run a "sanity check" baseline — if the baseline already solves it, the idea is moot
- Check for data leakage and label quality issues
- Test on a tiny subset first

**Key question**: "What is the cheapest experiment that would make me abandon this idea?"

If the idea survives falsification, proceed. If not, log the result (negative findings
are valid milestones!) and return to the scoring table.

### Step 6: Commit to Protocol

Once a direction survives:
1. Write a 1-paragraph research statement (claim + scope + method sketch)
2. Identify the primary metric, primary dataset, and primary baseline
3. Lock these before scaling up — this is your informal "preregistration"
4. Log the commitment in LOGBOX

### Step 7: Initialize Exploration Directory

If the project uses the exploration structure (see SKILL.md § File Management):

1. Create `explorations/NNN-slug/` — next sequential number + kebab-case name
2. Save brainstorming artifacts to the exploration directory:
   - `brainstorm.md` — scoring table, research statement, and falsification results
3. Add a row to the Exploration Registry in LOGBOX (status: `active`, parent: `—` or
   the exploration this was forked from)

**Multiple viable ideas**: if brainstorming produces 2-3 ideas above the 3.5 threshold,
create an exploration directory for each. Set the one the user chooses to pursue first
as `active` and the others as `paused`.

**Forking from a failed exploration**: when pivoting after a failed direction, set the old
exploration to `archived` and create the new one with the old ID as `parent`. Promote any
reusable artifacts (evidence maps, datasets) to `shared/`.

## Prompt Bank

Use these questions to push thinking during brainstorming.

**Problem & contribution:**
- What is the smallest, sharpest claim we want to defend?
- If we succeed, what changes for (a) theory, (b) practice, (c) measurement?
- What is the "obvious baseline" that must be beaten to matter?

**Mechanism & assumptions:**
- What assumption is currently taken for granted that may be false?
- What mechanism would explain the effect if the result is real?
- What conditions would make the method fail?

**Data & measurement:**
- What is the target population/distribution? What is the sampling process?
- What labels are assumed "ground truth," and how might they be biased?
- What data leakage pathways exist?

**Evaluation & falsification:**
- What metric best matches the real objective (and what metric is easiest to game)?
- What "sanity check" would immediately invalidate our pipeline if it fails?
- What ablations distinguish "real contribution" from incidental engineering?

**Framework-specific probes** (use when applying ideation frameworks):
- *Reformulation*: Are we solving the right problem, or a convenient proxy?
- *Abstraction*: What is the general principle behind this specific result?
- *Tension*: Which two goals does everyone want but treats as a trade-off?
- *Analogy*: What field solves a structurally similar problem with different tools?
- *What Changed*: What was dismissed 5 years ago that new conditions make viable?
- *Boundary*: Where exactly does the current best method break down?
- *Constraint*: Which hidden assumption, if dropped, would change everything?
- *Negation*: What if the opposite of conventional wisdom were true?
- *Composition*: What two existing techniques, combined, create emergent capability?
- *Simplicity*: If we strip this to one key idea, does it still work?
- *Stakeholder*: Who besides ML researchers would care about this problem?

## Creative Blocks

If the researcher is stuck, diagnose the block and apply a targeted framework
(see the full table in [ideation-frameworks.md](ideation-frameworks.md)):

| Block | Symptom | Unblock With |
|-------|---------|-------------|
| Fixation | Cannot think about the problem differently | F2 (Reformulation) |
| Tunnel vision | All ideas from same subfield | F5 (Cross-Pollination) |
| Self-censoring | Dismissing "weird" ideas too early | F9 (Negation) — evaluate after generating |
| Incrementalism | Every idea is +2% on a benchmark | F8 (Constraint Manipulation) |
| Analysis paralysis | Too many options | F6 (Adjacent Possible) — what is feasible now? |
| False dichotomy | Stuck choosing A vs. B | F4 (Janusian Synthesis) |

## Exit Criteria

- [ ] At least one idea scores ≥ 3.5/5 on the scoring rubric
- [ ] Fast falsification did not kill the top pick
- [ ] Primary metric, dataset, and baseline are identified (not yet locked)
- [ ] Research statement (1 paragraph) is written
- [ ] Exploration directory created (if using multi-exploration structure)
- [ ] LOGBOX entry recorded

## Transition

**Forward → Lit Review**: carry the research statement, initial candidate papers, and
scoring table.

**Backward ← Lit Review**: if novelty gap turns out to be false, archive the current
exploration (`archived` in LOGBOX), return here, and either re-score or create a new
exploration.

**Fork → New Exploration**: if multiple viable ideas exist, create separate explorations
and let the user choose which to activate first.
