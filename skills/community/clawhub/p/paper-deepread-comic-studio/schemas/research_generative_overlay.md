# Research-Generative Overlay For Paper Deep Reading

This overlay is now part of `paper_deep_reading_skill`. It must be applied **in addition to**, not instead of, all existing deep-reading, source-handling, report-contract, review-context, figure/table, formula-preservation, proof-to-practice, reviewer-audit, validation, and graph-handoff requirements.

## Non-Weakening Rule

- Never delete or weaken an existing `paper_deep_reading_skill` requirement to make room for this overlay.
- When there is tension between a shorter explanatory report and a more idea-generative report, choose the more idea-generative report.
- When there is tension between a safe factual claim and speculation about author intent, keep the factual claim safe and explicitly mark the author-side path as an evidence-backed reconstruction.
- When there is tension between generic future work and boundary-pushing research ideas, prioritize hidden-assumption-based and unavailable-mechanism-based idea generation.

## Core Lens

Read a paper as a reconstruction of the authors' possible design path:

\[
\text{Paper} = \text{Important Setting} + \text{Broken Assumption} + \text{Borrowed Tool} + \text{New Constraint} + \text{Surrogate Mechanism}.
\]

The strongest report should identify:

1. what mechanism was available in an easier setting;
2. why that mechanism becomes unavailable under the paper's target constraints;
3. what surrogate mechanism the authors invented;
4. how the narrative makes that surrogate feel inevitable;
5. which hidden assumptions of that surrogate can become new research ideas.

## Required Research-Generative Passes

### 1. Research Equation Pass

For every paper, extract the research equation:

\[
A(P) \cap \neg C \cap T \cap M \Rightarrow Z \approx Y.
\]

Where:

- \(A(P)\): an existing paradigm for an important problem;
- \(C\): a common assumption in prior work;
- \(\neg C\): the target setting where that assumption fails;
- \(T\): real-world constraints such as privacy, decentralization, non-IID data, limited labels, safety, latency, missing modalities, or limited compute;
- \(M\): a borrowed method family that almost works;
- \(Y\): the ideal mechanism that the borrowed method normally needs;
- \(Z\): the paper's constructed surrogate for \(Y\).

### 2. Author-Side Direction Discovery Pass

Reconstruct how the direction may have been found using this formula:

\[
\text{New Direction} = \text{Valuable Field} + \text{Painful Assumption} + \text{Emerging Tool} + \text{Unserved Setting}.
\]

Use careful language:

- "A plausible author-side thinking path is..."
- "The paper's setup suggests..."
- "The authors likely noticed..., but this is an inference rather than a factual claim about private thoughts."

### 3. Story-Construction Pass

Build a table:

| Challenge | Failure mode | Design principle | Module | Evidence |
|---|---|---|---|---|

Then identify whether the method is only a bag of modules:

\[
M_1 + M_2 + M_3
\]

or a closed loop:

\[
M_1 \Rightarrow M_2 \Rightarrow M_3 \Rightarrow M_1.
\]

### 4. Module Author-Thinking Pass

For every central module, use:

\[
M_i = \text{Failure} + \text{Unavailable Ideal Solution} + \text{Available Proxy} + \text{Design Choice} + \text{Assumption} + \text{Risk}.
\]

The report must say what each module is functionally replacing, not only what operation it performs.

### 5. Reverse Citation Logic Pass

For important citations or citation clusters, produce:

| Citation cluster | Narrative function | Assumption inherited | How this paper modifies it |
|---|---|---|---|

Common citation functions include field foundation, limitation paper, method ancestor, neighboring-field solution, strong baseline, benchmark protocol, implementation machinery, and negative contrast.

### 6. Experiments-As-Story-Evidence Pass

Read every experiment as:

\[
\text{Experiment} = \text{Claim} + \text{Counterfactual} + \text{Metric} + \text{Stress Condition}.
\]

State which alternative explanation each experiment rules out, which module it justifies, and whether the stress condition really tests the paper's claimed hard setting.

### 7. Reusable Story-Making Pattern Pass

Extract at least one reusable paper-making template, such as:

\[
A \text{ solves } P \text{ when } C; \quad T \Rightarrow \neg C; \quad M \text{ helps but requires } Y; \quad Y \notin T; \quad Z \approx Y.
\]

Also identify two-axis empty cells, replacement stories, and closed-loop contribution patterns when applicable.

