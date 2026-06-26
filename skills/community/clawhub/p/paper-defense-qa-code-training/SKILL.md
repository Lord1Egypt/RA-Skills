---
name: paper-defense-qa-code-training
description: Prepare evidence-grounded computer science paper defense Q&A, code/training audit, reviewer-style attack surfaces, mock-defense scripts, backup-slide plans, and illustrated Q&A storyboard / image-prompt packs. Use when users need paper-specific thesis, lab, conference, rebuttal, or interview defense preparation, including code and training-process grilling plus ChatGPT/Codex image-generation prompts for visual explanations.
version: 1.1.0
metadata:
  openclaw:
    emoji: "🛡️"
---

# Paper Defense Q&A + Code/Training Audit Skill

Use this skill when the user wants to prepare for a paper defense, thesis defense, lab-meeting Q&A, conference rebuttal discussion, advisor grilling, reviewer-style mock exam, or PPT defense for a computer-science / machine-learning paper.

This skill is designed as a downstream companion to `paper_deep_reading_teaching_explainer_v10`. The v10 skill produces the authoritative deep-reading and teaching report. This skill turns that report, the original paper, and any code / training artifacts into a defense-ready attack map and answer bank.

The central output is not a generic FAQ. It is a paper-specific and code-specific defense pack that asks:

```text
What will a skeptical committee, reviewer, peer, or engineer ask about this exact paper?
What evidence from the paper / code / logs supports the answer?
What should the speaker say, and what should they avoid overclaiming?
```

## Core mission

For each target paper, produce:

1. a prioritized bank of likely defense questions;
2. evidence-grounded answers;
3. paper-level attack surfaces;
4. code / repository / training-process attack surfaces;
5. backup-slide suggestions;
6. weak-evidence and missing-evidence triage;
7. mock-defense rehearsal scripts;
8. a concise answer playbook the speaker can memorize;
9. a visual Q&A storyboard and image-prompt pack for illustrated defense cards, diagrams, and figure-rich explanations.

The output should help the user answer hard questions without bluffing, over-defending, or hiding limitations.

## Relationship to the v10 deep-reading skill

Read the v10 outputs first when available:

- `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.md`
- `generated/teaching/<paper-slug>/qa_bank_cn.json`
- `generated/teaching/<paper-slug>/slide_blueprint_cn.json`
- `metadata/source_record.json`
- `metadata/project_directory_index.json`
- `metadata/routing_status.json`
- `metadata/delivery_bundle_manifest.json`
- OpenReview review / rebuttal digests if already collected
- figure / visual manifests if already collected

Do not replace the authoritative v10 detailed report. Treat it as the evidence base and build a derivative defense layer.

If the v10 detailed report is unavailable, this skill may still work from the paper PDF and code artifacts, but the output must mark the missing deep-read report as a blocker or reduced-confidence condition.

## Inputs

### Minimum useful input

- the target paper PDF, arXiv page, conference page, or a previously generated v10 detailed report;
- the user's defense context: class presentation, lab meeting, thesis defense, conference rebuttal, proposal defense, advisor meeting, or interview.

### Strong input

- authoritative deep-reading report from v10;
- paper PDF and supplementary material;
- official code repository or submitted anonymized code;
- training scripts, evaluation scripts, configs, logs, checkpoints, hyperparameter sweeps, random seeds, and hardware notes;
- OpenReview reviews, rebuttals, decision, and public discussion when relevant;
- PPT draft or slide blueprint;
- optional style preference for visual explanations, e.g. clean academic infographic, chalkboard explainer, comic-panel metaphor, or PPT-friendly flat illustration.

### Optional defense-context fields

Use or infer:

```json
{
  "defense_context": "thesis_defense | lab_meeting | conference_rebuttal | paper_reading_group | advisor_grilling | job_talk | proposal_defense",
  "target_audience": ["advisor", "committee", "reviewer", "peer", "beginner", "practitioner"],
  "paper_subfield": "e.g. ML systems / CV / NLP / security / theory / databases / HCI",
  "known_weaknesses": [],
  "known_sensitive_points": [],
  "available_time_minutes": 30,
  "expected_qna_minutes": 30,
  "code_available": true,
  "training_artifacts_available": true,
  "risk_tolerance": "conservative"
}
```

## Non-negotiable evidence discipline

