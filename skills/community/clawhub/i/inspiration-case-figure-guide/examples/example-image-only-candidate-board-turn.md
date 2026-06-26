# Example IMAGE_ONLY Candidate Board Turn

This file documents the expected P5 behavior. The actual P5 reply must contain only generated image artifacts.

Expected constraints:

- mode: `IMAGE_ONLY`
- no prose
- no state footer
- no caption
- no critique
- candidate count: 4-6, normally 6
- rendering route: ChatGPT web Create image / ChatGPT Images 2.0, or Codex `$imagegen` first with approved API fallback

The next `TEXT_ONLY` reply after this turn must record `candidate_image_batch_id` and review the candidates.
