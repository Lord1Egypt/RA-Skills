# Review Rubric

Use this rubric in P6 and P9.

## Inspiration Clarity

- Does the figure answer "why is this paper needed?"
- Is the case, failure, observation, or contrast visible in the first few seconds?
- Is the figure anchored to one reader question rather than multiple vague goals?

## Evidence Integrity

- Are all examples, metrics, screenshots, outputs, and labels supplied by the paper or the user?
- Does the figure avoid invented results, fake charts, fake UI, and unsupported causal claims?
- If the figure uses a metaphor, is the metaphor clearly tied back to the paper's evidence?

## Paper Fit

- Does the selected subtype match the paper slot?
- Would the figure work as a first figure, intro teaser, method lead-in, limitation figure, or rebuttal exhibit?
- Is the density appropriate for the venue and page space?

## Visual Legibility

- Is there a stable reading order?
- Are labels short and exact?
- Are colors semantic rather than decorative?
- Are callouts placed near the evidence they explain?

## Candidate Bridge Compliance

Fail review if:

- text candidates lead directly to final prompt, final image, or caption;
- P4 setup is missing after multi-option text;
- P5 is not `IMAGE_ONLY`;
- P6 does not record and compare the image batch;
- state omits `visual_candidate_board_status`, `candidate_image_batch_id`, or `selected_visual_candidate`.

## Default Recommendation Rule

When multiple options exist, recommend the candidate that makes the inspiration source most concrete while preserving evidence integrity. Prefer a slightly plainer but truthful figure over a visually dramatic unsupported one.
