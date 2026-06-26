# Workflow and State Contract

Version: 1.2.0

This skill uses the `research-paper-figure-skill-factory` v1.0.1 candidate-image bridge. It must not stop at text candidates.

## Required Workflow

| Step | Mode | Purpose | Output |
|---|---|---|---|
| S0 | STARTUP_PLAN_ONLY (TEXT_ONLY) | Startup plan only | Startup plan |
| P1 | TEXT_ONLY | Intake target-paper material, slot, constraints, and optional sample images | Material status |
| P2 | TEXT_ONLY | Diagnose framework-figure need and multi-label subtype routing | Subtype candidates |
| P3 | TEXT_ONLY | Define reader effect and produce 4-6 text candidates, normally 6 | Text candidate schemes |
| P4 | TEXT_ONLY | Set up visual candidate board | Candidate-board brief |
| P5 | IMAGE_ONLY | Generate/display 4-6 candidate images or schematic candidates, normally 6 | Image candidates only |
| P6 | TEXT_ONLY | Record candidate batch, compare, and lock/revise direction | Selected/revised direction |
| P7 | TEXT_ONLY | Build final content architecture and formal image brief | Final image brief |
| P8 | IMAGE_ONLY | Generate formal figure candidate or revision batch | Formal images only |
| P9 | TEXT_ONLY | Review, refine, caption, legend, and body text | Final paper text package |

## Candidate-Image Bridge

After any text reply with multiple schemes, layouts, styles, metaphors, density levels, subtypes, or prompt alternatives:

1. The first recommended next prompt must ask to generate/display candidate images or schematic candidates, normally 6.
2. The next text step must set up the board unless the user already supplied count, varied axis, fixed elements, and route.
3. The following response must be `IMAGE_ONLY`.
4. The next text response must record the image batch before final prompt or caption work.

Skipping is allowed only when the user explicitly says to stay text-only. Record `visual_candidate_board_skipped_by_user: true`.

## Every Text Reply

Every `TEXT_ONLY` reply must include:

- `当前执行计划`
- substantive work
- `默认推荐`
- `当前状态与产物`
- `下一步你可以这样问`

The footer must list:

- current mode and current step;
- all steps plus current position;
- current-turn outputs;
- cumulative outputs;
- pending outputs;
- material/sample-image status;
- text candidate count;
- candidate-board status;
- candidate image batch ID when available;
- selected visual candidate when available;
- previous `IMAGE_ONLY` output recording status;
- next recommended action.

## Image-Only Turns

P5 and P8 are image-only. They contain only native image generation/artifacts. No prose, no state footer, no caption, no critique.
