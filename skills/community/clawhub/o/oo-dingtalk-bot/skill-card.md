## Description:

Use the OOMOL-connected oo CLI to inspect action schemas and send messages through a DingTalk custom bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other DingTalk users use this skill to inspect the available custom bot message actions and send text, Markdown, link, feed-card, or action-card messages through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions can run remote installer code whose changes have not been verified.

Mitigation: Review setup first; use a separately approved, version-pinned and verified CLI installation, and review its bundled-skill synchronization settings.

Risk: Message contents pass through OOMOL to DingTalk.

Mitigation: Avoid sending sensitive content unless that data flow is approved for the account and use case.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [DingTalk custom bot documentation](https://open.dingtalk.com/document/dingstart/custom-bot-creation-and-installation)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown instructions with bash commands and JSON payloads; connector results are returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
