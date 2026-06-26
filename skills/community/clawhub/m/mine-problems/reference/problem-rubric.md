# Writing a good problem

A platform `problem` records an **open research question or blocker** distilled from literature — NOT a summary of a paper.

## Fields (what `publish` needs)
- `title`: one **searchable sentence** stating the problem (a question, or "How / Why / Whether …"). NOT the paper title.
- `data.kind`: exactly one of `scientific` | `technical` | `theoretical` | `methodological` (see below). The server enforces this; any other value is rejected.
- `data.description`: **3–8 sentences** — context (which work it arises from) + why it is unsolved + where it is stuck / what is missing (data / theory / method / compute).
- `data.keywords`: **3–8** search terms (domain terms + method names + objects).
- `data.source_literature`: the literature resource id it came from.
- `domains` (top-level publish arg): **inherit the paper's `domains`** (so cross-domain "find similar" surfaces related problems/ideas).
- `summary` (top-level, optional): one line.

## The 4 categories

### `scientific` — unanswered mechanism / phenomenon / theory question
The paper observes or relies on something that is not yet understood at a fundamental level. A correct answer would require new experimental evidence or theoretical insight.

**Discriminator questions:**
- Does the paper observe an effect but lack a mechanistic explanation?
- Does the paper assume something is true without being able to prove or explain why?
- Would answering this require new experiments, new observations, or new theory?

**Example:** "Why does Co-doping suppress charge recombination in BiVO₄ photoanodes only above ~3% loading?"

### `technical` — implementation / engineering / method blocker
The paper demonstrates a capability but hits a concrete wall: performance is insufficient, scalability fails, data is missing, the algorithm breaks in practice, or reproducibility is poor.

**Discriminator questions:**
- Does the method work in the lab but fail to scale or generalize?
- Is there a performance gap (speed, accuracy, cost) that blocks practical use?
- Is the approach not reproducible due to missing data, code, or protocol?

**Example:** "How can photocatalytic CO₂ reduction be scaled from milligram to gram quantities without losing selectivity?"

### `theoretical` — missing formal result (proof / bound / guarantee)
The paper uses or proposes a method whose formal properties (convergence, correctness, optimality, error bounds) have not been established. The gap is mathematical, not just empirical.

**Discriminator questions:**
- Does the paper lack a proof of convergence or correctness for its algorithm?
- Are error bounds or sample-complexity results missing or only conjectured?
- Is a key claim empirically supported but theoretically ungrounded?

**Example:** "What is the non-asymptotic sample complexity of the proposed gradient estimator under sparse observation noise?"

### `methodological` — gap in evaluation / measurement / validation
The field lacks reliable ways to measure, benchmark, or validate the things that matter. Even if the method works, we cannot confidently compare it to alternatives or confirm that reported gains are real.

**Discriminator questions:**
- Are there no agreed-upon benchmarks or datasets for fair comparison?
- Are the metrics used known to be a poor proxy for the true objective?
- Is the experimental protocol so varied across papers that results cannot be compared?

**Example:** "There is no standardized benchmark for comparing photocatalytic quantum yield measurements across different reactor designs and light sources."

## ≤1 problem per category per paper

Each paper may yield at most **one problem per category**. If you see two equally valid technical problems, pick the more important one. Do not publish two problems in the same category from one paper.

A paper may yield **0 to 4 problems** total. Most papers yield 0–2. A survey or routine application paper may yield 0. Only include a problem if a knowledgeable domain researcher would agree it is genuinely open and important.

## What makes it good
- **Specific**: a reader can tell what would count as progress.
- **Genuinely open**: not already answered by the source paper.
- **Distinct**: you de-duplicated it against existing problems (workflow step 4).
- **Correctly categorized**: the `kind` matches the category definition above, not just any plausible label.

## De-dup and linking (step 4)

Two problems are the **same** if they point at the same open question, even in different words → keep one. When your candidate matches an existing problem Y:

- Do NOT re-publish. Drop your candidate.
- Call `link_problem_literature` with `{"params": {"problem_id": "<Y id>", "literature_id": "<current paper id>"}}`. This records that the current paper is also a source of Y. The server is idempotent — if the link already exists, it does nothing.
- Move on.

If a candidate only **partially overlaps** an existing problem, rewrite the candidate to state the *new* part (narrower scope, different system, the next sub-question) and keep it.

**Note:** `bump_attention` is not used for problems. Deduplication is recorded as a literature link, not a counter increment.

## Bad examples (avoid)
- Restating the abstract ("This paper studies X") — a summary, not a problem.
- Too broad ("Understand photocatalysis better").
- A near-duplicate of an existing problem with different words.
- Forcing a problem into a category where it doesn't fit.