Every generated answer must be tagged as one of:

- `paper_grounded`: directly supported by the paper, appendix, supplement, or official review materials;
- `code_grounded`: supported by repository files, configs, logs, scripts, or checkpoints;
- `experiment_log_grounded`: supported by runs, seeds, hardware records, sweep logs, result tables, or failure cases;
- `review_grounded`: supported by public reviewer / rebuttal / meta-review text;
- `inferred`: reasoned from available evidence but not explicitly stated;
- `missing_evidence`: plausible but not supported by current materials;
- `external_context`: supported by official venue guidelines, benchmark docs, dataset docs, or verified external sources.

Do not merge these labels. If an answer depends on inference or missing evidence, say so explicitly.

## Core answer principle

A strong defense answer has this shape:

```text
Claim: what we can defend.
Evidence: where the paper/code/log supports it.
Boundary: what the evidence does not show.
Why it matters: why the design or result is still meaningful.
Follow-up: what test, ablation, or implementation check would resolve the remaining doubt.
```

When the evidence is incomplete, use the balanced-defense template:

```text
The current materials support X through [paper section / figure / table / code / log].
They do not fully establish Y because [missing baseline / missing seed variance / unavailable training log / untested setting].
So the safe answer is: X is supported under [scope], while Y remains a limitation.
A fair follow-up would be [specific experiment or code check].
```

Never answer a hard question by pretending the paper proves more than it does.

## Visual Q&A and image-generation separation rule

This skill may prepare a series of illustrated Q&A cards, storyboard frames, and image prompts, but text answering and image generation must be separated.

Always do the text work first:

1. write the defense question, spoken answer, evidence label, and boundary;
2. then write the visual concept and image prompt;
3. do not generate images in the same response unless the user explicitly asks for image generation as a separate follow-up task.

For ChatGPT web usage, tell the user to open or invoke Create image mode and ask to generate the numbered image prompts from `visual_image_prompt_pack_cn.md`. Prefer ChatGPT Images 2.0 / `gpt-image-2` when available.

For Codex / CLI / agent usage, do not use low-quality local placeholder art for the final visual cards. When running inside Codex, prefer invoking the `imagegen` skill for actual image generation; otherwise use ChatGPT Images 2.0 / `gpt-image-2` through an approved image-generation API, or another user-approved high-quality text-to-image API. Keep the Markdown/JSON answer pack and the image-generation call as separate steps.

When exact equations, code snippets, or tiny labels must be perfectly readable, generate the image as a clean background / metaphor / layout and overlay exact text later in PPT, SVG, HTML, or another deterministic renderer. Use generated text inside the image only when small wording errors would not damage the defense.

At the end of every text-only delivery or textual response produced by this skill, append exactly this follow-up prompt as the final image-generation reminder. Do this after the written answer, while still keeping image generation as a separate follow-up step:

```text
请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。
```

This sentence is a prompt for the next image-generation step, not an instruction to generate images inside the current text-only answer.

## Workflow overview

Run the workflow in eight passes.

### Pass 1: Intake and defense scope

Read the project state and identify:

- target paper identity;
- venue and paper type;
- defense context;
- available artifacts;
- missing artifacts;
- likely audience composition;
- time budget;
- whether code and training artifacts are in scope.

Output a short `Defense Scope` block and a `Blockers / Evidence Gaps` block before generating detailed answers.

### Pass 2: Claim-to-evidence map

Extract every major defensible claim:

- problem claim;
- novelty claim;
- method claim;
- theoretical claim;
- experimental claim;
- efficiency / compute claim;
- reproducibility claim;
- deployment / practical claim;
- limitation claim.

For each claim, record the exact evidence:

```text
Claim -> Evidence -> Strength -> Caveat -> Likely question -> Answer posture
```

### Pass 3: Paper-level attack surface

Generate questions from these axes:

1. **Problem and motivation**: why this problem matters, what breaks in prior work, what assumption changed.
2. **Novelty and positioning**: closest prior work, incremental vs conceptual contribution, why not an obvious combination.
3. **Method mechanism**: data flow, model architecture, losses, optimization, training / inference difference, algorithmic complexity.
4. **Formula and theory**: assumptions, theorem statements, proof gaps, theory-to-implementation mismatch.
5. **Experiment design**: dataset choice, splits, metrics, baselines, ablations, hyperparameters, seeds, variance, significance.
6. **Evidence-to-claim alignment**: what the experiments actually prove versus what the paper claims.
7. **Figures and tables**: how to read them, what they hide, what they over-suggest.
8. **Limitations and failure modes**: scope, robustness, distribution shift, corner cases, cost, ethics, safety, privacy.
9. **Future work**: what follows scientifically rather than only engineering improvements.
10. **Presentation choices**: which slides may trigger questions, where backup slides are needed.

