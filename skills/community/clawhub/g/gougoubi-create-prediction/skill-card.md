## Description:

Create public Gougoubi prediction proposals from minimal input with deterministic enrichment, group creation, approval handling, and transaction submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to publish new Gougoubi public prediction markets from a market name and deadline while the agent enriches rules, tags, group details, approvals, and transaction submission steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated market rules, tags, stake amount, language fallback, or group details may not match the user's intent for a public prediction market.

Mitigation: Review those generated fields before allowing the proposal creation flow to continue.

Risk: The workflow includes crypto approval and transaction submission steps.

Mitigation: Do not auto-confirm wallet actions; inspect every approval and transaction before confirming.

Risk: A proposal with moderation concerns could be published publicly.

Mitigation: Require user confirmation when moderation risk is detected.

## Reference(s):

- [Gougoubi public proposal creation page](https://gougoubi.ai/premarket/proposals/create/public)
- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-create-prediction)
- [Publisher profile](https://clawhub.ai/user/chinasong)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON with concise status, warning, and confirmation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes transaction hash, proposal address when available, normalized input, warnings, or a retryable failure stage.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
