# Runtime Playbook - Google Colab

## Runtime Selection Heuristics

| Goal | Preferred Runtime | Notes |
|------|-------------------|-------|
| Data cleaning and EDA | CPU | Faster startup, lower cost |
| Small model training | T4 or equivalent | Good baseline for quick iterations |
| Large model fine-tuning | L4/A100 class | Use only with explicit budget guardrails |
| Teaching and demos | CPU or T4 | Favor reproducibility over raw speed |

## Rehydration After Disconnect

When runtime resets:

1. Re-run environment cell and reinstall pinned packages.
2. Re-mount data sources and verify path existence.
3. Re-load checkpoints rather than restarting training from zero.
4. Validate random seed and split method before resuming.

## Dependency Hygiene

- Use pinned versions for non-standard libraries.
- Group installs in one cell to avoid hidden version drift.
- Save `pip freeze` snapshot for significant runs.

## Escalation Rule

If the same import or runtime failure repeats 3 times, pause and move to root-cause analysis instead of repeated ad hoc fixes.