### 8. Weakness-To-New-Idea Pass

Turn hidden assumptions into research directions:

\[
M_i \text{ works if } H_i \quad \Rightarrow \quad \text{New idea: make } M_i \text{ work under } \neg H_i.
\]

For each idea, state:

- violated hidden assumption;
- why the current paper is fragile there;
- what new mechanism would be needed;
- whether it is engineering follow-up, cross-domain transfer, or boundary-pushing research.

## Integrated Source

The overlay was merged from the following research-generative skill content, adapted so it strengthens rather than replaces `paper_deep_reading_skill`.

---

# Skill: Research-Generative Paper Reading

## Purpose

This skill turns a paper-reading task into a **research-generation exercise**.

It is designed for cases where the goal is not only to summarize a paper, but to infer:

- how the authors may have discovered the research direction;
- how they constructed the paper’s story;
- why each method module exists;
- why key related works were cited;
- what reusable “story-making” pattern the paper teaches;
- where future research opportunities and scientific boundary-pushing directions may lie.

The output should help a reader find **new research questions**, not merely understand the existing paper.

---

## Core Principle

Read the paper as if you are reconstructing the authors’ hidden design path.

Do not only ask:

> What did the paper do?

Instead ask:

> What sequence of observations, constraints, failures, borrowed ideas, and narrative choices could have led the authors to this work?

A strong reading should convert the paper from a static finished product into a dynamic reasoning trajectory.

---

## Recommended Output Structure

A high-quality report should usually contain the following sections:

1. One-sentence thesis of the paper
2. How the authors may have found this research direction
3. How the authors built the story
4. Method deep reading: the author-thinking behind each module
5. Why the key citations appear
6. How the experiments support the story
7. What story-making pattern is worth learning
8. Weaknesses, hidden assumptions, and fragile links
9. New research points and boundary-pushing directions
10. Final evaluation

Sections 2, 3, 4, 5, and 7 are the most important when the user asks for an author-perspective or research-inspiration reading.

---

# 1. First Pass: Identify the Paper’s Research Equation

Start by extracting the paper’s core research equation.

A useful template is:

\[
\text{Paper} =
\text{Important Setting}
+
\text{Broken Assumption}
+
\text{Borrowed Tool}
+
\text{New Constraint}
+
\text{Surrogate Mechanism}
\]

Or more explicitly:

\[
\text{Research Direction}
=
A(P)
\;\cap\;
\neg C
\;\cap\;
T
\;\cap\;
M
\]

Where:

- \(A(P)\): an existing paradigm \(A\) that solves an important problem \(P\);
- \(C\): a common assumption made by prior work;
- \(\neg C\): the paper’s target setting where this assumption fails;
- \(T\): a difficult real-world constraint, such as privacy, decentralization, non-IID data, low labels, latency, safety, limited compute, missing modalities, or distribution shift;
- \(M\): a method family that seems promising but cannot be directly applied.

The paper usually becomes interesting when:

\[
A \text{ is useful, but assumes } C;
\quad
T \text{ makes } C \text{ invalid};
\quad
M \text{ helps, but relies on } Y;
\quad
Y \text{ is unavailable under } T.
\]

Then the authors’ contribution often becomes:

\[
\text{Replace unavailable mechanism } Y
\text{ with new mechanism } Z.
\]

This gives a powerful reading lens:

> What unavailable mechanism did the authors replace?

Examples of unavailable mechanisms:

| Unavailable mechanism \(Y\) | Possible replacement \(Z\) |
|---|---|
| central server | neighbor consensus, peer graph, gossip update |
| labels | pseudo-labels, weak supervision, self-supervision |
| shared validation set | synthetic validation set, proxy risk, agreement score |
| global data | generated data, prototypes, public data, embeddings |
| trusted clients | reputation, uncertainty, robust aggregation |
| full communication | compression, event-triggered update, local caches |
| aligned modalities | contrastive bridges, latent anchors, adapters |

---

# 2. How the Authors May Have Found the Direction

This section should reconstruct the “research discovery path.”

Do not write it as a factual claim about the authors’ private thoughts. Write it as an evidence-based reconstruction:

> The authors likely noticed that...
>
> A plausible thinking path is...
>
> The paper’s setup suggests the following chain...

## 2.1 Direction-Finding Formula

Use this formula:

\[
\text{New Direction}
=
\text{Valuable Field}
+
\text{Painful Assumption}
+
\text{Emerging Tool}
+
\text{Unserved Setting}
\]

