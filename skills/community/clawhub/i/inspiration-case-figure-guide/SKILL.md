---
name: inspiration-case-figure-guide
license: MIT-0
description: "Use when the user wants to design, prompt, generate, critique, or integrate publication-ready research-paper inspiration figures: motivating examples, problem-teaser figures, failure cases, before/after contrast panels, observation-to-method case stories, reviewer-facing limitation cases, and introduction figures that explain why a paper is needed. Generated from research-paper-figure-skill-factory v1.0.1 with full-feasible local PDF evidence, startup-plan-only first replies, strict text/image separation, mandatory text-candidate to visual-candidate setup to IMAGE_ONLY candidate-board to candidate-review workflow, optional sample images, ChatGPT web Create image / ChatGPT Images 2.0, Codex $imagegen first, all-step/current-position state footers, and next-question help in every text reply."
metadata:
  display_name: Inspiration Case Figure Guide
  version: "3.0.0"
  author: OpenAI
  tags:
    - research-figure
    - inspiration-figure
    - motivating-example
    - case-walkthrough
    - failure-case
    - intro-figure
    - candidate-image-bridge
    - imagegen
    - chatgpt-images-2
    - clawhub
    - openclaw
  compatibility: Codex, ChatGPT web, OpenClaw, ClawHub marketplace. Requires image-generation capability for rendering.
  openclaw:
    skillKey: inspiration-case-figure-guide
---

# Inspiration Case Figure Guide

This skill designs publication-ready raster figures that make a paper's inspiration legible. Use it for introduction or analysis figures that show the motivating case, surprising observation, failure example, before/after contrast, limitation boundary, or concrete scenario that explains why the paper exists.

It was generated with `research-paper-figure-skill-factory` v1.0.1 from the project-local full-feasible diagram corpus: 7,631 local PDF records processed, 0 skipped, 146,071 figure captions extracted, 119,534 diagram-relevant captions, and 93,088 multi-label figure records. The inspiration/case evidence subset contains 48,536 keyword-and-label matched records across 7,021 papers, including 2,958 papers where the relevant signal appears in the first figure. Representative rendered pages are audit aids only, not the corpus size.

## Non-Negotiable Contract

### First Trigger

On the first reply in a new project, output only a startup plan. Do not analyze the paper, draft prompts, create captions, or generate images. The first reply is `STARTUP_PLAN_ONLY (TEXT_ONLY)` and must ask the user to confirm or provide material for P1.

If the first user message asks to "直接出图", "生成 6 张图", "出候选图", "generate images", or otherwise asks for image generation, record the request as pending only. The first reply must not call `$imagegen`, Create image, an image API, or include image markdown/artifacts.

### Mandatory Candidate-Image Bridge

After any multi-option text decision, do not move directly to final prompt, final image generation, caption, or text-only direction lock. Use this mandatory bridge:

1. `TEXT_ONLY` text-candidate turn: present 4-6 text candidates, normally 6.
2. `TEXT_ONLY` visual candidate-board setup: define candidate count, varied axis, fixed elements, rendering route, and comparison criteria.
3. `IMAGE_ONLY` candidate-board generation: generate/display 4-6 candidate images or schematic candidates, normally 6.
4. `TEXT_ONLY` candidate review: record the image batch, compare candidates, recommend one direction, and ask the user to select, revise, combine, or request another board.

This bridge is mandatory after candidate schemes, subtype choices, layout choices, style choices, metaphor choices, density choices, and prompt alternatives. Skip it only if the user explicitly says to stay text-only or skip image candidates, then record `visual_candidate_board_skipped_by_user: true`.

### Strict Text/Image Separation

Every assistant response is exactly one mode:

- `TEXT_ONLY`: planning, intake, diagnosis, candidate text, candidate-board setup, prompt writing, critique, state update, and confirmation request.
- `IMAGE_ONLY`: image generation only. No prose, caption, prompt text, critique, or state footer.

If a reply emits visible text, do not generate images in the same response. If generation is ready, ask for confirmation and stop. If the user has confirmed generation and state is sufficient, the next assistant reply may be `IMAGE_ONLY` only.

### Rendering Route

For candidate boards, drafts, final diagrams, and revisions:

1. In ChatGPT web, use **Create image** through **ChatGPT Images 2.0**.
2. In Codex, use the `$imagegen` skill first.
3. If `$imagegen` is unavailable in Codex, use ChatGPT Images 2.0 API or another approved image-generation API.
4. Native bitmap outputs such as PNG, JPG, JPEG, or WebP are allowed.
5. Do not use SVG, Mermaid, TikZ, Graphviz, HTML/CSS, canvas, matplotlib, filesystem code drawing, or code-rendered/exported images as candidate, draft, final, or fallback visuals.

### Every Text Reply

Every `TEXT_ONLY` reply must include these sections in order:

1. `当前执行计划`
2. The substantive work for the current step
3. `默认推荐`
4. `当前状态与产物`
5. `下一步你可以这样问`

The state footer must include `全部步骤与当前位置`, current response mode, current-turn outputs, cumulative outputs, pending outputs, candidate-board state, and the previous `IMAGE_ONLY` batch recording status.

The first copyable prompt must begin:

`请使用**inspiration-case-figure-guide**，执行，根据当前状态，下一步执行：...`

Always include this fallback prompt:

`请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。`

Normal follow-up turns continue from the active session/history. Ask for the latest `当前状态与产物` only if history is unavailable, truncated, or moved to another conversation.

## Required Workflow

