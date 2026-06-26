---
name: prediction_market_smoke_test
description: A minimal test skill for prediction-market workflows. Use when the user wants a quick checklist for evaluating a prediction market, drafting a thesis, or testing that this skill installs correctly from ClawHub.
---

# Prediction Market Smoke Test

This is a minimal publish-and-install test skill.

Use this skill when the user wants to:
- sanity-check whether a prediction market question is well-formed
- draft a quick trading thesis before opening a position
- verify that this skill can be installed from ClawHub

## Quick Workflow

When this skill is used, follow this short workflow:

1. Restate the market question in one sentence.
2. Identify the resolution source and what event would count as a YES result.
3. List the top 3 reasons the market may be mispriced.
4. Give a one-paragraph bullish case and one-paragraph bearish case.
5. End with a concise checklist:
   - resolution source confirmed
   - time to resolution understood
   - major ambiguity checked
   - current thesis stated clearly

## Output Template

Use this structure when helpful:

### Market Summary
- Question:
- YES means:
- Resolution source:
- Deadline:

### Possible Edge
- Reason 1:
- Reason 2:
- Reason 3:

### Bull Case

### Bear Case

### Final Checklist
- Resolution source confirmed
- Ambiguity reviewed
- Thesis written

## Notes

- This skill is intentionally simple so it is easy to publish, install, and validate.
- After confirming this works through ClawHub, you can replace it with your real prediction-market skill.