A strong paper often emerges from one of the following intersections:

\[
\text{Direction}
=
\text{Popular Paradigm}
\times
\text{Realistic Constraint}
\times
\text{Underexplored Failure Mode}
\]

or:

\[
\text{Direction}
=
\text{Method That Works Somewhere}
-
\text{Condition It Secretly Requires}
+
\text{Setting Where That Condition Fails}
\]

When reading, identify:

1. **The popular paradigm**  
   What research area is already important or active?

2. **The hidden assumption**  
   What does prior work quietly assume?

3. **The realistic violation**  
   In the real world, when does this assumption fail?

4. **The tempting borrowed method**  
   What existing technique almost solves the issue?

5. **The blocking constraint**  
   Why can’t that technique be directly used?

6. **The authors’ conceptual replacement**  
   What new mechanism plays the role of the missing piece?

## 2.2 Reconstructing the Authors’ Initial Observation

Many papers begin from a dissatisfaction:

\[
\text{Existing Work Works}
\quad
\text{but only when}
\quad
C_1, C_2, \ldots, C_k
\text{ hold.}
\]

The authors’ insight is often:

\[
\exists C_j
\quad
\text{such that}
\quad
C_j \text{ is unrealistic in the target setting.}
\]

Then the paper asks:

\[
\text{Can we retain the benefits of the old paradigm without } C_j?
\]

In the report, write this as:

> The authors likely started from the observation that prior work in \(A\) is attractive because it solves \(P\), but most methods assume \(C\). In the target setting \(T\), \(C\) is either unavailable, expensive, unsafe, or unrealistic. This creates a gap: how can one preserve the advantage of \(A\) while replacing \(C\) with a feasible proxy?

## 2.3 Look for the “Almost Works, But Not Quite” Method

A good research direction often comes from a method family that almost transfers.

Formula:

\[
M_{\text{source}}
\rightarrow
M_{\text{target}}
\quad
\text{fails because}
\quad
R_{\text{source}} \not\subseteq R_{\text{target}}
\]

Where:

- \(M_{\text{source}}\): method family that works in a source setting;
- \(M_{\text{target}}\): desired target setting;
- \(R_{\text{source}}\): requirements of the method;
- \(R_{\text{target}}\): resources allowed in the target setting.

Ask:

- What method from a neighboring field is being imported?
- What assumption prevents direct import?
- What local mechanism replaces the missing assumption?

Then write:

> The paper’s direction can be read as a transfer problem. The authors borrow \(M\) from a setting where resource \(Y\) exists. But in the target setting, \(Y\) is prohibited or absent. The paper’s main idea is therefore to construct \(Z\), a surrogate for \(Y\), using only resources allowed in the target setting.

## 2.4 Infer the Inspiration Source

Authors often draw inspiration from 3 layers:

\[
\text{Inspiration}
=
\text{Problem Pressure}
+
\text{Method Analogy}
+
\text{System Constraint}
\]

For each major contribution, ask:

| Question | What to infer |
|---|---|
| What failure did the authors repeatedly emphasize? | Problem pressure |
| What prior method is structurally similar? | Method analogy |
| What is disallowed in the setting? | System constraint |
| What replacement signal is available? | Design source |
| What did the authors make consensus over? | Story core |

A good report should explicitly state:

> The likely inspiration was not simply “use method \(M\),” but “method \(M\) normally depends on \(Y\); since \(Y\) is unavailable, create \(Z\) that plays the same functional role.”

---

# 3. How the Authors Built the Story

This section explains the narrative construction of the paper.

A paper’s story usually follows this pattern:

\[
\text{Story}
=
\text{Problem Importance}
+
\text{Prior Success}
+
\text{Unrealistic Assumption}
+
\text{New Setting}
+
\text{Specific Failure Modes}
+
\text{Mechanisms}
+
\text{Evidence}
\]

## 3.1 The Gap-to-Mechanism Bridge

The best papers do not present modules as arbitrary engineering. Each module answers one named failure.

Use this mapping:

\[
\text{Challenge}_i
\rightarrow
\text{Failure Mode}_i
\rightarrow
\text{Design Principle}_i
\rightarrow
\text{Module}_i
\rightarrow
\text{Ablation}_i
\]

A strong report should reconstruct this table.

