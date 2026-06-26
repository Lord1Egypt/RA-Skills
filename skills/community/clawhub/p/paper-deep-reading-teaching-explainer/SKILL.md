---
name: paper-deep-reading-teaching-explainer
description: Deep-read research papers into authoritative, evidence-grounded teaching reports, reproducibility/defense-ready explanations, innovation-mining artifacts, staged multi-image cartoon storyboard plans with continuity/cinematography and anti-hallucination source checks grounded in PDF and/or LaTeX sources, and final image-PDF assembly guidance. Use when users need rigorous paper understanding, teachable explanations, answer-prep material, reproducibility checks, and presentation-ready visual workflows without mixing report generation and image generation in one turn.
version: 10.1.8
metadata:
  openclaw:
    emoji: "📚"
    requires:
      anyBins:
        - python3
        - python
---

# ChatGPT Paper Deep Reading Skill

Use this source bundle inside a ChatGPT Project when the goal is to deeply read one paper or a small paper set into graph-ready, innovation-oriented intermediate artifacts.

This v10 fork adds a mandatory teaching-explainer overlay: every deep-read should also become material that helps the user explain the paper clearly to another person, defend it in discussion, and turn it into a teachable story without weakening any original research-generative or graph-ready requirement.

The normal downstream handoff after this stage is:

- `report-innovation-graph-workbench`

That downstream stage should read the uploaded deep-read bundle from Project `sources`, mine new directions and innovation points, and build graph outputs from the same evidence.


## Activation and staged-output protocol

When the user invokes this skill for a paper deep read, start with a brief plan before the report. The first execution turn is **text-only**:

1. show the plan;
2. generate and directly display the complete authoritative deep-reading report;
3. state the current status and produced artifacts;
4. tell the user how to ask for the next visual/storyboard step.

The first execution turn must **not** generate images. Report generation and image generation are separate phases.

## Reproducibility-defense-teaching quality overlay

Every report and downstream cartoon storyboard must be detailed enough for a user to reproduce the method, defend it in discussion, and teach it to another person. Do not stop at generic summaries.

Mandatory quality rules:

- Explain each key concept through `intuition -> mathematical formula -> concrete example -> limitation` / `直觉 -> 数学公式 -> 具体例子 -> 局限`.
- Present the paper in knowledge-dependency order: define symbols first, then data/input construction, then model/modules, then training and inference, then experiments and limitations.
- For every complex module, state its input, output, symbols, tensor/data dimensions when available, trainable parameters, fixed hyperparameters, and data flow.
- Strictly separate `paper-stated`, `reasonable inference from the paper`, and `inference borrowed from nearby work`. Label these categories explicitly in the report and do not blur them in image prompts.
- If the paper omits hardware, runtime, hyperparameters, baseline source, whether baselines were rerun/reimplemented, dataset split, random seeds, or preprocessing details, list the missing items as reproducibility gaps: mark them as `未报告` / `not reported`, 不要编造.
- Make the experiment section unusually concrete: dataset scale, label definition, split protocol, baseline taxonomy, baseline implementation source, metric meaning, main result exceptions, ablations, qualitative examples, and reproduction risks.
- Include one complete numeric toy example that walks through both training and inference with small numbers. If the paper's exact values are unavailable, use a clearly labeled illustrative toy example and state what is paper-stated versus toy-only explanation values.
- Apply the same quality bar to cartoon storyboards: visuals should show data flow, symbols, dimensions, missing experimental details, and evidence confidence instead of only attractive high-level summaries.
- Whenever the assistant writes image-generation prompts in text or generates several continuous cartoon images, include a continuity/cinematography block: sequence order, camera distance and movement, transition logic, style bible, recurring characters, colors, typography, symbols, and the narrative role of each image. For later batches, preserve the established style and logic from earlier images unless the user explicitly changes it.
- Before writing image-generation prompts or generating images, run a visual source-grounding check against the original paper sources and the authoritative deep-reading report. Every paper-specific module name, equation, dataset, metric, baseline, number, claim, limitation, or visual metaphor must be supported by the PDF/LaTeX or by a report section that is itself grounded in those sources. If the report and original paper conflict, prefer the original paper and flag the conflict; if evidence is missing, mark `未报告` / `not reported` or ask the user rather than hallucinating.
- For each requested visual part, generate a multi-image sequence rather than compressing several concepts into one crowded image. Background, algorithm, experiments, limitations, and future directions should be separate batches; inside a batch, split motivation, symbols, module IO, data flow, training, inference, results, exceptions, and caveats into separate images when they are distinct teaching points.

Because conversations may be stateless, every status or handoff reply must remind the user to resume with a prompt like:

```text
使用这个skill，根据状态，执行第X步：<要执行的阶段>。
```

If the user does not know the next prompt, tell them they can say:

```text
使用这个skill，根据状态，告知下一步应该问什么。
```

## Staged cartoon storyboard and PDF assembly protocol

After the complete text-only report has been delivered, the user may request separate visual steps. Each step generates one coherent part of a unified cartoon-comic storyboard. Keep style, protagonist, color palette, typography, panel numbering, camera grammar, and narrative logic consistent across all visual steps.

Maintain a compact storyboard bible after the first visual step: protagonist/narrator design, paper-specific visual metaphors, line style, color palette, typography, title/footer format, symbol dictionary, evidence-label style, aspect ratio, and camera language. Every later visual prompt must restate or reference this bible and say how the new images continue from the previous batch.

Hard separation rules:

- Do not generate images in the same assistant response that generates the full deep-reading report.
- Do not mix long textual report generation and image generation in the same assistant response.
- Each image-generation step should focus on one storyboard section only.
- Each storyboard section should produce multiple 16:9 images by default. Do not collapse a full section into one giant infographic unless the user explicitly asks for a single overview image; even then, explain that it is a lossy overview and keep the normal multi-image sequence as the recommended output.
- The final PDF assembly step must not create new images; it only combines already-generated images into a paginated PDF.

Default staged visual workflow:

0. **Text-only deep read**: plan, complete report, current status, produced artifacts, and next-step prompts. No images.
1. **Background / old-method defects / paper problem / inspiration**: continuous cartoon panels explaining why the problem matters and what previous methods miss.
2. **Algorithm overview and modules**: unified cartoon explanation of input construction, symbols, dimensions, module inputs/outputs, trainable parameters, data flow, training, inference, and one small numeric walkthrough.
3. **Experiment section**: dataset scale, label definition, split protocol, baseline taxonomy, whether baselines are rerun/reimplemented, metric meaning, results, exceptions, ablations, qualitative plots, missing implementation details, and reproducibility gaps.
4. **Limitations and defense**: reviewer-style concerns, overclaim guardrails, weak evidence, and defensible answers.
5. **Future directions and innovation graph**: hidden assumptions, new directions, next experiments, and research agenda.
6. **Cover / summary / Q&A backup visuals**: title cover, final recap, oral-defense backup cards.
7. **Final image-PDF assembly**: collect all approved storyboard images, sort them in story order, verify page count and visual order, and export one 16:9 PDF handoff.