### Pass 4: Code and training-process attack surface

If code or training artifacts are available, audit them. If they are not available, generate questions that a committee would ask and mark the answers as `missing_evidence` or `paper_grounded`.

Audit axes:

| Axis | What to inspect | Typical defense risk |
|---|---|---|
| Repository entry points | `train.py`, `eval.py`, configs, README commands | unclear reproducibility path |
| Dependencies and environment | versions, CUDA, packages, Docker, hardware | results depend on hidden environment |
| Data pipeline | split generation, preprocessing, augmentation, leakage prevention | train/test leakage or unfair comparison |
| Model implementation | architecture, equation-to-code mapping, initialization, frozen modules | paper method not faithfully implemented |
| Loss and optimization | objective signs, weights, schedules, optimizer, gradient clipping, mixed precision | fragile or under-explained training tricks |
| Hyperparameter search | search space, validation protocol, selected configs | cherry-picking or unfair tuning |
| Randomness and seeds | number of runs, seed control, deterministic settings | unreported variance |
| Checkpoint selection | early stopping, best-on-validation vs test, model averaging | implicit test tuning |
| Evaluation code | metric implementation, post-processing, statistical aggregation | metric mismatch or inflated performance |
| Baseline reproduction | official implementations, tuning budget, same data preprocessing | weak or unfair baselines |
| Compute and cost | GPU type, hours, memory, energy estimate, inference latency | impractical or non-comparable cost |
| Released artifacts | pretrained weights, logs, commands, result tables | cannot verify main claims |
| Failure runs | negative results, instability, divergent runs | hidden brittleness |
| Licenses and ethics | dataset license, model release, PII, safety risks | legal or ethical blind spots |

For every code-related question, include:

```text
Question:
Likely trigger:
Evidence to check:
Safe answer if evidence exists:
Safe answer if evidence is missing:
Backup artifact to prepare:
```

### Pass 5: Prioritize questions

Classify every question by:

- `likelihood`: high / medium / low;
- `severity`: high / medium / low;
- `answer_readiness`: ready / needs evidence / risky / cannot defend;
- `audience`: beginner / peer / advisor / reviewer / committee / practitioner / author-defender / bug-hunter;
- `attack_axis`: novelty / soundness / reproducibility / experiment / code / training / theory / ethics / presentation;
- `answer_mode`: concise / technical / evidence-heavy / limitation-acknowledging / bridge-to-future-work.

Prioritize as follows:

| Priority | Condition | Required action |
|---|---|---|
| P0 | high likelihood + high severity + weak evidence | prepare honest limitation answer and backup slide |
| P1 | high likelihood + high severity + strong evidence | memorize answer and evidence reference |
| P2 | medium likelihood + high severity | prepare short answer and one backup detail |
| P3 | high likelihood + low severity | answer briefly, do not spend too much time |
| P4 | low likelihood + low severity | keep as appendix / backup only |

### Pass 6: Generate answer bank

For each major question, produce:

```text
Q_ID:
Question:
Audience:
Attack axis:
Why they may ask:
Expected concern:
Short answer, 1-2 sentences:
Long answer:
Evidence references:
Confidence:
What not to overclaim:
Backup slide / artifact:
If challenged again:
Follow-up experiment or code check:
```

The answer bank must include at least:

- 10 beginner / non-specialist questions;
- 15 peer / technical questions;
- 15 advisor / reviewer questions;
- 10 code and training-process questions when code/training is in scope;
- 5 limitation / failure-mode questions;
- 5 future-work questions;
- 5 “hostile but fair” questions.

For small papers or short user requests, reduce counts but keep all categories represented.

### Pass 7: Mock defense rehearsal

Create a rehearsal sequence:

