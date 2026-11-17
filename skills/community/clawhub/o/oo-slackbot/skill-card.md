## Description:

Use the oo CLI to read and manage Slack messages, conversations, reactions, users, and files through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Slack workspace users use this skill to inspect channels, messages, users, and files, and to create or manage messages and reactions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback runs an unverified remote installer without a separate approval step.

Mitigation: Prefer installing a verified CLI yourself, or require explicit approval before downloaded setup code runs.

Risk: Actions run with access mediated through the connected Slack account, including posting and deletion actions.

Mitigation: Limit the connected account's permissions and review posts and deletions.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Slack Web API documentation](https://docs.slack.dev/apis/web-api/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Guidance]

**Output Format:** [JSON action payloads and connector responses; Slack message text or Block Kit content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checks action schemas before payload construction; write actions require user confirmation and destructive actions require explicit approval.]

## Skill Version(s):

1.0.8 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
