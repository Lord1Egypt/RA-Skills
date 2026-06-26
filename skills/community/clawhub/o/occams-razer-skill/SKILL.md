skill_name: OccamsRazorAnalyzer
version: 1.0.0
description: A logical analysis tool that applies the principle of parsimony (Occam's Razor) to evaluate competing hypotheses. Capable of operating in Forensic (probabilistic) and Academic (theoretical) modes.
tags:
  - logic
  - reasoning
  - analysis
  - forensics
  - philosophy
  - problem-solving
inputs:
  scenario_description:
    type: string
    description: The problem, event, or phenomenon requiring explanation.
    required: true
  hypotheses:
    type: array
    items: string
    description: A list of competing explanations or theories to be evaluated.
    required: true
  mode:
    type: string
    enum: [FORENSIC, ACADEMIC, COMBINED]
    default: COMBINED
    description: Sets the operational environment. FORENSIC prioritizes evidence probability. ACADEMIC prioritizes ontological economy. COMBINED utilizes both channels.
  constraints:
    type: array
    items: string
    description: Optional list of known facts or axioms that must be adhered to.
    required: false
outputs:
  preferred_hypothesis: string
  complexity_analysis: object
  logic_rationale: string
  confidence_score: percentage
---

# Occam's Razor Analyzer

## Overview

This skill implements the **Principle of Parsimony** (Occam's Razor: *Entities should not be multiplied without necessity*). It serves as a rational engine to evaluate competing explanations for a phenomenon. It does not claim to discern absolute truth, but rather to identify the explanation with the highest probability of accuracy based on the economy of assumptions.

## Operational Modes

The agent must adapt its reasoning strategy based on the `mode` specified in the input.

### 1. FORENSIC Mode (Investigative)
**Context:** Crime scenes, system outages, medical diagnoses, debugging, historical analysis.
**Logic Style:** Probabilistic and Evidentiary.

*   **Objective:** Identify the most likely sequence of events.
*   **Heuristic:** Avoid the "Conspiracy Trap." Complex coordinated actions are statistically rare compared to simple incompetence or single-actor events.
*   **Rule:** If Theory A requires three independent failures to occur simultaneously, and Theory B requires only one failure, prefer Theory B *unless* direct evidence explicitly contradicts Theory B.

### 2. ACADEMIC Mode (Theoretical)
**Context:** Philosophy, theoretical physics, mathematics, conceptual debate.
**Logic Style:** Ontological and Structural.

*   **Objective:** Identify the most elegant theoretical framework.
*   **Heuristic:** Avoid "Ad Hoc Rescue" (adding assumptions to save a favored theory).
*   **Rule:** Do not postulate the existence of new entities, forces, or dimensions if existing ones suffice to explain the phenomenon. Prefer the theory that integrates most smoothly with established axioms.

## Execution Workflow

When this skill is invoked, follow this internal process:

1.  **Deconstruction:** Break down each provided hypothesis into a chain of logical dependencies.
2.  **Assumption Counting:** Identify "Assumptions"—statements not supported by provided evidence (Constraints) or established axioms.
3.  **Complexity Scoring:** Assign a score to each hypothesis based on the number of unproven assumptions.
4.  **Comparative Analysis:**
    *   Select the hypothesis with the lowest Complexity Score that still fully explains the `scenario_description`.
    *   If scores are equal, analyze the "Bayesian Likelihood" of the assumptions (Forensic) or "Theoretical Elegance" (Academic).
5.  **Fallacy Check:**
    *   *Simplistic Fallacy:* Does the simpler theory ignore critical evidence? If so, penalize it.
    *   *Ad Hoc Rescue:* Does the complex theory add convenient exceptions to fit the data? If so, penalize it.
6.  **Synthesis:** Generate the output JSON explaining which hypothesis was "shaved" and why.

## Usage Examples

### Example 1: Forensic Investigation
**Input:**
*   **Scenario:** "Database server crashed at 3:00 AM. No human logs detected."
*   **Hypotheses:**
    1.  A cosmic ray flipped a bit in the RAM, causing a cascade failure.
    2.  The automated maintenance script has a memory leak that only triggers under high load.
*   **Mode:** `FORENSIC`

**Agent Logic:**
*   *Hypothesis 1 Assumptions:* Cosmic ray occurrence (rare), specific bit location (specific), lack of ECC correction (specific).
*   *Hypothesis 2 Assumptions:* Memory leak exists in code (common), high load occurred (common).
*   *Rationale:* Hypothesis 2 is statistically more probable and requires fewer rare physical events.

### Example 2: Academic Logic
**Input:**
*   **Scenario:** "Why do objects fall?"
*   **Hypotheses:**
    1.  Invisible intangible angels push them down.
    2.  Curvature of spacetime caused by mass (General Relativity).
*   **Mode:** `ACADEMIC`

**Agent Logic:**
*   *Hypothesis 1 Assumptions:* Existence of angels, intangibility property, intent to push.
*   *Hypothesis 2 Assumptions:* Spacetime is a fabric, mass affects geometry.
*   *Rationale:* Hypothesis 1 multiplies entities (angels) without necessity. Hypothesis 2 uses existing frameworks (mass, space) to explain the phenomenon, satisfying ontological economy.
```