---
name: jev-ai-decision-workflow
description: Design and review typed AI decisions with Yes/No, Choice, or Score outputs. Use for classification, routing, moderation, triage, qualification, guardrails, batch decision planning, result review, and Jev AI integration; require representative evaluation and human review for consequential decisions.
metadata:
  openclaw:
    homepage: https://ai-jev.pro/what-is-jev
    version: 1.0.0
---

# Jev AI Decision Workflow

Turn repeated text decisions into inspectable Yes/No, Choice, or Score workflows. This Skill is text-only by default. Its optional MCP is deterministic and read-only: it does not call models, access accounts, consume credits, submit jobs, read private data, or make decisions for the user.

## Define the decision

State the input record, exact question, output type, allowed choices or score range, decision criteria, and risk level. Keep one decision field focused on one operational question. Split compound questions when different answers could be correct for different parts.

For high-risk employment, financial, medical, legal, safety, security, or trust decisions, make human review mandatory. Do not turn a probability into permission for an irreversible action.

## Prepare evidence

Build a representative labeled dataset that includes ordinary cases, rare classes, ambiguous inputs, adversarial wording, missing context, and expected escalations. Measure errors by class or score band. A provider-reported probability is an estimate; do not call it calibrated confidence without calibration evidence.

## Use the optional MCP

- `build_typed_decision_spec` checks the question, schema, criteria, and risk controls.
- `validate_decision_batch` checks ids, empty inputs, duplicates, and size limits without sending records anywhere.
- `review_typed_decision_result` checks evidence, completeness, probability presence, and escalation rules.
- `get_jev_ai_resources` returns canonical public Jev AI pages.

Connect the stdio server with:

```bash
openclaw mcp add jev-ai \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/jev-ai-decision-workflow-mcp \
  --include 'build_typed_decision_spec,validate_decision_batch,review_typed_decision_result,get_jev_ai_resources'
```

Then run `openclaw mcp doctor jev-ai --probe`. If the installed release lacks that command group, add `npx -y github:gpt-img-2/jev-ai-decision-workflow-mcp` as a Stdio server in MCP settings. Never imply the MCP or Jev AI ran when it did not.

## Return an inspectable result

Return `Decision`, `Input`, `Output schema`, `Criteria`, `Risk`, `Test set`, `Metrics`, `Escalation`, `Known limits`, and `Next verification`. Distinguish observed results from product claims and unknowns.

## Canonical resources

- Playground: https://ai-jev.pro/
- Jev API: https://ai-jev.pro/jev-api
- Batch processing: https://ai-jev.pro/batch
- What is Jev?: https://ai-jev.pro/what-is-jev
- Pricing: https://ai-jev.pro/pricing
- About: https://ai-jev.pro/about
- Privacy: https://ai-jev.pro/privacy-policy
- Terms: https://ai-jev.pro/terms-of-service
- Raw Skill: https://ai-jev.pro/skills/jev-ai-decision-workflow/SKILL.md
- MCP source: https://github.com/gpt-img-2/jev-ai-decision-workflow-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/jev-ai-decision-workflow