| Story element | Reading question |
|---|---|
| Challenge | What breaks in the new setting? |
| Failure mode | Why do existing methods fail? |
| Design principle | What kind of signal could repair it? |
| Module | What mechanism implements that signal? |
| Ablation | What experiment proves this module was needed? |

If a paper has three modules, look for a “three-challenge, three-mechanism, three-ablation” structure:

\[
(C_1, C_2, C_3)
\rightarrow
(M_1, M_2, M_3)
\rightarrow
(A_1, A_2, A_3)
\]

This structure makes the paper easy to defend.

## 3.2 The Narrative Escalation Pattern

Many good papers escalate the problem in stages.

Template:

1. **Base setting is important.**
2. **But the standard assumption fails.**
3. **A known solution family seems relevant.**
4. **But it fails under the new constraints.**
5. **This creates several concrete sub-problems.**
6. **Each sub-problem motivates one module.**
7. **The modules form a closed loop.**
8. **Experiments validate the full loop and each part.**

In formula form:

\[
P
\rightarrow
A_{\text{old}}
\rightarrow
\neg C
\rightarrow
M_{\text{candidate}}
\rightarrow
\neg R
\rightarrow
\{F_i\}_{i=1}^{k}
\rightarrow
\{Z_i\}_{i=1}^{k}
\rightarrow
\text{Empirical Closure}
\]

Where:

- \(P\): important problem;
- \(A_{\text{old}}\): existing paradigm;
- \(\neg C\): broken assumption;
- \(M_{\text{candidate}}\): tempting method family;
- \(\neg R\): missing resource or violated requirement;
- \(F_i\): failure modes;
- \(Z_i\): proposed modules.

## 3.3 Closed-Loop Story Design

The strongest method stories are not a list of modules. They are loops.

A weak story looks like:

\[
M_1 + M_2 + M_3
\]

A strong story looks like:

\[
M_1 \Rightarrow M_2 \Rightarrow M_3 \Rightarrow M_1
\]

or:

\[
\text{Signal}
\rightarrow
\text{Data}
\rightarrow
\text{Model}
\rightarrow
\text{Better Signal}
\]

When reading, ask:

- Does Module 1 produce something Module 2 needs?
- Does Module 2 create a resource Module 3 uses?
- Does Module 3 improve the condition under which Module 1 works?
- Is there a conceptual object that flows through all modules?

Common flowing objects:

| Flowing object | Typical story |
|---|---|
| pseudo-label | confidence improves training |
| generated data | data improves validation or augmentation |
| graph consensus | neighbors improve local estimates |
| uncertainty | filtering improves reliability |
| prototypes | shared representation without raw data |
| rewards | policy improves data collection |
| memory | past experience stabilizes current learning |

Write the story as:

> The paper is not merely stacking modules. It constructs a loop: \(M_1\) creates \(S\), \(M_2\) improves or expands \(S\), and \(M_3\) uses \(S\) to make the global system more reliable. This makes the contribution feel coherent rather than additive.

---

# 4. Method Deep Reading: The Author-Thinking Behind Each Module

This is the heart of an author-perspective report.

For every method module, reconstruct the likely thought process using the following template.

## 4.1 Module Reading Template

For module \(M_i\), answer:

\[
M_i =
\text{Failure}
+
\text{Unavailable Ideal Solution}
+
\text{Available Proxy}
+
\text{Design Choice}
+
\text{Assumption}
+
\text{Risk}
\]

Expanded:

1. **Failure being fixed**  
   What would go wrong without this module?

2. **Ideal but unavailable solution**  
   What would solve the problem if constraints did not exist?

3. **Available proxy**  
   What signal/resource is still allowed?

4. **Design choice**  
   How does the module turn that proxy into a usable mechanism?

5. **Assumption**  
   Under what condition does this module work?

6. **Risk or failure case**  
   When might the module fail?

7. **Evidence**  
   What ablation or analysis should prove it matters?

## 4.2 Functional Role Formula

Do not describe a module only by its operations. Describe its functional role.

\[
\text{Module}
=
\text{Operation}
\quad
\text{serving the role of}
\quad
\text{Missing Mechanism}
\]

Examples:

| Operation | Functional role |
|---|---|
| neighbor averaging | replaces central aggregation |
| pseudo-labeling | replaces missing labels |
| data augmentation | replaces data diversity |
| synthetic validation | replaces shared validation set |
| confidence threshold | replaces oracle correctness check |
| clustering | replaces known client groups |
| uncertainty estimation | replaces ground-truth reliability |
| contrastive alignment | replaces paired modalities |
| distillation | replaces direct data sharing |