Platform guidance for image steps:

- ChatGPT web/app: use **Create image** for storyboard image generation.
- Codex / Claude Code / coding-agent environments: if the `imagegen` skill is available, prefer it for storyboard image generation. If `imagegen` is unavailable or insufficient, call **ChatGPT Images 2.0 API** or another approved image-generation API.
- Do not use SVG diagrams as a substitute for the requested cartoon-comic storyboard images.

Storyboard source-grounding rule:

- Image/storyboard steps may be grounded in the **uploaded PDF**, the **LaTeX source**, or both.
- If a PDF is available, use rendered pages, figure/table locations, visible diagrams, captions, axes, and numeric tables as visual evidence.
- If LaTeX source is available, use `figure`/`table` environments, captions, labels, `\includegraphics` paths, equations, section text, and appendix/source files as evidence.
- If both PDF and LaTeX are available, cross-check them: use the PDF for visual layout and rendered appearance, and use LaTeX for exact captions, labels, equations, figure filenames, and text around the figure.
- The authoritative deep-reading report remains the primary source of truth for storyboard planning. If PDF and LaTeX conflict, note the conflict in a text-only status turn rather than silently inventing content.
- When an image prompt uses paper-specific values, diagrams, or claims, those details must be traceable to the PDF, LaTeX source, or the authoritative report.
- Storyboard prompts must label factual status when needed: `paper-stated`, `reasonable inference`, `nearby-work inference`, or `missing / not reported`.
- Text answers that provide image prompts must include continuity guidance for multi-image batches: image numbers, shot type, camera movement or framing, transition from the previous image, consistent style tokens, and the exact logic relation to earlier/later images.
- Text answers that provide image prompts must also include a short anti-hallucination checklist: original paper checked, authoritative report checked, unsupported facts removed or marked `未报告`, and conflicts flagged before image generation.
- Text answers that provide image prompts must include one prompt per image. Do not write one overstuffed prompt that asks the image model to merge multiple stages or many dense subtopics into a single picture.

Platform guidance for the final PDF assembly step:

- ChatGPT web/app: use the available file/Python/PDF workflow to place one approved image per 16:9 page and export a single PDF.
- Codex / Claude Code / coding-agent environments: use a local script such as `scripts/assemble_storyboard_pdf.py`, PIL/Pillow, ReportLab, or another approved PDF library.
- Verify that pages are in the intended order, no image is clipped, and the PDF preserves the 16:9 slide aspect ratio.
- Recommended output names: `paper_storyboard_all_images.pdf` and, if useful, `paper_storyboard_images_and_pdf.zip`.

## Upstream input contract

This stage should be restartable from a fresh session using only the previous stage's uploaded zip plus status and directory descriptions.

The upstream delivery should therefore include:

- one complete paper bundle zip
- `metadata/routing_status.json`
- `metadata/project_directory_index.json`
- `reports/project_directory_index.md`
- `metadata/paper_batch_manifest.json`
- per-paper `metadata/source_record.json`
- when available, `metadata/openreview_rebuttal_digest.json`

For each materialized paper, the upstream `source_record.json` should already expose at least:

- `canonical_paper_page_url`
- `conference_paper_url`
- `conference_pdf_url`
- `openreview_forum_url`
- `openreview_pdf_url`
- `arxiv_abs_url`
- `arxiv_pdf_url`
- `arxiv_latex_url`
- `preferred_source_type`
- `preferred_local_source_path`
- `local_latex_dir`
- `local_pdf_path`
- `local_openreview_pdf_path`
- `local_official_pdf_path`
- `local_arxiv_pdf_path`
- `review_bundle_dir`
- `review_digest_path`
- `canonical_review_source_type`
- `retrieval_sources`
- `verification_state`
- `verification_checks`
- `source_acquisition_status`
- `source_stage`
- `artifact_status`
- `review_bundle_completeness`

The deep-read stage should read `routing_status` and `project_directory_index` before browsing the tree ad hoc. Do not guess missing structure from filenames if these two files are present.
When available, also read `metadata/delivery_bundle_manifest.json` before ad hoc browsing. It is the authoritative restart contract for fresh-session handoff.

If the user provides multiple PDFs, process them as one bounded batch and keep both:

- per-paper outputs
- a cross-paper comparison artifact when it helps graph building or topic selection

For each paper, generate one standalone authoritative detailed report.
Do not merge multiple papers into one only detailed report.
The report must be at least as rich as the examples under `E:/论文调研/reports/accepted_papers/*.md`, and it must also include the extra graph-ready and direction-mining sections required by this stage.
Treat those accepted-paper examples as the minimum top-conference deepread bar for the main narrative, not just for the appendix.


## Research-generative overlay: read for new ideas, not only for understanding

This skill now includes the `Research-Generative Paper Reading` lens. Apply it as a **mandatory overlay** on top of all original `paper_deep_reading_skill` requirements.

### Non-weakening and conflict-resolution rule

- Do not remove, weaken, shorten, or bypass any existing paper-deep-reading requirement, including source contracts, formula preservation, proof-to-practice mapping, figure/table analysis, reviewer-lens audit, OpenReview handling, structured appendix, validation, and handoff rules.
- If a tension appears between the old deep-read requirements and the research-generative overlay, choose the interpretation that is **most useful for discovering new research ideas**, while still satisfying the original requirement.
- Do not claim certainty about private author thoughts. Always distinguish paper-grounded evidence from plausible reconstruction.
- Generic future-work suggestions are not enough. Convert hidden assumptions, unavailable mechanisms, proxy mismatches, and fragile links into concrete research directions.

### Core research equation

For every paper, explicitly extract the paper's research equation:

\[
\text{Paper}
=
\text{Important Setting}
+
\text{Broken Assumption}
+
\text{Borrowed Tool}
+
\text{New Constraint}
+
\text{Surrogate Mechanism}.
\]

Also express the paper as:

\[
A(P) \cap \neg C \cap T \cap M \Rightarrow Z \approx Y.
\]

Where:

- \(A(P)\): an existing paradigm that solves an important problem \(P\);
- \(C\): a common assumption in prior work;
- \(\neg C\): the target setting where the assumption fails;
- \(T\): a realistic constraint such as privacy, decentralization, non-IID data, low labels, safety, latency, limited compute, missing modalities, or distribution shift;
- \(M\): a method family that almost transfers;
- \(Y\): the ideal mechanism normally required by \(M\);
- \(Z\): the paper's new surrogate mechanism for \(Y\).

