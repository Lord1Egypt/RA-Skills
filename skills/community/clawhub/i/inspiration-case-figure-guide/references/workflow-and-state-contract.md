# Workflow And State Contract

## Response Modes

Every assistant response must be exactly one mode:

- `STARTUP_PLAN_ONLY (TEXT_ONLY)` for S0.
- `TEXT_ONLY` for P1, P2, P3, P4, P6, P7, and P9.
- `IMAGE_ONLY` for P5 and P8.

Text and image output must never be combined in one reply.

## Required Workflow

| Step | Mode | Purpose |
|---|---|---|
| S0 | STARTUP_PLAN_ONLY (TEXT_ONLY) | Show startup plan only, no analysis or images |
| P1 | TEXT_ONLY | Intake target-paper material, target slot, constraints, and optional reference images |
| P2 | TEXT_ONLY | Diagnose inspiration need and multi-label subtype routing |
| P3 | TEXT_ONLY | Define reader effect and produce 4-6 text candidate schemes, normally 6 |
| P4 | TEXT_ONLY | Set up visual candidate board |
| P5 | IMAGE_ONLY | Generate/display 4-6 candidate images or schematic candidates, normally 6 |
| P6 | TEXT_ONLY | Record candidate image batch, compare candidates, and lock/revise direction |
| P7 | TEXT_ONLY | Build final content architecture and formal image brief |
| P8 | IMAGE_ONLY | Generate formal figure candidate or revision batch |
| P9 | TEXT_ONLY | Review, caption, legend, body insertion, and handoff |

## Every TEXT_ONLY Reply

Include these sections in this order:

1. `当前执行计划`
2. substantive step output
3. `默认推荐`
4. `当前状态与产物`
5. `下一步你可以这样问`

The final section contains the only copyable next prompts. The first prompt must match the default recommendation. Always include:

`请使用**inspiration-case-figure-guide**，根据当前状态，提供下一步提问建议。`

## Mandatory Candidate-Image Bridge

After any multi-option text decision, require:

1. P3 or equivalent text options.
2. P4 `TEXT_ONLY` board setup.
3. P5 `IMAGE_ONLY` candidate-board generation.
4. P6 `TEXT_ONLY` candidate review and direction lock.

Do not let the user go directly from text candidates to final prompt, final image, caption, or text-only direction lock unless the user explicitly says to skip candidate images. Record the skip as `visual_candidate_board_skipped_by_user: true`.

## Required State Fields

Track:

- active skill and version;
- current step and response mode;
- all steps and current position;
- target paper material status;
- target paper slot;
- paper thesis and figure thesis;
- inspiration source and evidence anchors;
- subtype labels and primary production subtype;
- reader-effect contract;
- exact labels allowed;
- forbidden invented content;
- sample/reference image transfer map;
- text candidate count and candidate IDs;
- visual candidate-board status;
- board type, varied axis, fixed elements, candidate count, comparison criteria;
- candidate image batch ID and history;
- selected visual candidate;
- final prompt/brief status;
- previous `IMAGE_ONLY` batch recording status;
- current-turn outputs, cumulative outputs, and pending outputs.

## State Recovery

Continue from active session history by default. If history is unavailable, ask for the latest `当前状态与产物` footer. Do not invent missing state.