1. **Warm-up round**: simple questions testing whether the user can explain the story.
2. **Mechanism round**: method, math, architecture, and algorithm questions.
3. **Evidence round**: experiments, baselines, ablations, and statistics.
4. **Code/training round**: implementation, configs, logs, reproducibility, and compute.
5. **Red-team round**: novelty, hidden assumptions, failure cases, and overclaiming.
6. **Recovery round**: questions where the best answer admits missing evidence and proposes a test.

For each round, include expected answer length, likely interruption, and a recovery phrase.

### Pass 8: Visual Q&A storyboard and image-prompt pack

When the user wants more intuitive, figure-rich defense preparation, transform high-value Q&A items into a visual series. Prioritize P0/P1 questions, code/training questions, and concepts that are hard to explain verbally.

Create these visual artifacts:

```text
visual_qa_storyboard_cn.md
visual_qa_storyboard_cn.json
visual_image_prompt_pack_cn.md
visual_generation_handoff_cn.md
visual_card_copy_cn.md
```

Use this structure for each visual card:

```text
Card ID:
Linked Q_IDs:
Purpose:
Question shown to audience:
Spoken answer summary:
Evidence label:
Boundary / what not to overclaim:
Visual metaphor or diagram:
Image prompt:
Text overlay plan:
Follow-up prompt for revision:
Generation status: text_ready | image_pending | image_generated
```

Recommended visual card types:

| Card type | Use when | Visual idea |
|---|---|---|
| Claim-evidence map | The question asks “where is that proven?” | claim nodes connected to paper/code/log evidence |
| Attack-surface radar | Many risks must be prioritized | radar or heatmap of novelty, soundness, reproducibility, compute |
| Method pipeline | The method is hard to explain | left-to-right architecture / data-flow storyboard |
| Equation-to-code bridge | The committee may ask whether implementation matches math | equation block connected to files/functions/config keys |
| Training timeline | Training stability or compute is questioned | timeline from data split to final checkpoint |
| Baseline fairness board | Reviewers may attack experiments | comparison table metaphor with same data, same metric, same tuning budget |
| Limitation boundary card | The answer must avoid overclaiming | safe zone / out-of-scope boundary diagram |
| Recovery answer card | The speaker needs a memorized answer | question bubble + claim/evidence/boundary/follow-up pattern |
| Backup slide visual | P0/P1 question needs a reserve slide | clean academic appendix-style figure |

Keep the visual series coherent: same aspect ratio, same visual style, same paper title convention, same evidence-label icons, and consistent terminology.

## Defense answer playbook

### 1. Novelty challenge

Question pattern:

```text
Isn't this just [prior method A] + [known trick B]?
```

Answer pattern:

```text
The closest prior work is indeed [A], and [B] is inherited.
The new part is [specific constraint / unavailable mechanism / surrogate / training setup].
The evidence that this is not only a plug-in is [ablation / comparison / theoretical analysis / failure of direct baseline].
The limitation is [what remains incremental or under-tested].
```

### 2. Baseline challenge

Question pattern:

```text
Why didn't you compare with [obvious baseline]?
Were baselines tuned fairly?
```

Answer pattern:

```text
The paper compares against [included baselines] because they cover [families].
[Missing baseline] would be relevant because [reason].
If it is absent, we should state that this is a limitation rather than dismiss it.
The fair follow-up is to run [baseline] under the same preprocessing, tuning budget, and metric.
```

### 3. Ablation challenge

Question pattern:

```text
Does the ablation prove the module's claimed role, or only show a performance drop?
```

Answer pattern:

```text
The ablation supports [local contribution] by removing/changing [component].
It does not by itself prove [causal explanation] unless the paper also shows [mechanism evidence].
So the defensible claim is [narrow claim].
A stronger test would be [targeted ablation / diagnostic / stress condition].
```

### 4. Training instability challenge

Question pattern:

```text
How sensitive is this result to seeds, hyperparameters, and compute?
```

Answer pattern:

```text
The reproducibility evidence available is [number of runs / std / config / logs / hardware].
The weak point is [missing variance / missing sweep / undocumented resource].
The safe answer is that the reported result is supported under [specified setup], but robustness to [unreported factor] is not fully established.
```

### 5. Code-faithfulness challenge

Question pattern:

```text
How do we know the code implements the method described in the equations?
```

Answer pattern:

