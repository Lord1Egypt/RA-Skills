---
name: prompt_design_tuning_best_practice
description: Collaboratively design, evaluate, iterate on, and recommend a final launch candidate for a target prompt under the principle of “human-gated, agent-executed” workflow.
---

# Prompt Design & Tuning Best Practices

The goal of this Skill is not to casually “chat about prompts,” but to turn prompt tuning into an **executable, reviewable, and cost-controlled** engineering workflow.

The Agent handles most of the execution work.  
Humans are responsible only for validating direction, approving high-cost loops, and signing off on the final launch candidate.

---

## When to Use

Use this Skill when the user needs to:

- design or optimize a target prompt from scratch
- design a separate evaluation / judge prompt
- compare the performance of multiple models on an evaluation set
- work with an existing API curl, SDK integration, or request protocol
- run controlled prompt iterations under a limited budget
- turn prompt tuning into a reusable workflow instead of a one-off chat exercise

---

## Working Modes

### 1. Design-Only Mode

Use this mode when:

- there is no runnable environment yet
- no evaluation resources are available yet
- real model calls cannot be executed for now

In this mode, the Agent should produce:

- task definition
- target prompt draft
- judge prompt draft
- evaluation plan
- script skeletons
- manual execution guidance

### 2. Execution Mode

Use this mode when:

- a runnable environment already exists
- the model invocation method has been provided
- the evaluation set, resource limits, and candidate models have been provided

In this mode, the Agent should continue with:

- batch generation
- automatic evaluation
- result analysis
- prompt iteration
- final candidate recommendation

---

## Core Principles

The following rules are non-negotiable by default:

1. The **target prompt** and the **judge prompt** must be separated.  
   Do not silently modify both in the same comparison round and then mix their gains together.

2. Before large-scale evaluation, the **task definition (task spec)** must be frozen first.

3. Every round of prompt optimization must have a clear **optimization hypothesis**.  
   No random “this sentence feels off, let’s tweak it” behavior.

4. An **experiment log** must be maintained, including at least:
   - version number
   - summary of changes in the current round
   - optimization hypothesis
   - evaluation results
   - cost information
   - conclusion

5. Any high-cost evaluation loop must be approved by a human beforehand.

6. The final launch candidate must be reviewed by a human.  
   A high machine-evaluation score does not automatically mean it is ready for launch.

7. If the input information is incomplete, low-risk assumptions may be made, but they must be stated explicitly.

---

## Recommended Inputs to Collect

The Agent should gather or infer the following whenever possible:

- business goal
- user scenario
- input format
- output format
- hard constraints
- unacceptable errors
- success criteria
- online acceptance threshold
- evaluation set
- candidate models
- invocation method (curl / SDK / API)
- resource limits (TPM, RPM, timeout, budget, retry cap)

---

## Target Deliverables

By default, the workflow should aim to produce the following:

- `docs/task_spec.md`
- `prompts/production_prompt_v{n}.md`
- `prompts/judge_prompt_v{n}.md`
- `docs/eval_plan.md`
- `scripts/run_generation.py`
- `scripts/run_judge.py`
- `reports/iteration_{n}_summary.md`
- `reports/final_recommendation.md`
- `reports/experiment_log.md`

---

## Human Gates

By default, human confirmation is required only at the following key checkpoints:

### Gate A — Freeze the Task Definition
Confirm:
- whether the task is understood correctly
- whether the success criteria are reasonable
- whether the constraints are complete

### Gate B — Confirm the Direction of the Target Prompt
Confirm:
- whether the target prompt is directionally correct
- whether it is ready to enter evaluation

### Gate C — Confirm the Direction of the Judge Prompt
Confirm:
- whether the evaluation standard is fair
- whether the judge is evaluating what actually matters

### Gate D — Approve a High-Cost Iteration Loop
Confirm:
- model list
- TPM budget
- number of iteration rounds
- whether it is worth spending more resources

### Gate E — Final Review
Confirm:
- whether the current best version can serve as a launch candidate
- whether to continue optimizing
- whether to stop

Unless the user explicitly asks for finer-grained control, do not interrupt too frequently in the middle.

---

# Execution Flow

## Phase 0 — Task Definition (Task Spec)

Before writing any prompt, first establish a clear task definition.

The task definition should include at least:

- problem description
- input format
- output format
- business goal
- user goal
- constraints
- explicitly forbidden outputs
- positive and negative examples
- success metrics
- unresolved issues
- current assumptions

If the user’s description is incomplete, do not stall.  
Fill in reasonable assumptions first, then present them for confirmation.

After this, proceed to **Gate A**.

---

## Phase 1 — Generate the First Draft of the Target Prompt

Based on the task definition, produce the first draft of the target prompt.

Requirements:

- instructions must be clear
- constraints must be explicit
- output structure must be stable
- ambiguity should be minimized
- controllability should be prioritized over fluffy “stylistic” wording
- examples should be included only when they are truly helpful

Also output:

- key design rationale
- predicted risk points
- likely failure scenarios
- what to pay close attention to in the first evaluation round

After this, proceed to **Gate B**.

---

## Phase 2 — Generate the First Draft of the Judge Prompt

Design an independent Judge / Eval Prompt.

Requirements:

- evaluate the task outcome, not whether the prompt itself reads nicely
- score across separate dimensions, then aggregate
- include hard-fail categories
- output must be structured JSON
- minimize bias caused by stylistic model preferences
- explicitly handle the following cases:
  - partially correct outputs
  - format errors
  - misunderstanding of the task
  - unsafe or policy-violating content
  - reasonable uncertainty caused by incomplete task information