The report must answer: **what unavailable mechanism did the authors replace, and how did they make the replacement feel inevitable?**

### Author-side direction discovery

Add a research-discovery reconstruction using:

\[
\text{New Direction}
=
\text{Valuable Field}
+
\text{Painful Assumption}
+
\text{Emerging Tool}
+
\text{Unserved Setting}.
\]

For each central idea, identify:

1. the popular paradigm;
2. the hidden assumption;
3. the realistic violation;
4. the tempting borrowed method;
5. the blocking constraint;
6. the authors' conceptual replacement.

Use phrases such as:

- "A plausible author-side thinking path is..."
- "The paper's setup suggests..."
- "This is an evidence-backed reconstruction rather than a factual claim about the authors' private thoughts."

### Story-construction and module logic

For each paper, reconstruct the story bridge:

\[
\text{Challenge}_i
\rightarrow
\text{Failure Mode}_i
\rightarrow
\text{Design Principle}_i
\rightarrow
\text{Module}_i
\rightarrow
\text{Ablation}_i.
\]

Create a table:

| Challenge | Failure mode | Design principle | Module | Evidence |
|---|---|---|---|---|

Then decide whether the method is a weak additive story:

\[
M_1 + M_2 + M_3
\]

or a stronger closed-loop story:

\[
M_1 \Rightarrow M_2 \Rightarrow M_3 \Rightarrow M_1.
\]

Name the object that flows through the loop, such as pseudo-labels, generated data, graph consensus, uncertainty, prototypes, rewards, or memory.

### Module author-thinking template

For every major module, use this template in addition to the existing formula/module critique:

\[
M_i
=
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
\text{Risk}.
\]

The report must identify:

- what would fail without the module;
- what ideal solution would solve it in an easier setting;
- what proxy signal/resource remains available;
- how the authors convert the proxy into a mechanism;
- the hidden assumption \(H_i\);
- the failure case under \(\neg H_i\);
- the new research idea created by attacking \(\neg H_i\).

### Reverse citation logic

Do not only list related work. For important citations, infer their narrative function:

| Citation cluster | Narrative function | Assumption inherited | How this paper modifies it |
|---|---|---|---|

Treat citations as permissions to make moves such as: field foundation, limitation evidence, method ancestor, neighboring-field transfer, strong baseline, benchmark protocol, implementation machinery, or negative contrast.

### Experiments as story evidence

Read each experiment as:

\[
\text{Experiment}
=
\text{Claim}
+
\text{Counterfactual}
+
\text{Metric}
+
\text{Stress Condition}.
\]

For every major experiment block, state:

- which claim it supports;
- which alternative explanation it rules out;
- which module or design choice it justifies;
- whether the stress condition actually matches the target hard setting;
- whether the ablation proves the module's narrative role or only reports a performance drop.

### Reusable paper-making pattern

Extract at least one reusable story template from the paper, especially:

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

Also look for:

- replacement story: easy-setting resource \(Y\) is unavailable, so the paper designs \(Z\);
- two-axis empty-cell story: prior work solves each difficulty separately but not their intersection;
- closed-loop contribution story: noisy signal -> proxy resource -> better coordination -> cleaner signal;
- boundary-pushing story: make a module work when its hidden assumption fails.

### Weakness-to-new-idea conversion

For each major weakness, use:

\[
\text{Weakness}
=
\text{Claim}
-
\text{Evidence}
+
\text{Hidden Assumption}.
\]

Then convert it into:

\[
\text{Future Work}
=
\text{Current Method}
+
\text{Violated Assumption}
+
\text{New Mechanism}.
\]

Prioritize directions that expose scientific frontier questions rather than only engineering refinements.


## Teaching-Explainer overlay: read so the paper can be taught to others

This skill now includes the `Teaching-Explainer Paper Reading` lens. Apply it as a **mandatory overlay** on top of the original deep-reading and research-generative requirements.

### Non-weakening rule for teaching outputs

- Do not replace the authoritative detailed report with a short teaching summary.
- Do not omit formulas, proofs, figure/table analysis, reviewer concerns, OpenReview context, research-equation analysis, structured appendix, validation, or next-stage handoff because the user wants a clearer explanation.
- Teaching clarity is an extra constraint: make the report easier to explain **after** the full evidence-grounded deep read is complete.
- If a simplified explanation would hide an important assumption, formula term, negative result, failure mode, reviewer concern, or evidence gap, include both the simplified explanation and the rigorous caveat.
- Keep epistemic discipline: mark whether a teaching claim is paper-grounded, inferred, externally contextualized, or a deliberately simplified analogy.

### Teaching source inspirations to integrate

The teaching layer distills public best practices from paper-reading seminars, reviewer guides, and paper-analysis skills. It should be used as a method, not as a citation substitute inside the paper report.

- Use a multi-pass reading logic inspired by the three-pass method: first identify the paper's shape, then understand the content, then reconstruct the work deeply enough to critique and teach it.
- Use role-based critical discussion inspired by role-playing paper-reading seminars: separate the archaeologist, bug hunter, researcher, practitioner, social-impact assessor, and author-defender viewpoints.
- Use a seminar-presentation target: high-level idea, key technical details, experimental results, background/related work, limitations, and 3-5 discussion questions.
- Use an introduction-story target: problem, motivation, solution, and contributions, then work backward from contributions to reconstruct the teachable narrative.
- Use reviewer criteria as teaching checkpoints: soundness, significance, novelty, clarity, relation to prior work, reproducibility, experimental design, statistical rigor, and evidence-to-claim alignment.
- Use architecture-diagram and epistemic-tag discipline from paper-reading skills: each diagram or analogy must distinguish what the paper says from what is inferred for explanation.

### Audience-first explanation contract

Before writing the final report, infer or ask for the likely audience when feasible. If the user does not specify, default to:

- primary audience: a technically literate graduate student outside the paper's narrow subfield;
- secondary audience: a skeptical reviewer or advisor;
- tertiary audience: a beginner who needs intuition but not every proof detail.

For each paper, the report must include an explicit explanation plan:

| Audience | What they already know | What they will likely miss | What must be explained first | How much math to show | What evidence will convince them |
|---|---|---|---|---|---|

Do not assume that a listener understands the paper's notation, task setting, benchmark culture, or hidden assumptions. Explain these before relying on them.

### Multi-pass teaching read loop

Run this loop in addition to the existing workflow:

1. **Orientation pass**: title, abstract, key figures, task setting, and claimed contribution. Produce a one-sentence paper thesis and a one-sentence why-it-matters statement.
2. **Structure pass**: map section-by-section roles: setup, gap, method, theory, experiments, ablations, limitations, rebuttal, appendix.
3. **Mechanism pass**: trace data, symbols, losses, modules, gradients/updates, evidence, and assumptions from input to output.
4. **Virtual reimplementation pass**: explain how one would rebuild a minimal toy version of the method and where the hard parts appear.
5. **Reviewer pass**: challenge novelty, soundness, baselines, reproducibility, claims, figures, and limitations.
6. **Teacher pass**: turn the deep read into a teachable sequence, blackboard derivation, examples, FAQ, and discussion prompts.
7. **Teachback pass**: create questions that test whether a listener really understood the paper rather than memorized the summary.

### Mandatory teaching sections in the authoritative report

The detailed report must include these sections in addition to all original sections:

- `面向讲解的受众画像与讲解目标`
- `3 层讲解摘要：30 秒 / 3 分钟 / 10 分钟`
- `讲解主线 Story Spine`
- `听众先修知识与概念铺垫`
- `公式 / 图表 / 实验的讲解脚本`
- `板书推导与小例子演示`
- `角色扮演式讨论问题`
- `可能被问到的问题与回答证据`
- `易误解点与纠偏`
- `PPT / 分享稿结构草案`
- `听众可带走的三句话`

These sections may appear near the end of the main report before the plain-language story summary, or inside a clearly marked teaching appendix, but they must be present in the authoritative report.

### Explanation story spine

For each paper, produce a compact teaching spine:

```text
Before this paper:
  The field could do X under assumption C.
Pain:
  In setting T, C fails, so X no longer works.
Tempting path:
  Method family M almost helps, but it requires unavailable mechanism Y.
Key insight:
  The paper constructs surrogate Z for Y.
Method:
  Z is implemented through modules M1, M2, ...
Evidence:
  Experiments/figures/theory show Z helps under stress condition S.
Caveat:
  Z still depends on hidden assumption H.
Teaching punchline:
  The paper's contribution is not just a module, but a replacement story: Y is unavailable, so Z is made useful.
```

This story spine must remain consistent with the research equation:

```text
A(P) ∩ ¬C ∩ T ∩ M ⇒ Z ≈ Y
```

### Explanation ladder

Provide explanations at three levels:

1. **Intuition layer**: analogy, plain-language causal story, no equations.
2. **Mechanism layer**: modules, signals, losses, data flow, and why each part is necessary.
3. **Evidence layer**: tables, figures, ablations, theory, reviewer discussion, and limitations.

The report must explicitly state what is lost when moving from layer 2 or 3 down to layer 1.


## Staged Cartoon Visual-Storyboard Workflow (mandatory after the report, only when the user asks)

This skill supports a second phase for generating presentation-friendly visual storyboards, but **the first execution of the skill must never generate images**. The first execution is a text-only deep-reading delivery.

### Hard separation rule: report text and image generation cannot happen in the same reply

- Do **not** generate images in the same assistant turn that delivers the authoritative detailed report, status, or step instructions.
- Do **not** mix a long textual explanation with image generation in the same assistant turn.
- Text-only turns may provide a plan, status, image-step menu, prompts, and platform guidance.
- Image-generation turns should be limited to generating the requested image batch. If using ChatGPT image generation, after the images are generated, keep the assistant's text minimal or empty according to the image tool behavior.
- If a user asks for both “show the report” and “draw images” in one message, first complete only the report/status turn, then tell the user exactly which follow-up command will start the next visual step.

### First-run behavior when the skill is invoked

When the user invokes this skill for a paper, first respond with a concise plan, then produce only the complete authoritative deep-reading report and required delivery/status information. This first run must include:

1. **Plan**: briefly state the workflow stages that will be used:
   - Step 0: complete text-only deep read;
   - Step 1+: staged visual storyboard generation, only after the user asks for a specific step.
2. **Complete deep-reading report**: generate and display the full detailed report satisfying all deep-read, research-generative, teaching-explainer, reviewer-audit, figure/table, formula, experiment, limitation, and handoff requirements.
3. **State and outputs**: tell the user what has been produced and what state the workflow is currently in.
4. **Next-step prompts**: tell the user how to ask for the next step. Include a restart-safe phrase such as:
   - `使用这个skill，根据状态，执行第1步：生成多张连续的卡通图，内容是背景、旧方法缺陷、论文问题与灵感来源。`
   - `使用这个skill，根据状态，告知下一步应该问什么。`

### Stateless conversation reminder

Assume the conversation may be stateless. In every text-only status or planning turn, remind the user to include the skill name and current state in the next command. Use wording like:

> 如果开启新会话或上下文丢失，并且要继续生图，请说：`使用这个skill，根据状态，执行第X步：生成多张连续的卡通图，内容是...`。如果不知道下一步怎么问，可以说：`使用这个skill，根据状态，告知下一步应该问什么。`

### Visual-generation platform guidance

Before starting any image-generation phase, include this guidance in a **text-only planning/status turn**, not in the same turn as image generation:

- If the user is using ChatGPT 网页版 / ChatGPT App: use **Create image** mode for the storyboard images.
- Do **not** generate SVG diagrams for these storyboard steps.
- If the user is using Codex, Claude Code, or another coding-agent environment: prefer the `imagegen` skill when it is available. If `imagegen` is unavailable or insufficient, call **ChatGPT Images 2.0 API** or another available image-generation API to produce the images; do not try to replace the requested cartoon storyboard with SVG-only output.

### Default staged visual storyboard plan

After Step 0 is complete, offer a multi-step image plan. The user may request one step at a time. Each step should generate a coherent set of multiple 16:9 images in the same visual identity: cartoon-comic academic infographic style, consistent narrator character, consistent title numbering, consistent color palette, clear panels, actual paper data where relevant, logical continuity, and intentional camera progression. Do not compress a whole step into one dense image.

Recommended default steps:

| Step | Name | Purpose | Typical image count | Must include | Must avoid |
|---|---|---:|---:|---|---|
| Step 1 | 背景 / 旧方法缺陷 / 问题与灵感 | Explain why the problem matters before the algorithm | 4-6 | continuous event streams, snapshot limitations, feature scarcity, context mismatch, ambiguous boundary, paper motivation | algorithm internals and experiment results |
| Step 2 | 算法整体流程与模块 | Explain the method from input event to training and inference | 5-7 | symbols, input/output, dimensions, module data flow, trainable parameters, fixed hyperparameters, training vs inference, one numeric walkthrough | final performance results |
| Step 3 | 实验部分 | Explain datasets, baselines, metrics, protocols, results, exceptions, ablations, qualitative plots, reproducibility caveats | 5-7 | dataset scale, labels, splits, baseline provenance, rerun/reimplementation status, metric meaning, main results, exceptions, missing GPU/runtime/seed/hyperparameter details | unsupported claims about hardware/time |
| Step 4 | 关键局限与答辩质疑 | Prepare defense visuals for limitations and likely reviewer questions | 3-5 | score/boundary caveat, training contamination, cold-start, reproducibility, AP caveat, fairness of baseline protocol | inventing reviewer comments not present in sources |
| Step 5 | 未来方向与创新图谱 | Turn the paper into research-direction visuals | 3-5 | hidden assumptions, violated settings, robust flow, inductive compatibility, online conformal boundary, causal/counterfactual compatibility | presenting future work as already validated |
| Step 6 | 汇报封面 / 总结 / Q&A backup | Presentation packaging | 2-4 | cover image, final takeaway image, Q&A map | adding new technical claims |