```text
Map equation/module [X] to [file:function/config].
The key variables are [paper symbols] corresponding to [code names].
The training/evaluation entry points are [commands].
If this mapping is absent from the repository, state that reproducibility is weakened and prepare a code-to-equation table.
```

### 6. Negative result challenge

Question pattern:

```text
Where does the method fail?
```

Answer pattern:

```text
The paper's tested scope is [datasets/settings].
Within that scope, the weakest evidence is [failure case / lower-performing setting / missing stress test].
The likely failure mode is [assumption violated].
This does not invalidate the contribution, but it narrows the claim to [safe scope].
```

### 7. Ethics / safety challenge

Question pattern:

```text
Could the method cause harm or be misused?
```

Answer pattern:

```text
The relevant risk is [privacy / bias / misuse / security / environmental cost / human-subject risk].
The paper addresses it through [evidence] or does not address it sufficiently.
The safe defense is to state the actual mitigation and identify what remains unresolved.
```

## Required output files

When building a full defense pack, create:

```text
generated/defense/<paper-slug>/defense_scope_cn.md
generated/defense/<paper-slug>/claim_evidence_map_cn.md
generated/defense/<paper-slug>/paper_attack_surface_cn.md
generated/defense/<paper-slug>/code_training_audit_cn.md
generated/defense/<paper-slug>/defense_qa_bank_cn.md
generated/defense/<paper-slug>/defense_qa_bank_cn.json
generated/defense/<paper-slug>/answer_playbook_cn.md
generated/defense/<paper-slug>/mock_defense_script_cn.md
generated/defense/<paper-slug>/backup_slide_plan_cn.md
generated/defense/<paper-slug>/evidence_gap_triage_cn.md
generated/defense/<paper-slug>/visual_qa_storyboard_cn.md
generated/defense/<paper-slug>/visual_qa_storyboard_cn.json
generated/defense/<paper-slug>/visual_image_prompt_pack_cn.md
generated/defense/<paper-slug>/visual_generation_handoff_cn.md
generated/defense/<paper-slug>/visual_card_copy_cn.md
```

If the user only asks for a short Q&A list, produce a compact Markdown answer but still follow evidence labels.

## Required report sections

The main `defense_qa_bank_cn.md` must contain:

1. `答辩范围与证据状态`
2. `论文一句话主张与最安全表述`
3. `核心贡献的可防守版本`
4. `高风险问题总览`
5. `论文层面问题与回答`
6. `方法 / 公式 / 理论问题与回答`
7. `实验 / 消融 / 基线问题与回答`
8. `代码与训练过程问题与回答`
9. `可复现性与工程实现问题与回答`
10. `局限性 / 失败模式 / 伦理风险问题与回答`
11. `未来工作与研究边界问题与回答`
12. `最不该说的话`
13. `备份页与证据材料清单`
14. `模拟答辩脚本`
15. `最后 10 分钟速记卡`
16. `图文答辩卡片与生图提示词`

## Question-generation taxonomy

Use this taxonomy as a minimum list. Expand based on the target paper.

### A. Paper-story questions

- Why is this problem important now?
- What is the exact task setting?
- What assumption in prior work fails here?
- What is the simplest example that shows the problem?
- What is the paper's main contribution in one sentence?
- What would be lost if this paper did not exist?
- What is not new in this paper?
- What is the difference between the paper's claimed contribution and the implementation trick?

### B. Related-work and novelty questions

- Which prior paper is closest?
- Is this a new problem, a new method, a new theory, a new benchmark, or a better engineering recipe?
- Why is this not an obvious combination of existing methods?
- What baseline would make the novelty claim weaker?
- What related work is missing?
- Which citation is used as an ancestor, which as a contrast, and which as a benchmark protocol?

### C. Method and formula questions

- What does each module do, and where does its output go?
- Which module is essential, and which is auxiliary?
- What ideal mechanism is unavailable, and what surrogate does the paper build?
- What hidden assumption makes the surrogate work?
- What does each term in the loss / objective / bound mean?
- How does training differ from inference?
- What is the computational complexity?
- What happens if this hyperparameter is zero, one, very large, or very small?

### D. Theory and proof questions

- What does the theorem actually claim?
- Which assumptions are required?
- Which assumption is unrealistic?
- Does the proof cover the implemented algorithm or only a simplified version?
- What would break if the assumption is violated?
- Is the theory explanatory, predictive, or only sanity-checking?

