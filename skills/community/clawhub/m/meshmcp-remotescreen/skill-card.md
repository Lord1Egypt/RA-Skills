## Description:

Plan consent-based screen-support review steps for owned Android devices using only user-provided context, privacy boundaries, safe next steps, and stop conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support reviewers use this skill to prepare a supervised Android screen-support checklist from user-provided screenshots or descriptions. It focuses the session on owner consent, privacy boundaries, safe next steps, and stop conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots or descriptions may expose private notifications, payment details, contact data, credentials, or unlock codes.

Mitigation: Ask the user to hide sensitive information and do not request credentials, device unlock codes, private notifications, payment details, or private contact data.

Risk: A support session could proceed without clear device ownership or consent.

Mitigation: Confirm the device owner and consent boundary before planning support steps, and stop when ownership or consent is unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/meshmcp-remotescreen)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown support summary, privacy checklist, safe next steps, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces a written checklist only and does not operate or observe the device.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
