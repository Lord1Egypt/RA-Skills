## Description:

Manage LinkedIn presence via the LinkedIn API, including posts, comments, media, profile data, and ad targeting searches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

LinkedIn users and their agents can read profiles and public content, draft and publish posts or comments, manage media, and look up ad targeting options through ClawLink. Publishing and deletion require the user's confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawLink brokers access to the connected LinkedIn account.

Mitigation: Confirm that you trust ClawLink to handle LinkedIn OAuth access before connecting the account.

Risk: Publishing, commenting, or deleting can change the user's public LinkedIn presence.

Mitigation: Preview each write and obtain explicit confirmation of the exact content, target, and effect before execution.

Risk: Reading other people's public LinkedIn content consumes ClawLink credit.

Mitigation: Disclose the credit cost and obtain the user's agreement before making paid public-data requests.

## Reference(s):

- [ClawHub LinkedIn skill](https://clawhub.ai/hith3sh/skills/linkedin-social)
- [ClawLink OpenClaw documentation](https://docs.claw-link.dev/openclaw)
- [LinkedIn API documentation](https://learn.microsoft.com/en-us/linkedin/)
- [LinkedIn Marketing API documentation](https://learn.microsoft.com/en-us/linkedin/marketing/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance and tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require a matching preview and explicit user confirmation.]

## Skill Version(s):

1.0.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