The report should say:

> This module should be read not as a technical trick, but as a surrogate for \(Y\), the mechanism that would have been available in an easier version of the problem.

## 4.3 Reverse-Engineering the Design Choice

For each design choice, ask:

\[
\text{Why this design rather than the simplest baseline?}
\]

A useful ladder:

1. **Naive local solution**  
   What is the simplest local-only method?

2. **Why it fails**  
   What bias, variance, instability, privacy issue, or compute issue appears?

3. **First improvement**  
   What extra signal can reduce the failure?

4. **Why the improvement is still insufficient**  
   Does it create imbalance, noise, cost, or new assumptions?

5. **Final design**  
   What extra correction makes the method robust enough?

This often reveals the authors’ actual design logic:

\[
\text{Naive}
\rightarrow
\text{Failure}
\rightarrow
\text{Borrowed Fix}
\rightarrow
\text{Constraint Violation}
\rightarrow
\text{Adapted Fix}
\]

## 4.4 Find the Hidden “Equivalent Ideal”

Most modules approximate an ideal object that is unavailable.

Use this question:

> If the authors had unlimited access, what would they use instead?

Then map:

\[
\text{Unavailable Ideal } I
\approx
\text{Constructed Proxy } \hat{I}
\]

Examples:

| Unavailable ideal \(I\) | Constructed proxy \(\hat{I}\) |
|---|---|
| true labels | pseudo-labels |
| global data distribution | generated data distribution |
| central validation set | synthetic validation set |
| oracle client reliability | performance on proxy data |
| true domain alignment | feature-level agreement |
| full gradients | compressed gradients |
| trusted server | consensus protocol |
| clean dataset | robust filtering |

In the report, state:

> The module makes sense once we see it as an approximation of \(I\). Its novelty is not merely in computing \(\hat{I}\), but in computing \(\hat{I}\) under the constraints of the paper’s target setting.

## 4.5 Identify the Module’s Fragile Assumption

Every clever module has a hidden bet.

Formula:

\[
M_i \text{ works if } H_i \text{ holds.}
\]

Examples:

- pseudo-labeling works if confidence correlates with correctness;
- neighbor consensus works if neighbors provide complementary rather than adversarial signals;
- synthetic data works if the generator covers the relevant distribution;
- adaptive aggregation works if proxy validation performance correlates with real performance;
- contrastive alignment works if positives are semantically aligned;
- personalization works if client-specific structure is stable.

A strong report should include:

> The module’s hidden assumption is \(H_i\). This is also a natural future research point, because if \(H_i\) fails, the paper’s mechanism may break.

This turns method reading into research generation.

---

# 5. Why Key Citations Appear: Reverse Citation Logic

Do not treat citations as a bibliography list. Treat them as narrative functions.

A citation usually appears because it gives the authors permission to make one of the following moves:

\[
\text{Citation}
\Rightarrow
\text{Narrative Permission}
\]

## 5.1 Citation Function Taxonomy

| Citation type | Function in the story | What to write in the report |
|---|---|---|
| Foundational paradigm | Establishes the field and importance | “This citation anchors the paper in \(A\).” |
| Limitation paper | Shows known weakness or gap | “This supports the claim that \(A\) struggles under \(T\).” |
| Method ancestor | Provides a tool later adapted | “This is the technical ancestor of module \(M_i\).” |
| Neighboring-field solution | Shows transfer inspiration | “The authors borrow the logic of \(M\), but remove its reliance on \(Y\).” |
| Strong baseline | Raises comparison pressure | “This baseline defines what the new method must beat.” |
| Benchmark protocol | Legitimizes experimental setup | “This citation justifies dataset split, non-IID construction, metric, or architecture.” |
| Implementation detail | Provides technical machinery | “This citation enables the practical realization of a submodule.” |
| Negative contrast | Shows what prior work cannot handle | “This citation is used to draw the boundary of the new contribution.” |

## 5.2 Citation Reverse-Engineering Formula

For each important cited work \(W\), infer:

\[
W
\rightarrow
\{\text{Problem}, \text{Tool}, \text{Assumption}, \text{Limitation}, \text{Borrowed Element}\}
\]

Then write:

\[
\text{Authors cite } W
\text{ not merely because } W \text{ is related,}
\text{ but because } W \text{ supplies } X
\text{ while leaving gap } G.
\]

