# Paper Deep Reading Teaching Explainer Skill v10.1.8

This package is a Clawhub/OpenClaw-friendly source skill for deep paper reading.

## What changed in v10

This version keeps the v9 `Research-Generative Paper Reading` lens and adds a new `Teaching-Explainer Paper Reading` lens without weakening any original requirement.

The skill now asks every paper reading report to do two things at once:

1. produce a rigorous, paper-grounded deep reading report; and
2. reverse-engineer how the paper could generate new research ideas; and
3. turn the deep read into material that helps the user explain, discuss, defend, and teach the paper to others.

## Core research-generative lens

Every report should identify:

```text
Paper = Important Setting
      + Broken Assumption
      + Borrowed Tool
      + New Constraint
      + Surrogate Mechanism
```

And should explicitly answer:

```text
What ideal mechanism Y is unavailable here?
What surrogate Z did the paper construct?
Which hidden assumption H_i makes Z fragile?
What new idea appears under not-H_i?
```

## Main files

- `SKILL.md`: main skill instructions.
- `schemas/detailed_report_contract.md`: authoritative report contract.
- `schemas/detailed_report_required_sections.json`: headings checked by validators.
- `schemas/research_generative_overlay.md`: full research-generative overlay.
- `workflow/`: staged reading workflow.
- `scripts/`: scaffold, validation, and bundle-building helpers.

## Recommended use

Upload this zip as the updated paper deep reading skill source. For each paper, generate one authoritative detailed report and run the validator before handoff.


## Core teaching-explainer lens

Every report should also produce:

```text
Before -> Pain -> Broken Assumption -> Key Replacement -> Mechanism -> Evidence -> Caveat -> Next Idea
```

And must include:

- audience map and teaching goal;
- 30-second / 3-minute / 10-minute summaries;
- formula, figure/table, and experiment teaching scripts;
- blackboard derivation and toy example;
- role-play discussion prompts;
- Q&A and defense bank;
- misunderstanding guardrails;
- slide/talk blueprint;
- three takeaways.

## New v10 files

- `schemas/teaching_explanation_overlay.md`
- `schemas/teaching_explanation_spec.template.json`
- `schemas/external_best_practices_sources.md`
- `schemas/reproducibility_defense_quality_overlay.md`
- `workflow/06_teaching_explainer_preparation.md`
- `workflow/07_talk_qa_rehearsal.md`


## Staged visual storyboard extension

After the complete text-only deep-reading report is delivered, this skill can continue with staged cartoon storyboard generation. The visual workflow is split into separate user-triggered steps: background/old-method defects, algorithm modules, experiments, limitations/defense, future directions, and presentation packaging.

Important constraints:

- The first skill run outputs only the plan, complete report, status, and next-step prompts; it must not generate images.
- Text report/status and image generation must not be mixed in the same assistant response.
- For ChatGPT web/app, use Create image. For Codex/Claude Code-style environments, prefer the `imagegen` skill when available; otherwise use ChatGPT Images 2.0 API or another available image-generation API.
- Do not generate SVG diagrams as a substitute for the requested cartoon-comic storyboard images.
- Storyboard image steps may be grounded in the uploaded PDF, LaTeX source, or both. If both exist, use PDF for rendered visual evidence and LaTeX for exact captions, labels, formulas, figure paths, and surrounding text.
- Multi-image prompt batches must include continuity and cinematography guidance: image order, camera/framing, transition logic, style bible, symbol bible, and consistency with prior batches.
- Because sessions may be stateless, users should resume with prompts such as: `使用这个skill，根据状态，执行第2步：生成算法整体流程与各模块解释的连续卡通图。`


## v10.1.8 ClawHub packaging update

This package is prepared for ClawHub/OpenClaw publication under the slug `paper-deep-reading-teaching-explainer`.

v10.1.8 removes the fixed next-skill recommendation footer. Status replies should now focus on `Current Status` and `Possible User Inputs For Next Stage`. When suggesting how to continue cartoon generation, the prompt must explicitly tell the user to say `生成多张连续的卡通图`.

v10.1.7 adds a multi-image decomposition rule for storyboard generation. Each requested visual part should be split into several 16:9 cartoon images with one prompt per image and one main teaching point per image. The skill should not compress background, algorithm, experiments, limitations, and future directions into one crowded all-in-one picture.

v10.1.6 adds a source-grounding anti-hallucination check for storyboard image prompts and generated images. Before image generation, prompts must be checked against the original PDF/LaTeX and the authoritative deep-reading report; unsupported facts must be removed, marked `not reported`, or sent back to the user for evidence. After image generation, suspect images must be corrected before PDF assembly.

v10.1.5 adds a continuity / cinematography quality overlay for staged cartoon image prompts. Whenever the assistant writes prompts for multiple continuous cartoon images, each batch must preserve sequence order, camera movement, visual style, characters, symbols, data-flow direction, evidence labels, and narrative logic. Follow-up batches must continue the established storyboard bible from previous images.

v10.1.4 adds a reproducibility / defense / teaching quality overlay. Reports and storyboards must explain key concepts as intuition -> formula -> example -> limitation, expose module inputs/outputs/symbols/dimensions/parameters/data flow, separate paper-stated facts from inference, audit missing experimental details, and include a complete numeric training/inference walkthrough.

v10.1.3 removes `.clawhubignore` and `LICENSE` from the ClawHub upload zip because ClawHub may reject extensionless or dotfiles during its non-text-file check. The package still declares MIT-0 in metadata and documentation.

v10.1.2 supplements the coding-agent image-generation guidance: in Codex-style environments, prefer the `imagegen` skill when available; fall back to ChatGPT Images 2.0 API or another approved image-generation API only when needed.

### Staged cartoon storyboard + final PDF flow

The skill now supports a strict staged visual workflow:

0. First run: plan + complete text-only deep-reading report + status + next-step prompts. No images.
1. Background, old-method defects, paper problem, and inspiration storyboard.
2. Algorithm overview and module-by-module storyboard.
3. Experiment section storyboard.
4. Limitations and defense storyboard.
5. Future directions and innovation graph storyboard.
6. Cover, summary, and Q&A backup storyboard.
7. Final assembly: combine all approved storyboard images into a single 16:9 PDF.

### Platform notes

- ChatGPT web/app: use Create image for image generation.
- Codex / Claude Code / coding-agent environments: prefer the `imagegen` skill when available; otherwise use ChatGPT Images 2.0 API or another approved image-generation API.
- Do not use SVG diagrams as a replacement for cartoon-comic storyboard images.
- Storyboard source basis can be PDF, LaTeX, or PDF+LaTeX; keep visual claims traceable to these sources or to the authoritative report derived from them.
- Each visual step should be split into multiple images by default. Do not compress a whole section into one dense collage unless the user explicitly asks for a single overview.
- Prompt-only handoff and direct image generation both need a continuity/cinematography block for multi-image batches.
- Prompt-only handoff and direct image generation both need an anti-hallucination checklist against the original paper and authoritative report.
- The PDF assembly step uses existing images only and may use `scripts/assemble_storyboard_pdf.py`.

### Resume prompt pattern

```text
使用这个skill，根据状态，执行第X步：<阶段名称>。
```

If unsure:

```text
使用这个skill，根据状态，告知下一步应该问什么。
```
