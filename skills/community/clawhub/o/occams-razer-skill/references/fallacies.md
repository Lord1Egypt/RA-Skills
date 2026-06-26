Here is the final reference document, formatted as a structured markdown guide designed to complement the Occam's Razor skill.

```markdown
# Logical Fallacies Reference Guide

## Overview
This document serves as a diagnostic tool for the Occam's Razor Analyzer. When evaluating hypotheses, the agent should cross-reference this list to identify structural weaknesses in reasoning. Detecting a fallacy often indicates a violation of parsimony or an error in the logical chain.

---

## 1. Fallacies of Relevance (Distractions)
*Arguments that rely on information unrelated to the logical conclusion.*

### Ad Hominem (Abusive)
*   **Definition:** Attacking the character or motive of the person making an argument rather than the argument itself.
*   **Structure:** Person A makes Claim X. Person B attacks Person A. Therefore, Claim X is false.
*   **Occam’s Razor Interaction:** Often used to dismiss a hypothesis without addressing its assumptions. In `FORENSIC` mode, an agent might validly question a witness's credibility, but this is evidence assessment, not logical disproof.

### Red Herring
*   **Definition:** Introducing an irrelevant topic to divert attention from the original issue.
*   **Structure:** Topic A is under discussion. Topic B is introduced under the guise of being relevant. Topic A is abandoned.
*   **Occam’s Razor Interaction:** Increases the "complexity score" of the dialogue by adding entities that do not explain the core phenomenon.

### Straw Man
*   **Definition:** Creating a distorted or exaggerated version of an opponent's argument and then attacking that version.
*   **Structure:** Person A makes Claim X. Person B restates Claim X as distorted Claim Y. Person B attacks Claim Y. Person B concludes Claim X is false.
*   **Occam’s Razor Interaction:** Creates a "ghost hypothesis" that is easier to dismantle than the actual hypothesis, violating the principle of accurate evidence assessment.

---

## 2. Fallacies of Ambiguity & Presumption
*Arguments that rely on unclear language or unwarranted assumptions.*

### Begging the Question (Circular Reasoning)
*   **Definition:** The conclusion of an argument is assumed in one of the premises.
*   **Structure:** A is true because B is true; B is true because A is true.
*   **Occam’s Razor Interaction:** A fatal flaw in `ACADEMIC` mode. It creates a logical loop that explains nothing while appearing to offer an explanation.

### False Dilemma (Bifurcation)
*   **Definition:** Presenting two alternatives as the only possibilities, when in fact other options exist.
*   **Structure:** Either X or Y is true. X is false. Therefore, Y must be true. (Ignoring options Z, W, etc.)
*   **Occam’s Razor Interaction:** Artificially limits the hypothesis space. This often forces the agent to choose a complex hypothesis because the simpler alternatives were "defined away."

### Ad Hoc Rescue
*   **Definition:** Adding arbitrary assumptions to a theory specifically to save it from being falsified by evidence.
*   **Structure:** Theory A predicts Outcome X. Outcome Y happens. Proponent adds Assumption Z to Theory A to explain Y.
*   **Occam’s Razor Interaction:** **Critical Violation.** This is the direct opposite of Occam's Razor. It explicitly "multiplies entities" (assumptions) to preserve a preferred conclusion.

---

## 3. Fallacies of Statistical & Causal Error
*Errors common in `FORENSIC` mode involving probability and causation.*

### Post Hoc Ergo Propter Hoc
*   **Definition:** Assuming that because Event B followed Event A, Event A caused Event B.
*   **Structure:** A occurred, then B occurred. Therefore, A caused B.
*   **Occam’s Razor Interaction:** A premature assignment of causality. While simple, this explanation often ignores hidden variables (common causes), which are the true drivers.

### Slippery Slope
*   **Definition:** Asserting that a relatively small first step will inevitably lead to a chain of related events culminating in a significant impact.
*   **Structure:** If A, then B, then C... then Z. Z is bad. Therefore, A is bad.
*   **Occam’s Razor Interaction:** Requires a high number of specific conditional assumptions to all be true. In `FORENSIC` mode, a Slippery Slope argument usually has a low probability/low parsimony score because it requires a "perfect storm" of events.

### The Conjunction Fallacy
*   **Definition:** Assuming that specific conditions are more probable than a single general one.
*   **Structure:** (Famous Example: The "Linda" problem). A complex narrative containing multiple specific details is judged more probable than a broad category containing those details.
*   **Occam’s Razor Interaction:** Directly violates probabilistic parsimony.
    *   *Incorrect:* "He is a jazz-playing accountant." (More specific, less probable).
    *   *Correct:* "He is an accountant." (Less specific, more probable).
    The agent must always penalize hypotheses that over-specify details not required by the evidence.

### Gambler’s Fallacy
*   **Definition:** Thinking that future probabilities are altered by past events, when in reality they are independent.
*   **Structure:** X has happened frequently recently. Therefore, X is less likely to happen next (or more likely, depending on the bias).
*   **Occam’s Razor Interaction:** Introduces a "hidden variable" or "balancing force" to the system that does not exist, violating the simplicity of probabilistic models.

---

## 4. Fallacies of Evidence Quality
*Errors regarding the weight or existence of evidence.*

### Appeal to Ignorance (Argumentum ad Ignorantiam)
*   **Definition:** Asserting that a proposition is true because it has not yet been proven false, or vice versa.
*   **Structure:** There is no evidence against X. Therefore, X is true.
*   **Occam’s Razor Interaction:** In `ACADEMIC` mode, lack of evidence is not proof of existence. In `FORENSIC` mode, this is the "God of the Gaps" error—inserting a complex explanation (e.g., a conspiracy) simply because a simple one hasn't been fully proven yet.

### Hasty Generalization
*   **Definition:** Drawing a conclusion based on insufficient or non-representative evidence.
*   **Structure:** Sample S (which is too small) has property P. Therefore, Population N has property P.
*   **Occam’s Razor Interaction:** In `FORENSIC` mode, this leads to incorrect "base rates." It simplifies the data-gathering process but complicates the resulting hypothesis by requiring it to explain anomalies that would otherwise be outliers.

### Texas Sharpshooter Fallacy
*   **Definition:** Cherry-picking data to support a hypothesis, or drawing a target around the data points after the fact.
*   **Structure:** Ignoring data points A, B, and C because they don't fit. Focusing on D, E, and F which fit the hypothesis.
*   **Occam’s Razor Interaction:** A hypothesis that must ignore chunks of data to work is not parsimonious. A truly simple theory explains the *whole* data set, not just a curated subset.
```