### Visual step execution protocol

When the user asks to execute a visual step:

1. Verify which step is requested and whether it follows the current state.
2. If the request is not clear, provide a text-only step menu and ask the user to choose. Do not generate images in that clarification turn.
3. If the request is clear and explicitly asks to generate images, call the image-generation tool directly for that step. Use 16:9 aspect ratio unless the user explicitly changes it.
4. Preserve continuity with earlier generated images when available by referencing their visual style: same cartoon narrator, same title numbering, same panel language, same blue-accent academic-comic style, same symbol dictionary, same evidence-label treatment, and compatible camera grammar.
5. Ground all factual data in the paper and prior report. If a value is not in the PDF, mark it as missing in a text-only planning/status turn, or show it as “未报告” in an image prompt; 不要编造.
6. For image steps, do not generate SVG. Use Create image in ChatGPT web/app. In Codex-style environments, prefer the `imagegen` skill when available; otherwise use ChatGPT Images 2.0 API or another approved image API.
7. Do not include detailed report text in the same response as image generation.
8. For method visuals, show knowledge dependency order: symbols -> data/input -> model/modules -> training/inference -> experiments/limitations.
9. For key concept visuals, use the compact ladder `intuition -> formula -> concrete example -> limitation` when space permits.
10. For experiment visuals, show missing implementation details explicitly as `未报告` rather than visually inventing them.
11. For multi-image batches, plan the sequence like a short film: establishing shot -> process/interaction shots -> close-up of the key mechanism/equation/result -> synthesis/transition shot. Use this only as a default rhythm; adapt it to the paper's logic.
12. Keep each cartoon image pedagogically legible: one main idea per image, minimal readable labels, clear visual hierarchy, stable left-to-right or top-to-bottom data flow, and no decorative scenes that hide the scientific point.
13. Before prompt handoff or direct generation, run the source-grounding anti-hallucination checklist. After image generation, inspect the generated image against the prompt, original sources, and report. If an image contains unsupported text, invented numbers, wrong module names, wrong arrows, or ungrounded conclusions, do not move it to PDF assembly; revise the prompt and regenerate or ask the user for missing evidence.
14. Split dense content across images. If a prompt contains more than one major teaching point, divide it into separate image prompts instead of asking for a single compressed collage.

### Prompting templates for the user

At the end of Step 0 or any text-only status turn, provide concise examples:

- `使用这个skill，根据状态，执行第1步：生成多张连续的卡通图，内容是背景、旧方法缺陷、论文问题与灵感来源。`
- `使用这个skill，根据状态，执行第2步：生成多张连续的卡通图，内容是算法整体流程与各模块解释。`
- `使用这个skill，根据状态，执行第3步：生成多张连续的卡通图，内容是实验部分，包含数据集、baseline、AUC/AP、主结果、消融和复现缺口。`
- `使用这个skill，根据状态，执行第4步：生成多张连续的卡通图，内容是局限性与答辩质疑。`
- `使用这个skill，根据状态，执行第5步：生成多张连续的卡通图，内容是未来方向和创新图谱。`
- `使用这个skill，根据状态，告知下一步应该问什么。`


### Formula teaching rule

For every preserved key formula, provide:

| Formula | What problem it solves | Term-by-term meaning | How to say it aloud | Where it appears in the algorithm | What can go wrong |
|---|---|---|---|---|---|

Also include one beginner-friendly concrete example for at least one central formula or update rule.

### Figure and table teaching rule

For every important figure/table already analyzed by the deep-read stage, add a teaching script:

| Visual | First thing to point at | Listener confusion risk | Claim supported | What not to overclaim | Suggested verbal explanation |
|---|---|---|---|---|---|

If a figure is visually persuasive but evidentially weak, teach that distinction explicitly.

### Experiment teaching rule

Turn each experiment block into a question-answer unit:

```text
Question the experiment answers:
What a skeptical listener might ask:
Setup / dataset / baseline / metric:
Expected result if the paper's claim is true:
Actual result:
What it proves:
What it does not prove:
How to explain the table or curve in one sentence:
```

### Role-play discussion pack

For each paper, create role-based discussion prompts:

| Role | What this role checks | Required output |
|---|---|---|
| Archaeologist | prior-work ancestry and what is truly new | one older ancestor, one inherited assumption, one modification |
| Bug Hunter | rigor, correctness, reproducibility, clarity | three attack questions and one likely author response |
| Researcher | future directions and test-of-time value | two follow-up projects, one high-risk boundary idea |
| Industry Practitioner | deployability and cost-benefit | adoption conditions, complexity cost, practical failure mode |
| Social Impact Assessor | risks, misuse, bias, privacy, safety | one positive impact, one omitted negative impact |
| Author Defender | rebuttal and best-paper pitch | strongest acceptance argument and weakest vulnerable claim |
| Teacher | whether a non-specialist can follow | analogy, prerequisite list, teachback questions |

### Talk / PPT blueprint rule

Do not create a separate final report that competes with the authoritative detailed report. If a talk or slide blueprint is needed, make it a derivative artifact that cites the authoritative report as its source.

Minimum slide blueprint:

| Slide | Title | One-sentence point | Visual / formula | Speaker notes | Transition | Likely question |
|---|---|---|---|---|---|---|

Recommended default structure:

1. Why should we care?
2. What was impossible or painful before?
3. What assumption breaks?
4. What is the core idea in one picture?
5. What does the method actually do?
6. What is the central formula / mechanism?
7. How does the algorithm run on a toy example?
8. What experiments prove the claim?
9. What do figures/tables actually show?
10. What are the strongest weaknesses?
11. How would a reviewer attack it?
12. What research directions follow?
13. Three takeaways.

### Q&A and defense rule

Prepare likely questions from three audiences:

- beginner questions: terms, task, intuition, why not simpler;
- peer questions: method details, formulas, baselines, ablations, assumptions;
- advisor/reviewer questions: novelty, significance, reproducibility, missing evidence, limitations, next work.

