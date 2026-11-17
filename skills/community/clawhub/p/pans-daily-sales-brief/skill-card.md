## Description:

Pans Daily Sales Brief generates daily AI compute sales briefs covering follow-ups, expiring contracts, new leads, performance metrics, and competitor news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashiming](https://clawhub.ai/user/dashiming)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and business operators use this skill to maintain local pipeline data and generate daily sales briefings for customer follow-up, contract renewal, lead tracking, performance review, and competitor monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify local customer, contract, lead, competitor, and sales statistics data.

Mitigation: Use non-sensitive or backed-up pipeline data and review generated updates before relying on them for sales operations.

Risk: Write and competitor-search operations depend on local helper scripts outside the reviewed package.

Mitigation: Review the local helper scripts and installed search skill before enabling write operations or competitor-news searches.

Risk: Sales pipeline records may contain customer, contract, and revenue information.

Mitigation: Avoid storing confidential business data unless the local environment and retention practices are approved for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashiming/skills/pans-daily-sales-brief)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Plain text or JSON sales brief output with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list, add, and update local customer, contract, lead, competitor, and sales statistics records.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
