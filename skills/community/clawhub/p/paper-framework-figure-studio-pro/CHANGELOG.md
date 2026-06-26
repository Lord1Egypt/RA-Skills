# Changelog

## 1.2.0

- Regenerated from `research-paper-figure-skill-factory` v1.0.1.
- Replaced the old S0/P1-P8 workflow with S0/P1-P9.
- Added mandatory candidate-image bridge after multi-option text decisions:
  - P4 `TEXT_ONLY` visual candidate-board setup;
  - P5 `IMAGE_ONLY` candidate-board generation;
  - P6 `TEXT_ONLY` candidate review and direction lock/revision.
- Added validation rule that the skill must not move from 4-6 text candidates directly to final prompt, final generation, or caption unless the user explicitly skips image candidates.
- Updated metadata, agent rules, workflow/state contract, prompt policy, templates, examples, publish files, and release checklist.

## 1.1.0

- Generated as `paper-framework-figure-studio-pro` from `research-paper-figure-skill-factory` v1.0.0.
- Added full-feasible corpus coverage contract: 7,631 candidate/accessible/processed PDFs, 0 skipped PDFs, and 93,088 multi-label diagram records.
- Enforced first-trigger behavior and text/image turn separation.