For each answer, point back to specific evidence from the paper or state that the paper does not provide enough evidence.

### Misunderstanding guardrails

Every teaching report must include:

- what the paper does **not** claim;
- which simplified analogy could mislead;
- which result should not be generalized beyond the paper's tested setting;
- which module is easy to mistake for the whole contribution;
- which baseline comparison is easy to overinterpret;
- which limitation should be stated out loud during a talk.

### Teachback self-test

End the teaching section with 8-12 questions a listener should be able to answer after the explanation. Include at least:

- one problem-setting question;
- one assumption-breaking question;
- one method-dataflow question;
- one formula interpretation question;
- one experiment-evidence question;
- one limitation question;
- one reviewer-attack question;
- one future-direction question.

### Teaching sidecar artifacts

When useful, create derivative sidecar artifacts under:

- `generated/teaching/<paper-slug>/teaching_outline_cn.md`
- `generated/teaching/<paper-slug>/slide_blueprint_cn.json`
- `generated/teaching/<paper-slug>/qa_bank_cn.json`
- `generated/teaching/<paper-slug>/role_play_discussion_pack_cn.md`

These sidecars must not replace the authoritative detailed report. They should cite or reference the sections of the authoritative report they derive from.


## Extended deep-reading rule set

The following requirements are mandatory even when they are not strongly emphasized by the original paper:

- **Title interpretation rule**: explicitly interpret the paper title term by term. Explain what each keyword means, why the title is phrased that way, and how the title maps onto the actual method, setting, and claims in the paper.
- **Mentioned-paper expansion rule**: do not only list cited papers. For the papers that the target paper repeatedly discusses, compare what they solved, what they still left open, and why the current paper needed to move beyond them.
- **Multi-layer scientific-problem rule**: explain both the paper-level problem and the upper problem ladder. Prefer continuous ladders such as direction-native -> parent-field -> broader AI/ML, and also discuss algorithm-lineage and bottleneck-derived upper problems when defensible.
- **Claim-audit rule**: extract the paper's innovation points and core claims one by one, then audit whether each claim is supported by theory, experiments, ablations, visual evidence, reviewer discussion, or only by suggestive narrative. Say explicitly when support is weak, indirect, or missing.
- **Research-thought reconstruction rule**: reconstruct the likely reasoning path that led the authors from observed pain points and prior work to the final design. Also infer what papers, methods, or upper-level scientific problems may have inspired the idea. Separate evidence-backed inference from speculation.
- **Author-subjectivity linkage rule**: when discussing the idea, theory, proof choices, algorithm, or modules, explicitly note where the design may reflect the authors' subjective judgments, tastes, priors, heuristics, engineering preferences, or research style. Distinguish objective necessity from author-specific choice whenever the paper gives enough evidence.
- **Paper-grounded specificity rule**: do not stay at a generic or abstract summary level. Stay close to the actual paper by naming the concrete modules, symbols, assumptions, losses, theorem objects, datasets, baselines, figures, and experimental findings that the authors actually use.
- **Related-work relation rule**: explain the main related-work clusters and state the exact relation between each cluster and the current paper: inherited, contrasted, generalized, specialized, hybridized, or problem-shifted.
- **Symbols-and-concepts rule**: explain symbols, assumptions, operators, and problem-specific concepts in beginner-friendly language before relying on them in later sections.
- **Formula-preservation rule**: do not drop, compress away, or replace key equations with prose-only summaries. Preserve the paper's core objective functions, update rules, constraints, estimators, bounds, and theorem statements in readable form, then explain each formula term by term and state what role the formula plays in the method.
- **Proof-to-practice mapping rule**: if the paper contains theory or proofs, explicitly map theorem assumptions, intermediate claims, and conclusions to the practical algorithm, implementation steps, or system behavior. State whether the implementation is exactly matched to the proved object, only approximately aligned, or only motivated by the theory.
- **Theory-purpose rule**: explain why each proof or theoretical claim was included by the authors, what reviewer doubt or scientific concern it addresses, what practical meaning it has, and where the theory stops being faithful to the real implementation.
- **Module-and-equation critique rule**: do not stop at restating the design. For each central formula, module, and modeling assumption, judge whether it may be brittle, under-justified, overly heuristic, computationally expensive, hard to optimize, poorly identified, or mismatched to the claimed scientific goal. Then discuss concrete improvement room, alternative formulations, and what trade-offs those changes would create.
- **Concrete algorithm walkthrough rule**: the algorithm section must not stop at equations. Give a step-by-step procedure and at least one small concrete example that instantiates the states, inputs, outputs, and updates.
- **Experiment genealogy rule**: when baselines are compared in the experiments, explain how those baselines relate to the algorithms and literature introduced earlier in the paper, especially the Introduction and Related Work sections.
- **Experiment-purpose rule**: for every major experiment block, state what question it is trying to answer, what reviewer doubt it addresses, and what kind of evidence it produces. Also point out interesting, surprising, or controversial empirical phenomena.
- **Reviewer-lens enrichment rule**: enrich the deep-reading report with extra reviewer lenses inspired by strong GitHub paper-review / peer-review skills. At minimum, explicitly audit novelty, significance, technical soundness, methodological rigor, reproducibility, results-claims alignment, missing baselines or controls, figure/table clarity, limitation honesty, and venue-fit or acceptance logic when relevant.
- **LaTeX-figure explanation rule**: when a LaTeX source is available, do not ignore figures just because the paper is not being read from a rendered PDF. Reconstruct important figures from figure environments, captions, labels, referenced text, and included image paths when possible, then explain what each figure is trying to show, how it supports the argument, and what it leaves unclear.
- **PDF-figure explanation rule**: when a PDF source is available, important figures must also be explicitly interpreted rather than only glanced at. Explain each key architecture figure, pipeline figure, qualitative example, and experimental plot in terms of purpose, visual structure, figure-to-claim mapping, and what remains unclear, potentially misleading, or insufficiently supported.
- **Experiment-chart consistency rule**: in the experiment section, explicitly explain important tables, charts, curves, qualitative figures, and numeric comparisons. State which claim each visual or data block supports, whether the evidence really matches the stated claim, and where there is partial support, contradiction, or unexplained mismatch. Analyze plausible reasons for those mismatches instead of smoothing them away.
- **Innovation-type rule**: judge whether the work is mainly incremental, cross-domain, boundary-breaking, or a mixture. Explain why.
- **Boundary-crossing rule**: discuss whether the paper truly crosses a disciplinary or subfield boundary, or mainly recombines ideas inside one field.
- **Limitation rule**: explicitly discuss the paper's weaknesses, unresolved assumptions, failure modes, scope limits, and risks of overclaim. Distinguish between minor limitations and structural limitations that cap the paper's impact.
- **Scientific-frontier direction rule**: when proposing future work, distinguish ordinary follow-up engineering from directions that could actually push scientific boundaries. State what new scientific question, cross-field bridge, or conceptual shift would be required for a boundary-pushing follow-up.
- **New-direction rule**: speculate about follow-up directions and new innovation hooks, including cross-domain transfer, lateral migration of the method, native extensions of the paper's own line, and higher-risk directions that may open a new boundary rather than only improve a benchmark.
- **Story-summary rule**: end with one simple and vivid story that a non-specialist could understand without equations.
That means the authoritative report must explicitly cover:

