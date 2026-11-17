## Description:

Analyzes Amazon keyword-level competition, search popularity, product counts, advertising counts, and supply-demand ratio using LinkFox SIF data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and e-commerce operators use this skill to query Amazon keyword competition metrics and compare supply-demand conditions, search popularity, product counts, and ad competition for supported marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is marked suspicious by clawscan because it handles keyword queries, account onboarding details, phone/SMS verification data, API keys, paid plan/payment workflows, endpoint overrides, and automatic feedback behavior.

Mitigation: Install only if you trust LinkFox with those data flows, obtain and store API keys through official account pages or a secret manager, avoid endpoint override environment variables, review payment orders before paying, and require explicit consent before feedback submission.

Risk: API calls consume paid LinkFox credits and payment onboarding can create purchase orders.

Mitigation: Confirm the user's intent before repeated or exploratory calls, show credit/payment implications before continuing, and have the user review any generated payment order.

Risk: Full API responses are written to a local session data directory and may contain commercially sensitive keyword research.

Mitigation: Run the skill only in trusted workspaces and avoid sharing saved response files unless the user intends to disclose the keyword research.

## Reference(s):

- [SIF keyword overview API reference](references/api.md)
- [Authentication and billing onboarding](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-sif-keyword-overview)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parameters, shell commands, tabular analysis, and saved JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill queries one keyword per API call, supports 13 Amazon marketplaces, caches identical calls for 24 hours, and saves full API responses under a local linkfox session data directory.]

## Skill Version(s):

1.0.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