Example phrasing:

> This citation functions as a method ancestor. The paper inherits the idea of \(X\), but the target setting lacks \(Y\), so the authors redesign \(X\) into \(X'\).

or:

> This citation functions as a contrastive boundary. It shows that prior work can solve the problem when \(C\) holds, which helps the authors justify why their setting, where \(C\) does not hold, deserves a new method.

## 5.3 Build a Citation-to-Module Map

For the report, create a table:

| Citation cluster | What it contributes | What assumption it carries | How this paper modifies it |
|---|---|---|---|
| Field foundation | Importance of \(P\) | Usually assumes \(C\) | Paper removes \(C\) |
| Method family | Tool \(M\) | Requires \(Y\) | Paper replaces \(Y\) with \(Z\) |
| Closest prior work | Baseline solution | Does not handle \(T\) | Paper adapts to \(T\) |
| Technical machinery | Algorithmic component | Works in original setting | Paper embeds it into new system |
| Experimental precedent | Protocol or metric | Benchmark convention | Paper follows or extends it |

This is especially useful for explaining why some references are “key” while others are background.

## 5.4 Detect the Citation Storyline

A paper’s related work often secretly says:

\[
\text{People solved } P \text{ under } C_1;
\quad
\text{others solved } P \text{ under } C_2;
\quad
\text{but nobody solved } P \text{ under } \neg C_1 \cap \neg C_2.
\]

This creates the opening for the paper.

Write this as:

> The related work is not just listing fields. It constructs a coordinate system. One axis is \(A\), another is \(T\), and the paper positions itself in the empty cell where both constraints must be handled simultaneously.

---

# 6. Experiments as Story Evidence

Experiments should be read as narrative proof.

A useful formula:

\[
\text{Experiment}
=
\text{Claim}
+
\text{Counterfactual}
+
\text{Metric}
+
\text{Stress Condition}
\]

For each experiment, ask:

1. What claim does this experiment support?
2. What alternative explanation does it rule out?
3. What stress condition makes the result meaningful?
4. Which module does it justify?
5. Does the ablation align with the method story?

## 6.1 Main Result

Main results usually answer:

\[
\text{Does the complete system outperform prior solutions under the target setting?}
\]

Look for:

- low-resource regimes;
- high heterogeneity;
- distribution shift;
- privacy constraints;
- adversarial or noisy conditions;
- scalability.

## 6.2 Ablation

Ablation should map back to modules:

\[
M_i \text{ removed}
\Rightarrow
\text{performance drop}
\Rightarrow
\text{module necessity}
\]

A strong report should say whether the ablation truly proves the module’s narrative role.

## 6.3 Stress Tests

Stress tests show whether the paper’s central idea survives when the target difficulty increases.

Examples:

- fewer labels;
- stronger non-IID;
- fewer clients;
- weaker graph connectivity;
- noisier labels;
- worse generator;
- lower compute;
- malicious clients;
- domain shift.

Use this reading:

\[
\text{If the paper claims to solve } T,
\text{ then experiments should vary the intensity of } T.
\]

---

# 7. What Story-Making Pattern Is Worth Learning

This section should extract a reusable storytelling template from the paper.

The goal is to teach the reader how to build future papers.

## 7.1 General Story Template

A strong research story can often be expressed as:

\[
\boxed{
\text{Old Success}
+
\text{New Reality}
\Rightarrow
\text{Old Assumption Breaks}
\Rightarrow
\text{Known Tool Almost Works}
\Rightarrow
\text{Constraint Blocks Direct Use}
\Rightarrow
\text{New Surrogate Mechanism}
}
\]

More concretely:

\[
\boxed{
A \text{ solves } P \text{ when } C \text{ holds;}
\quad
T \text{ makes } C \text{ invalid;}
\quad
M \text{ can address } \neg C \text{ but requires } Y;
\quad
Y \notin T;
\quad
\text{therefore we design } Z \approx Y.
}
\]

This is one of the most useful formulas for generating new research ideas.

## 7.2 Three-Module Story Template

Many system or algorithm papers can be built as:

\[
\boxed{
F_1 \rightarrow M_1,\quad
F_2 \rightarrow M_2,\quad
F_3 \rightarrow M_3
}
\]

Where:

- \(F_1\): signal reliability failure;
- \(F_2\): data or representation insufficiency;
- \(F_3\): coordination, selection, or optimization failure.

Then:

\[
M_1 \text{ repairs signal}
\]
\[
M_2 \text{ expands information}
\]
\[
M_3 \text{ coordinates the system}
\]

A particularly elegant story is:

\[
M_1 \Rightarrow M_2 \Rightarrow M_3
\]

rather than:

\[
M_1 + M_2 + M_3.
\]

In prose:

> The first module creates a usable signal. The second module enriches or stabilizes that signal. The third module uses the improved signal to coordinate the whole system.

## 7.3 Replacement Story Template

Another powerful pattern is the replacement story:

\[
\text{In easy setting: }
Y \text{ is available.}
\]
\[
\text{In hard setting: }
Y \text{ is unavailable.}
\]
\[
\text{Our idea: }
Z \text{ plays the role of } Y \text{ without violating constraints.}
\]

Examples:

| Easy-setting resource \(Y\) | Hard-setting replacement \(Z\) |
|---|---|
| labels | pseudo-labels |
| server | peer consensus |
| public dataset | generated data |
| validation set | proxy validation |
| oracle confidence | calibrated uncertainty |
| clean clients | robust reputation |
| full communication | sparse communication |
| paired data | contrastive alignment |

This is often the deepest “paper-making” logic.

## 7.4 Two-Axis Empty Cell Template

Position the paper as filling an empty cell:

\[
\text{Axis 1: Problem condition}
\]
\[
\text{Axis 2: System constraint}
\]

Create a table:

|  | Easy system | Hard system |
|---|---|---|
| Easy data | solved | partly solved |
| Hard data | partly solved | **your paper** |

The story becomes:

> Prior work solves each difficulty separately, but the intersection remains underexplored.

Formula:

\[
\text{Contribution}
=
\text{Difficulty}_1
\cap
\text{Difficulty}_2
\cap
\cdots
\cap
\text{Difficulty}_k
\]

This is especially useful for papers combining:

- privacy + low labels;
- decentralization + non-IID;
- robustness + personalization;
- multimodality + missing data;
- long context + low latency;
- safety + autonomy;
- fairness + distribution shift.

## 7.5 Closed-Loop Contribution Template

The most memorable papers often create a loop:

\[
\boxed{
\text{Noisy Signal}
\rightarrow
\text{Proxy Resource}
\rightarrow
\text{Better Coordination}
\rightarrow
\text{Cleaner Signal}
}
\]

or:

\[
\boxed{
\text{Weak Supervision}
\rightarrow
\text{Representation Improvement}
\rightarrow
\text{Reliability Estimation}
\rightarrow
\text{Better Weak Supervision}
}
\]

When writing the report, identify the loop and state:

> The paper’s contribution is not a bag of tricks. It constructs a feedback loop in which the output of one module becomes the missing resource required by the next module.

## 7.6 Boundary-Pushing Template

Convert hidden assumptions into future research.

For each module:

\[
M_i \text{ works if } H_i.
\]

Then future work is:

\[
\text{New Research Direction}
=
\text{Make } M_i \text{ work when } \neg H_i.
\]

Examples:

| Current hidden assumption \(H_i\) | Future direction \(\neg H_i\) |
|---|---|
| neighbors are helpful | malicious or untrusted neighbors |
| confidence is calibrated | overconfident wrong predictions |
| generator covers distribution | biased or low-quality generator |
| proxy metric matches true metric | proxy-real mismatch |
| graph is fixed | learnable or dynamic topology |
| clients share label space | partial or open-set labels |
| data is stationary | temporal drift |
| compute is sufficient | resource-constrained deployment |

This is one of the best ways to turn a reading report into a research proposal.

---

# 8. Weakness and Breakthrough Analysis

A good report should not only praise the paper. It should expose the scientific frontier.

Use the following formula:

\[
\text{Weakness}
=
\text{Claim}
-
\text{Evidence}
+
\text{Hidden Assumption}
\]

For each key claim, ask:

1. What evidence supports it?
2. What evidence is missing?
3. What assumption is required?
4. What happens if the assumption fails?
5. Can that failure become a new paper?

## 8.1 Common Weakness Categories

| Category | Questions |
|---|---|
| Theory | Is there convergence, risk, bias, or generalization analysis? |
| Scalability | Does the method scale to larger data, models, clients, or modalities? |
| Robustness | What if clients are noisy, malicious, or unreliable? |
| Privacy | Does the method leak through gradients, models, synthetic data, or statistics? |
| Compute | Is the method realistic for edge devices? |
| Evaluation | Are benchmarks too simple or too clean? |
| Proxy mismatch | Does the proxy signal really match the target objective? |
| Ablation depth | Do ablations isolate mechanisms or only show performance differences? |
| Assumption realism | Are clients, labels, topology, or distributions realistic? |

## 8.2 Convert Weaknesses into Research Directions

Use:

\[
\text{Future Work}
=
\text{Current Method}
+
\text{Violated Assumption}
+
\text{New Mechanism}
\]

Example phrasing:

> The paper assumes \(H\). A natural next step is to study the setting where \(H\) fails. This would require replacing \(M\)'s reliance on \(H\) with a more robust mechanism such as \(Z\).

---

# 9. Writing Style for the Report

The report should sound like a research mentor explaining how the paper was probably invented.

Use phrases such as:

- “A plausible author-side thinking path is...”
- “This module is best understood as a surrogate for...”
- “The citation is not ornamental; it plays the role of...”
- “The story can be compressed into the formula...”
- “The hidden bet of this module is...”
- “This weakness can be converted into a new research question...”
- “The paper’s deepest lesson is not the specific technique, but the replacement pattern...”

Avoid:

- simply listing sections;
- repeating the abstract;
- describing equations without explaining why they were needed;
- treating citations as background only;
- giving future work that is too generic;
- claiming to know the authors’ private thoughts with certainty.

---

# 10. Final Report Skeleton

Use this skeleton when producing the final answer.

```markdown
# Paper Deep Reading Report

## 1. One-Sentence Thesis

This paper can be read as solving:

\[
A \text{ works under } C,\quad
T \text{ breaks } C,\quad
M \text{ almost helps but requires } Y,\quad
\text{so the paper designs } Z.
\]

## 2. How the Authors May Have Found This Direction

### 2.1 The likely starting dissatisfaction
...

### 2.2 The transfer that almost worked
...

### 2.3 The unavailable mechanism
...

### 2.4 The replacement mechanism
...

### 2.5 Research-direction formula
\[
\text{Direction} =
\text{Popular paradigm}
+
\text{Broken assumption}
+
\text{Hard setting}
+
\text{Surrogate mechanism}
\]

## 3. How the Authors Built the Story

### 3.1 Challenge-to-module map

| Challenge | Failure mode | Design principle | Module | Evidence |
|---|---|---|---|---|

### 3.2 Narrative escalation
...

### 3.3 Closed-loop story
...

## 4. Method Deep Reading

For each module:

### Module \(M_i\)

| Lens | Interpretation |
|---|---|
| Failure fixed | ... |
| Ideal unavailable solution | ... |
| Available proxy | ... |
| Design choice | ... |
| Hidden assumption | ... |
| Possible failure | ... |
| Future research point | ... |

## 5. Why the Key Citations Appear

| Citation cluster | Narrative function | Assumption inherited | How the paper modifies it |
|---|---|---|---|

## 6. Experiments as Story Evidence

...

## 7. Story-Making Pattern Worth Learning

\[
A \text{ solves } P \text{ when } C;
\quad
T \Rightarrow \neg C;
\quad
M \text{ helps but requires } Y;
\quad
Y \notin T;
\quad
Z \approx Y.
\]

...

## 8. Weaknesses and Boundary-Pushing Directions

| Hidden assumption | Why it matters | New research direction |
|---|---|---|

## 9. Final Evaluation

...
```

---

# 11. Quality Checklist

Before finalizing the report, check:

- Did I explain how the authors may have discovered the direction?
- Did I identify the broken assumption?
- Did I identify the unavailable ideal mechanism?
- Did I explain the replacement mechanism?
- Did I map every major module to a concrete failure mode?
- Did I explain why key citations appear?
- Did I extract a reusable story-making formula?
- Did I convert hidden assumptions into future research ideas?
- Did I avoid claiming certainty about private author intentions?
- Did I help the reader generate new research directions?

---

# 12. Compact Mental Model

The entire skill can be compressed into this one line:

\[
\boxed{
\text{Read a paper as: }
\text{What was impossible under the new constraints,}
\text{what surrogate did the authors invent,}
\text{and how did they make that surrogate look inevitable?}
}
\]

A deep report should reveal not only the paper’s contribution, but the **research-making grammar** behind it.

