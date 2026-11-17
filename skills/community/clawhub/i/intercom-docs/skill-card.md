## Description:

Create, update, improve, and review Intercom help-center and support documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgelewi5](https://clawhub.ai/user/georgelewi5)

### License/Terms of Use:

MIT-0

## Use Case:

External documentation authors, support teams, and developers use this skill to draft, revise, audit, and maintain Intercom help-center content from product, support, codebase, or existing article context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Intercom workspace access tokens can expose or modify help-center content if mishandled.

Mitigation: Treat tokens as passwords, avoid writing them into docs or commits, and prefer read-only inspection before proposing any changes.

Risk: Documentation changes may introduce incorrect or misleading public help content.

Mitigation: Review proposed deltas and verify uncertain product behavior before applying updates to customer-facing articles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georgelewi5/skills/intercom-docs)
- [Intercom Help Center API endpoint](https://api.intercom.io/help_center/collections)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with optional inline shell commands for Intercom API inspection]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested article titles, article bodies, review summaries, proposed deltas, assumptions, and items to verify.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