### E. Experiment and evidence questions

- Which claim does each experiment support?
- Are the baselines strong and fairly tuned?
- Are metrics appropriate for the stated goal?
- Is the dataset split clean?
- Are the gains statistically meaningful?
- Are standard deviations, confidence intervals, or multiple seeds reported?
- Does the ablation isolate the mechanism or merely show a drop?
- Are there stress tests under the target hard setting?
- Is there any result that contradicts the story?

### F. Code and implementation questions

- Where is the training entry point?
- What command reproduces the main result?
- Which config corresponds to the main table?
- How are datasets downloaded, preprocessed, and split?
- How are random seeds controlled?
- How is the model architecture instantiated?
- Where is the loss implemented?
- Does the code match the equations exactly?
- Are hidden tricks used: gradient clipping, warmup, EMA, label smoothing, mixed precision, special initialization, filtering, checkpoint averaging?
- Are failure runs or unstable runs logged?

### G. Training-process questions

- What optimizer, learning-rate schedule, batch size, and number of steps were used?
- How were hyperparameters selected?
- Was validation used correctly, or was the test set indirectly tuned?
- What compute budget was required?
- Is performance sensitive to hardware, mixed precision, or distributed-training details?
- How many seeds were run?
- How was the best checkpoint chosen?
- Are pretrained weights used, and under what license?
- Is there any data contamination risk?

### H. Reproducibility and release questions

- Are dependencies specified?
- Are training and evaluation scripts available?
- Are pretrained models available?
- Does the README contain exact commands and expected results?
- Are logs, configs, and seeds included?
- Is the model / dataset license compatible with release?
- Can a third party reproduce the headline table without contacting the authors?

### I. Limitation and failure-mode questions

- Under what setting would the method fail?
- Which claim is most vulnerable?
- What does the paper not prove?
- What is the strongest negative result?
- What would a reviewer use as the main rejection reason?
- What real-world deployment risk is not addressed?

### J. Future-work questions

- What is the most natural next experiment?
- What would turn this from an engineering improvement into a new research direction?
- Which hidden assumption should be attacked next?
- What adjacent field could reuse the mechanism?
- What new benchmark would test the real contribution better?

## Audience-specific modes

### Beginner / non-specialist

Goal: check whether the speaker can explain without jargon.

Answer style:

- start from problem, not algorithm;
- use one example;
- avoid symbols until the intuition is clear;
- end with the paper's safe contribution.

### Peer / technical reader

Goal: check mechanism and details.

Answer style:

- define symbols;
- map modules to data flow;
- mention relevant equations / figures;
- identify assumptions and ablations.

### Advisor / committee

Goal: check independence, judgment, and limitation awareness.

Answer style:

- state trade-offs;
- compare alternatives;
- admit evidence gaps;
- propose concrete follow-up work.

### Reviewer / bug hunter

Goal: attack novelty, soundness, reproducibility, and evidence.

Answer style:

- cite exact evidence;
- avoid emotional defense;
- state what is proven and what is not;
- turn gaps into experiments or revisions.

### Industry practitioner

Goal: check cost, reliability, adoption, and operational risk.

Answer style:

- quantify compute, latency, memory, data requirement, failure cost;
- compare against simpler baselines;
- state deployment assumptions.

## Red-team rules

For every generated answer, perform a red-team pass:

- Does the answer cite concrete evidence?
- Is the answer too broad compared with the evidence?
- Does it ignore a missing baseline or failed ablation?
- Does it claim robustness without stress tests?
- Does it imply reproducibility without code/log support?
- Does it hide training tricks?
- Does it answer a different question than the one asked?
- Could the committee ask “where exactly is that shown?” and expose a gap?

If yes, rewrite the answer conservatively.

## Code-to-paper mapping rule

When code is available, build a mapping table:

| Paper object | Paper location | Code path | Function / class | Config key | Evidence strength | Risk |
|---|---|---|---|---|---|---|

Include at least:

- model architecture;
- each major module;
- loss terms;
- data preprocessing;
- train / validation / test split;
- optimizer and scheduler;
- evaluation metrics;
- main experiment config;
- baseline configs;
- checkpoint selection logic.

If code line numbers are known, include them. If not, include file and function names.

## Training-run audit rule

When logs or configs are available, build a training-run audit:

| Run / config | Dataset | Seed | Hardware | Time | Key hyperparameters | Result | Matches paper? | Notes |
|---|---|---|---|---|---|---|---|---|

Look for:

- mismatch between logged results and paper table;
- missing seeds;
- best-run-only reporting;
- test-set tuning;
- unreported preprocessing;
- non-default code paths;
- dependencies on pretrained models;
- failed or omitted runs.

## Backup-slide rule

For high-risk questions, propose backup slides:

| Question | Backup slide title | Content | Evidence | When to show |
|---|---|---|---|---|

Backup slides should cover:

- closest prior work comparison;
- full method pipeline;
- equation-to-code mapping;
- dataset splits and metrics;
- ablation table interpretation;
- seed variance / compute details;
- limitations and future tests;
- ethics / safety / privacy when relevant.

## “Most dangerous questions” section

Always identify the top 5-10 most dangerous questions.

For each:

```text
Why dangerous:
Current evidence:
Best honest answer:
What not to say:
How to reduce risk before the defense:
```

Dangerous questions often come from:

- missing obvious baseline;
- unexplained training trick;
- no multiple seeds;
- code not matching paper;
- reliance on proprietary or unavailable data;
- large compute without cost comparison;
- overclaiming generalization;
- lack of failure-case analysis;
- theory not matching implementation;
- ethical or legal risk.

## Output style

Use Chinese by default unless the user asks otherwise. Keep technical terms in English when they are standard in the field, but explain them.

Use compact tables for prioritization and evidence mapping. Use natural spoken answers for Q&A items, because the user needs to speak them during defense.

Prefer exact, defendable answers over impressive but vague answers.

For visual outputs, keep the image prompts practical: specify the card purpose, audience, visual metaphor, layout, style, aspect ratio, and exact text to overlay outside the image when needed. Avoid decorative images that do not help answer a real defense question.

## Full-pack directory structure

A complete defense pack should look like:

```text
paper_defense_bundle/
  metadata/
    defense_focus_spec.json
    defense_generation_status.json
  generated/
    defense/
      <paper-slug>/
        defense_scope_cn.md
        claim_evidence_map_cn.md
        paper_attack_surface_cn.md
        code_training_audit_cn.md
        defense_qa_bank_cn.md
        defense_qa_bank_cn.json
        answer_playbook_cn.md
        mock_defense_script_cn.md
        backup_slide_plan_cn.md
        evidence_gap_triage_cn.md
        visual_qa_storyboard_cn.md
        visual_qa_storyboard_cn.json
        visual_image_prompt_pack_cn.md
        visual_generation_handoff_cn.md
        visual_card_copy_cn.md
  reports/
    stage_delivery_handoff.md
```

## Validation requirements

Before handoff, verify:

- every high-risk question has an answer;
- every answer has evidence labels;
- every code/training answer either has a concrete artifact reference or is marked as missing evidence;
- every P0/P1 question has a backup slide or evidence artifact;
- every limitation answer states the safe scope;
- no answer claims unsupported reproducibility, robustness, or novelty;
- `defense_qa_bank_cn.json` is valid JSON;
- when visual mode is requested, visual storyboard files exist, each visual card links to at least one Q_ID, and every image prompt is marked `image_pending` until a separate image-generation step is explicitly requested.

Use `scripts/validate_defense_qa_bundle.py` when operating locally.

## ClawHub packaging rule

For ClawHub distribution, keep the skill folder name URL-safe and lowercase: `paper-defense-qa-code-training`. Keep `SKILL.md` frontmatter with `name`, `description`, and semver `version`. Include only text-based support files, keep the bundle under 50MB, and use MIT-0 / MIT No Attribution terms. Use `scripts/package_clawhub_skill.py` to validate and produce versioned `.zip` and `.skill` archives.

## Reply footer rule

At the end of every substantive reply using this skill, append:

```text
Current Status
Recommended Next Skill
Possible User Inputs For Next Stage
```

Typical next skill:

- `slides_creation_or_ppt_refinement` if the user wants PPT;
- `paper_deep_reading_teaching_explainer_v10` if the paper has not yet been deeply read;
- `report-innovation-graph-workbench` if the user wants future-direction mining after defense prep;
- a separate image-generation step if the user wants to render the `visual_image_prompt_pack_cn.md` prompts into actual figures.