- 论文信息
- 论文标题解读
- 这篇论文真正解决的是什么
- 论文中提到的其他论文做了什么、留下了什么空白、与本文是什么关系
- 核心方法到底在干什么
- 公式保留与逐式解释
- PDF 版本关键图解释
- 理论、证明与实现步骤对照
- 具体公式、模块与设计假设的不足及可改进空间
- 创新点、核心主张与证据逐条核对
- 这篇论文为什么重要 / 为什么值得被接收
- 实验是如何被设计出来的
- 倒推作者怎么想到这个 idea
- idea / 理论证明 / 具体算法或模块里哪些部分更像作者的主观选择、经验判断或研究风格
- 报告必须结合论文本身的具体模块、公式、图表、实验与措辞，不能停留在过于抽象的泛化总结
- 审稿人最关注什么
- 额外审稿视角审计（借鉴 GitHub 热门审稿 skill 的 reviewer 关注点）
- 作者是怎么回复的
- 审稿人是否认同作者回复
- 审稿意见回复覆盖核对
- 强点 / 弱点 / 不足
- 作者团队近年的相关延续
- 未来边界
- 创新类型判断（增量 / 交叉 / 边界突破）
- 对选题的直接启示
- 可能的新研究方向或新创新点（尤其是可能推动科学边界的方向）
- 通俗生动故事总结
- 参考来源
- 再加上本 stage 需要的结构化补充附录
- 其中结构化附录里必须显式包含“公式保留与逐式解释”“理论、证明与实现步骤对照”以及“具体公式、模块与设计假设的不足及可改进空间”

The detailed report length is not capped. Prefer completeness over brevity when the paper warrants it.

In ChatGPT Projects, the default input should be one uploaded paper-collection zip in Project `sources`.
That zip should contain the paper PDFs and metadata bundle produced by the collection stage. Do not assume a local filesystem paper folder exists.
If a clean local scaffold is needed before building the upload bundle, initialize it with:

- `scripts/init_paper_deep_reading_scaffold.py`
- `scripts/build_paper_deep_reading_bundle.py`
- `scripts/validate_detailed_report_structure.py`

That scaffold should create:

- `metadata/query_spec.json`
- `metadata/paper_batch_manifest.json`
- `metadata/delivery_bundle_manifest.json`
- `metadata/routing_status.json`
- `metadata/project_directory_index.json`
- `reports/project_directory_index.md`
- `reports/stage_delivery_handoff.md`
- `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.md`

## Core rule

Work in stages. If the next step depends on files not yet present in the current Project `sources`, stop and ask the user to upload them first.

This especially includes:

- paper PDFs
- OpenReview review / rebuttal exports
- supplementary PDFs
- LaTeX source
- generated page images
- generated visual manifests
- generated intermediate Markdown / JSON

## Required layered outputs

- broader ML/AI scientific problems
- adjacent parent-field problems
- higher-problem provenance:
  - paper-explicit
  - borrowed-algorithm ancestry
  - new-algorithm bottleneck
- direction-native problems
- module-to-problem mapping
- graph node candidates
- graph relation candidates
- related-paper linkage notes
- idea-genesis trace
- motivation-to-algorithm bridge evidence
- rebuttal-aware gap notes
- figure analysis
- table / chart design analysis
- reviewer-lens audit matrix
- figure-to-claim mapping
- table/chart/data-to-claim mapping
- experiment consistency notes
- visual prompt blueprint
- teaching story spine
- audience prerequisite map
- formula/table/experiment teaching scripts
- role-play discussion pack
- Q&A and defense bank
- slide/talk blueprint
- teachback self-test

When extracting upper scientific problems, do not rely only on the paper's own phrasing.
Build a progressive problem ladder instead of making a large abstraction jump.
Prefer:

- direction-native problem
- adjacent parent-field problem
- broader ML/AI scientific problem

Example:

- `PFL -> FL -> AI/ML`

Do not jump directly from `PFL` to a remote `AI/ML` abstraction if `FL` is the scientifically meaningful middle layer.
Only skip the middle layer when no defensible parent-field layer exists, and say so explicitly.

Also infer the upper ladder from:

- the algorithm families the paper borrows from
- the problems or bottlenecks the new algorithm itself runs into

Keep those three paths separate in the machine-readable outputs so a downstream graph page can show:

- what the paper explicitly claimed
- what was implied by borrowed algorithm lineage
- what was implied by the new method's encountered bottlenecks

For each path, preserve the nearest parent-field layer before the broader ML/AI layer whenever the evidence supports it.

## Review-context rule

If the paper is from ICLR, use the paper title and year to find the matching OpenReview forum before writing the review/rebuttal section. Use that forum as the canonical source for reviewer concerns, author replies, and decision context.

If the paper came from a previous collection stage, prefer consuming the already downloaded local OpenReview bundle from the project tree instead of re-searching first. The detailed report should explicitly use that local bundle when it exists.

If an ICLR paper still lacks `openreview_forum_url`, report that gap explicitly in the machine-readable output and in the human-facing report instead of silently continuing as if review context were complete.

If the paper is not from ICLR, do not force a review/rebuttal section by default unless the user explicitly asks for external peer-review context and a reliable public source exists.

## Algorithm-detail rule

For the proposed method, prefer extracting more than a short summary. Capture:

- model form
- architecture summary
- key modules
- training pipeline
- inference pipeline
- optimization objectives
- communication or deployment path when relevant

Also analyze how the paper narrows the gap between motivation and final algorithm. Explicitly look for:

- small experiments
- probe experiments
- pilot or trial model designs
- explanatory ablations
- toy examples that clarify the update path
- visualizations used to justify the mechanism

When summarizing the proposed method, do all of the following when the source materials allow it:

- define the major symbols before relying on them
- separate novel steps from inherited steps
- state where each step gets its input and where its output is consumed
- give at least one concrete worked example of the algorithm or pipeline
- connect each major step back to the motivation it is meant to satisfy

For experiments, also require:

- explicit mapping from each baseline back to the related-work families introduced earlier
- explicit statement of why each experiment block exists
- explicit note of surprising, unstable, or controversial findings
- explicit discussion of whether the evidence supports only local gains or a broader scientific claim

For each one, state what claim it is trying to support and whether it really makes the final method more convincing.

Example:

- if the paper uses `LoRA`, check whether that points upward to feature alignment, shared-subspace design, or interface-stable transfer
- if the new method later depends on cross-family alignment, record alignment as an upper problem even if the paper only framed it as an implementation detail

## No new retrieval rule inside deep reading

This stage must not reopen external retrieval.

Do not, inside this stage:

- reopen author-team search on academic sites
- start fresh related-paper harvesting
- search GitHub for workflow borrowing
- widen source discovery beyond what the uploaded upstream bundle already delivered

Instead:

- reuse upstream source_record.json, routing_status.json, project_directory_index.json, and any already downloaded review / rebuttal bundle
- if upstream materials already contain author-team notes, summarize them
- if author-team continuation context is missing, mark it as an upstream gap and defer it back to the download / collection stages
- if you notice a retrieval weakness, record it as a follow-up need rather than solving it here

## Report layering rule

For human-facing reading output, keep one authoritative report file.

- The detailed report should be the main report.
- Intermediate Markdown should only be a staging or audit artifact.
- If intermediate Markdown exists, its structured additions should be merged into the main detailed report rather than kept as a second parallel final report.
- In the final Project `sources` refresh bundle, prefer intermediate JSON only; do not include intermediate Markdown unless the user explicitly wants audit traces.

## Important constraint

ChatGPT canvas should prefer standard-library-safe scripts and source files already placed in `sources`.

If PDF rendering, OCR, or local figure extraction has already been done outside ChatGPT, ask the user to upload:

- `visual_manifest.json`
- extracted page images
- intermediate JSON / Markdown

Preferred OCR preprocessing order before upload:

- `RapidOCR`
- `Tesseract + pytesseract`
- `EasyOCR`

If the local OCR chain is unavailable, upload the rendered page images anyway and let ChatGPT continue with PDF text layer, captions, and nearby blocks.

Do not keep OCR lines, OCR block parsing, or figure-analysis confidence in the default final artifacts unless the user explicitly wants OCR audit traces.

When a local preprocessing batch is already finished, only upload final artifacts into Project `sources`.
Do not upload probe or test-only OCR directories such as `visuals_test` or `visuals_easyocr_probe*`.
Prefer a final bundle that contains:

- final `visual_manifest.json`
- the final `visuals/pages/` directory if the Markdown still references those images
- final intermediate JSON
- final detailed Markdown / PDF
- final PDFs
- final comparison tables or graph-seed JSON files
- final project directory index JSON / Markdown

Before handing the bundle to the next stage, run:

- `scripts/validate_detailed_report_structure.py`
- `scripts/build_paper_deep_reading_bundle.py`

Do not assume ChatGPT can access local files outside Project `sources`.

## Use

- `workflow/01_request_sources.md`
- `workflow/02_extract_structure.md`
- `workflow/03_figure_and_table_analysis.md`
- `workflow/04_gap_mining_and_graph.md`
- `workflow/05_extended_argument_and_innovation_audit.md`
- `workflow/06_teaching_explainer_preparation.md`
- `workflow/07_talk_qa_rehearsal.md`
- `workflow/08_staged_cartoon_visual_storyboard.md`
- `workflow/09_storyboard_pdf_assembly.md`
- `scripts/assemble_storyboard_pdf.py`
- `schemas/paper_focus_spec.template.json`
- `schemas/detailed_report_contract.md`
- `schemas/detailed_report_required_sections.json`
- `schemas/per_paper_output_layout.md`
- `schemas/project_directory_index_spec.md`
- `schemas/project_directory_annotations.template.json`
- `schemas/motivation_bridge_analysis.md`
- `schemas/research_generative_overlay.md`
- `schemas/reproducibility_defense_quality_overlay.md`
- `schemas/teaching_explanation_overlay.md`
- `schemas/cartoon_storyboard_continuity_quality_overlay.md`
- `schemas/visual_source_grounding_anti_hallucination_overlay.md`
- `schemas/teaching_explanation_spec.template.json`
- `schemas/external_best_practices_sources.md`
- `schemas/routing_status_template.json`
- `schemas/sources_zip_layout.md`
- `schemas/sources_refresh_templates.md`
- `scripts/build_canvas_deepread_intermediate.py`
- `scripts/init_paper_deep_reading_scaffold.py`
- `scripts/build_paper_deep_reading_bundle.py`
- `scripts/validate_detailed_report_structure.py`
- `scripts/update_project_directory_index.py`
- `scripts/update_routing_status.py`

## Reply footer rule

At the end of every substantive reply, append:

- `Current Status`
- `Possible User Inputs For Next Stage`

## Batch Completeness Rule

- Deep-read every paper in `metadata/paper_batch_manifest.json`. Do not select-read only part of the batch.
- Each paper must produce one authoritative per-paper detailed report plus the expected machine-readable intermediate artifact.
- If a paper is from `ICLR`, consume the already-downloaded local OpenReview review / rebuttal bundle instead of skipping review context.
- Before handoff, run `scripts/validate_detailed_report_structure.py`. That validator should fail if any paper in the batch still lacks its authoritative report.
- The handoff bundle should also include the current status description and the project directory description so the next session can resume from the zip alone.

## Next-Stage Handoff

- Next-stage function: mine directions and innovation points from authoritative deep-read outputs, then build the graph workspace
- Pass forward from this stage:
  - `*_detailed_cn.md`
  - `*_detailed_cn.pdf`
  - `intermediate/*.json`
  - visual manifests and final figure-analysis artifacts when available
  - derivative teaching sidecars under `generated/teaching/` when generated
  - the refreshed deep-read bundle uploaded back into Project `sources`
- `metadata/query_spec.json`
- `metadata/paper_batch_manifest.json`
- `metadata/delivery_bundle_manifest.json`
- `metadata/routing_status.json`
- `metadata/project_directory_index.json`
- `reports/project_directory_index.md`
- `reports/stage_delivery_handoff.md`
- the complete refreshed zip bundle uploaded back into Project `sources`
- Next-stage user may need to provide:
  - `research_subfield` or a confirmed direction label
  - which candidate starting nodes or expansion branches to activate
  - optional `budget` / `hardware` information before ranking directions
  - whether the next graph stage should only list unranked candidate directions or produce a ranked priority table
- Next stage should reference these state fields first:
  - `paper_id`
  - `paper_title`
    - `key_artifacts`
    - `blockers`
    - and consult `metadata/project_directory_index.json` before searching the tree ad hoc
