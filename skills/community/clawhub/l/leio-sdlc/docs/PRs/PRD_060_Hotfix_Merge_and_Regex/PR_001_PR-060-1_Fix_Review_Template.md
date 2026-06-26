status: completed

---
status: completed
title: Fix Review Template and Reviewer Prompt
---
# PR-060-1: Fix Review Template and Reviewer Prompt

## Objective
Prevent false positive LGTM evaluations by removing hardcoded tags from the review template and enforcing strict tag output in the reviewer prompt.

## Tasks
1. Update `TEMPLATES/Review_Report.md.template`:
   - Remove the literal strings `[LGTM]` and `[ACTION_REQUIRED]`.
   - Under `## Verdict`, replace the checkboxes with a placeholder instruction: `(Write exactly [LGTM] or [ACTION_REQUIRED] here)`.
2. Update `scripts/spawn_reviewer.py`:
   - Strengthen the System Prompt to emphasize: "You must output EXACTLY one status tag in the Verdict section: either `[LGTM]` or `[ACTION_REQUIRED]`. Do not output both."
