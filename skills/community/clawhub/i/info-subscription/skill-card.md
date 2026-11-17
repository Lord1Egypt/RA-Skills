## Description:

Info Subscription subscribes a user to company announcement data sources and sends scheduled email notifications for newly detected updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiaoshaohua](https://clawhub.ai/user/qiaoshaohua)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to bind an email address, subscribe to supported listed-company announcement feeds, check subscription status, manually trigger a push test, or unsubscribe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because the skill asks agents to follow unnecessary control instructions and avoid source inspection during error handling.

Mitigation: Reviewers should remove the thought-process and no-source-inspection instructions before installation or publication.

Risk: The skill transmits the user's email address to adeeptools.com and stores it locally.

Mitigation: Install only with clear user consent, disclose email storage and transmission, and restrict local configuration file permissions.

Risk: Trigger and unsubscribe commands can act on an arbitrary supplied email address according to the artifact behavior and security guidance.

Mitigation: Remove arbitrary-address trigger and unsubscribe support or require authentication before those actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiaoshaohua/skills/info-subscription)
- [adeeptools homepage](https://adeeptools.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill stores a locally bound email address and sends subscription, trigger, unsubscribe, and status requests to adeeptools.com.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
