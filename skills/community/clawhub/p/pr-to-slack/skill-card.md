## Description:

Creates or reuses Bitbucket Cloud pull requests, assigns configured reviewers, requests review through Slack, and announces the batch after a clean review of unchanged commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvolutionor](https://clawhub.ai/user/alvolutionor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to deliver requested Bitbucket pull requests, coordinate a Slack review, and announce the change only when the review is clean and the commits remain unchanged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted Slack thread text can make an ordinary message appear to be the trusted review bot's clean result.

Mitigation: Treat the included review checker as advisory until sender, channel, thread, and timestamp are verified from structured Slack connector metadata; manually confirm the bot's actual message before announcing.

Risk: Broad Bitbucket credentials may grant unnecessary pull-request access.

Mitigation: Limit Bitbucket credentials to the minimum PR permissions needed for the requested repositories.

Risk: Extending the workflow with the unused Jira helper could introduce additional credential exposure.

Mitigation: Review the Jira helper before enabling or extending its use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alvolutionor/skills/pr-to-slack)
- [Configuration and request format](references/setup.md)
- [Example review-bot protocol](references/review-protocol.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Configuration guidance]

**Output Format:** [Text with pull request links, review status, and announcement links when sent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Announcement is conditional on a clean review and unchanged source and destination commits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