Also output:

- scoring dimensions
- weight design
- hard-fail conditions
- Judge output JSON schema
- Judge blind spots

After this, proceed to **Gate C**.

---

## Phase 3 — Design the Evaluation Plan

Before running large-scale evaluations, define the evaluation plan clearly.

The plan should include at least:

- source and size of the evaluation set
- sample slicing strategy (easy / medium / hard / edge cases)
- online acceptance threshold
- primary metrics
- secondary diagnostic metrics
- tie-breaking rules
- maximum number of iteration rounds
- total budget limit
- early stopping conditions

Default loop policy:

- by default, run at most **2 high-cost optimization rounds**
- stop if the gains are marginal and the failure types have not improved in substance
- if the Judge itself looks unreliable, fix the Judge first instead of continuing to modify the target prompt

---

## Phase 4 — Write the Generation Script

If executable conditions are available, the Agent should write a batch generation script.

The script should support, as much as possible:

- jsonl / csv / excel input
- multiple models
- resume from checkpoint
- retries and backoff
- logging
- strict input-output order preservation
- TPM / RPM rate limiting
- structured outputs for downstream evaluation

### TPM Handling Principles

Do not crudely translate TPM directly into high concurrency.

Preferred approach:

- estimate token consumption per request
- use token-bucket or time-window rate limiting
- use conservative concurrency when RPM and latency are unknown
- prioritize stability before speed

---

## Phase 5 — Batch Generate Model Outputs

Run the full evaluation set across all specified models and prompt versions.

At minimum, record:

- model name
- prompt version
- input sample ID
- raw output
- token usage (if available)
- latency
- retry count
- request failure information
- truncation / parsing failures

If generation failures occur frequently:

- first separate infrastructure issues from prompt issues
- do not conclude that the prompt is bad before ruling out quota, network, rate-limiting, or protocol problems

---

## Phase 6 — Run Automatic Evaluation

Use the Judge Prompt to evaluate generated outputs in batch.

Requirements:

- Judge output must be structured JSON
- raw judge outputs must be traceable
- compute overall scores and slice-level metrics
- automatically identify major failure clusters
- distinguish format errors from content errors
- if the Judge is noisy, state that explicitly instead of pretending the results are reliable

---

## Phase 7 — Analyze and Optimize

A new prompt iteration is allowed only when there is a clear optimization hypothesis.

Each round must include:

1. summarize the previous round’s results
2. identify the major failure clusters
3. propose the optimization hypothesis for this round
4. modify only the most necessary prompt sections
5. provide a version-diff summary
6. predict what should improve and what may regress

Do not run another round for no reason.

If the next round will consume meaningful resources, go to **Gate D** first.

---

## Phase 8 — Final Recommendation

Once a version reaches a sufficiently strong level, the Agent should produce a final review package.

It should include at least:

- final target prompt
- final judge prompt
- recommended model
- overall metrics
- slice-level metrics
- major remaining failure types
- cost / latency notes
- whether launch is recommended
- what should be monitored after launch

After this, proceed to **Gate E**.

---

# Default Outputs at Each Gate

## Gate A Output

- task definition document
- current assumptions
- missing information
- recommended acceptance criteria

## Gate B Output

- target prompt v1
- design rationale
- expected risks

## Gate C Output

- judge prompt v1
- scoring rubric
- JSON schema
- Judge blind spots

## Gate D Output

- current result comparison
- failure analysis
- prompt change summary
- next-round optimization hypothesis
- estimated resource consumption

## Gate E Output

- final candidate
- why it is the current best version
- where it may still fail
- recommendation to launch / continue optimizing / stop

---

# Default Analysis Templates

## Experiment Log Fields

Each experiment round should record at least:

- iteration
- production_prompt_version
- judge_prompt_version
- model
- dataset_version
- hypothesis
- change_summary
- aggregate_score
- slice_scores
- dominant_failures
- cost
- verdict

## Suggested Failure Taxonomy

The Agent should try to classify failures into one of the following:

- task misunderstanding
- missing constraints
- extraction error
- reasoning error
- incomplete coverage
- unsafe / policy-violating output
- format / schema error
- verbose / redundant output
- hallucinated details
- mismatch between Judge and actual task goal
- infrastructure failure

---

# Explicitly Forbidden Anti-Patterns

Do not do the following:

- modify both the target prompt and the judge prompt in the same round without saying so
- look only at aggregate score and ignore the failure distribution
- overfit to a tiny evaluation set without warning about the risk
- use machine evaluation as a substitute for final human review
- loop endlessly because the score moved slightly
- rewrite the whole prompt when only one part is broken
- hide critical assumptions
- declare success without showing hard examples

---

# Default Behavior When the Skill Is Triggered

When this Skill is triggered, the Agent should follow this order:

1. build or refresh the task definition
2. determine which phase the workflow is currently in
3. prioritize filling missing artifacts before rewriting existing ones
4. prefer incremental optimization over full rewrites
5. request confirmation only at the defined human gates
6. after each major step, output a concise decision memo including:
   - what changed
   - why it changed
   - which metrics improved
   - what major issues remain
   - whether another round is worth it

---

# Example Trigger Phrases

The following requests are suitable triggers for this Skill:

- “Help me automate this prompt tuning workflow”
- “Write the target prompt first, then the judge prompt, then design the evaluation”
- “Use the evaluation set and several models to find the current best prompt”
- “Run 1 to 2 prompt iteration rounds under a controlled budget”
- “Turn this prompt tuning process into a reusable agent skill”
- “Let the agent drive the process, and keep humans only at key checkpoints”