# Media Generation - MiniMax

Use this file when the user needs MiniMax-driven video or music generation, or when a multimodal workflow includes queued output retrieval.

## Mental Model

Video and music jobs are operationally closer to render queues than to chat completions.
Plan four phases:
1. prepare payload
2. submit job
3. poll status
4. fetch and validate output

## Current Routing Notes

- `Hailuo 2.3` is the current MiniMax-branded video lane to consider for motion-heavy work
- `Music 2.5` is the current MiniMax music lane to consider for music-first generation
- verify the exact currently documented model name and request shape before hardcoding production calls

## Design Rules

### Prompt and Asset Packaging
- separate subject, action, timing, and style when the modality benefits from compositional prompts
- record which assets are mandatory, optional, or forbidden before submitting the job
- keep a copy of the smallest successful prompt for reruns

### Polling Behavior
- use bounded polling intervals instead of tight loops
- stop with a user-visible status if the queue runs too long
- distinguish between queue delay, processing failure, and fetch failure

### Output Validation
- confirm duration, aspect ratio, format, and output URL before claiming success
- if the result is close but wrong, change the smallest useful variable first
- do not rerun blindly when the real problem is asset mismatch or wrong duration target

## Safety Boundaries

- confirm rights for images, music references, lyrics, logos, and character likenesses before upload
- treat long-running generation as paid remote compute and keep the user informed
- avoid hidden rerun loops that can burn credits without consent
