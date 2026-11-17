## Description:

Tracks AI API usage by logging calls, reporting spending by model and period, and suggesting cheaper models to optimize costs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odinbot33](https://clawhub.ai/user/odinbot33)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to track local AI API usage, estimate spend from model and token counts, review spending by model or task, and identify cheaper routing options for simple work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local usage logs can contain model names, token counts, costs, task labels, sources, and user-provided descriptions.

Mitigation: Avoid recording prompts, secrets, customer data, or proprietary details in descriptions; review or delete usage.jsonl when it is no longer needed.

Risk: Cost estimates depend on pricing.json and may become inaccurate as provider prices change.

Mitigation: Review and update pricing.json before relying on reports for budgeting or routing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odinbot33/skills/oee-ai-cost-tracker)
- [ClawHub publisher profile](https://clawhub.ai/user/odinbot33)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; generated tracker data is local JSONL and CLI text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local pricing.json model rates and writes usage entries to a local usage.jsonl file.]

## Skill Version(s):

1.0.0 (source: server release metadata, created 2026-02-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