| Step | Reply Type | Goal | Output |
|---|---|---|---|
| S0 | STARTUP_PLAN_ONLY (TEXT_ONLY) | Startup confirmation only | Startup plan |
| P1 | TEXT_ONLY | Intake target-paper material, target slot, inspiration source, constraints, and optional sample images | Material status |
| P2 | TEXT_ONLY | Diagnose inspiration need and multi-label subtype routing | Subtype candidates + default route |
| P3 | TEXT_ONLY | Define reader effect and produce 4-6 text candidate schemes, normally 6 | Text candidates + required visual-candidate next action |
| P4 | TEXT_ONLY | Set up visual candidate board: count, varied axis, fixed content, route, and comparison criteria | Candidate-board brief |
| P5 | IMAGE_ONLY | Generate/display 4-6 candidate images or schematic candidates, normally 6 | Candidate images only |
| P6 | TEXT_ONLY | Record the candidate image batch, compare candidates, recommend one, and lock or revise direction | Selected/revised visual direction |
| P7 | TEXT_ONLY | Build final content architecture and formal image brief/prompt for the selected direction | Final image brief |
| P8 | IMAGE_ONLY | Generate formal figure candidate or revision batch through the approved image route | Formal image candidates only |
| P9 | TEXT_ONLY | Review, refine, caption, legend, body insertion, and handoff text | Final paper text package |

P4/P5/P6 are not optional after P3 when multiple text options were presented. They are the visual selection bridge.

## Inspiration/Case Routing

Record all applicable labels before locking a primary production subtype. A single figure may be both a motivating example, mechanism spark, failure case, and evidence board.

Primary subtypes:

- `problem_teaser`: a first-viewport problem hook that makes the research gap concrete.
- `motivating_case_walkthrough`: one example moves through input, observation, failure, insight, and method need.
- `failure_to_need`: a failure or limitation case that motivates the paper's intervention.
- `before_after_contrast`: old behavior vs desired behavior or baseline vs proposed direction.
- `observation_to_hypothesis`: empirical or qualitative observation becomes a design principle.
- `scenario_storyboard`: user, system, environment, or task scenario that exposes the unresolved problem.
- `evidence_to_inspiration_board`: compact evidence tiles supporting why the idea is needed.
- `taxonomy_hook`: a small design-space or category map that reveals the missing region.
- `mechanism_spark`: an intuition diagram showing why a core mechanism should work.
- `reviewer_concern_case`: a rebuttal-facing example that clarifies a boundary, risk, or misconception.

Choose one primary subtype for the current rendering, but keep secondary labels as constraints on layout, arrows, callouts, and density.

## Candidate Defaults

- Text candidates: 4-6, normally 6.
- Candidate-board images: 4-6, normally 6.
- Formal image candidates: 4-6, normally 6 unless a selected direction needs fewer variants.
- If the user says only "继续", "出图", "生成", or "generate" after a text-candidate or board-setup turn, default to 6 candidate images.
- Generate one image only when the user explicitly asks for one.
- If a text reply presents multiple schemes, layouts, styles, metaphors, densities, or prompt options, the first recommended next prompt must ask to generate/display multiple candidate images or schematic candidates, normally 6.

## Sample / Reference Images

Sample images are optional. Ask whether the user wants to provide one or more sample/reference images before rendering. For each image, record the preferred transfer attributes:

- style
- layout
- panel rhythm
- information density
- content-detail level
- label style and label placement
- color semantics
- callout grammar
- negative reference constraints

Do not copy sample-image content, claims, data, identities, or proprietary marks unless the user explicitly owns or authorizes that content. Use samples as controllable visual references only.

## State Fields

Preserve these fields in every text reply:

- current mode and current step
- all workflow steps and current position
- material status
- paper thesis / figure thesis
- inspiration source: case, observation, failure, contrast, scenario, or intuition
- subtype labels and primary production subtype
- reader-effect contract
- exact case evidence, labels, constraints, and forbidden invented content
- sample/reference image transfer map
- text candidate count and candidate IDs
- visual candidate-board status
- visual board type, varied axis, fixed elements, candidate count
- candidate image batch ID
- visual candidate history and selected visual candidate
- final image brief status
- rendering route
- current-turn outputs, cumulative outputs, pending outputs
- whether the previous `IMAGE_ONLY` output has been recorded
- next recommended action

If history is incomplete, do not invent missing state. Ask the user to provide the latest `当前状态与产物` or the missing material.

## Evidence Guardrails

- Do not invent examples, metrics, user studies, failure rates, model outputs, or benchmark outcomes.
- If the target paper has no concrete motivating case, ask for the intended inspiration claim or create a text-only gap analysis before proposing visuals.
- Keep the inspiration figure anchored to one reader question: "Why is this paper needed?"
- The figure may be visually memorable, but the paper's claim must remain inspectable and defensible.
- For final prompts, include exact labels and forbid long paragraphs, fake charts, fake screenshots, logos, watermarks, and decorative clutter.

## References

Use these package references as needed:

- `references/workflow-and-state-contract.md`
- `references/visual-style-and-board-protocol.md`
- `references/prompt-generation-policy.md`
- `references/figure-class-taxonomy.md`
- `references/figure-pattern-library.md`
- `references/review-rubric.md`
- `references/source-corpus-notes.md`
- `references/evidence-map-index.md`
- `references/evidence-lineage-summary.md`
- `references/builder-time-acquisition-report.md`
- `references/initial-corpus-manifest.md`
- `templates/state-footer-template.md`
- `templates/figure-brief-template.md`
- `templates/prompt-template.md`
- `templates/user-input-bundle.md`
