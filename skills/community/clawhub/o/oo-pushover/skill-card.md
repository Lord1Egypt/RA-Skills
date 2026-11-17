## Description:

Manage Pushover notifications, delivery groups, account information, and Open Client data through a connected Pushover account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Pushover users and developers can use this skill to inspect account limits and groups, send notifications, and manage delivery groups or Open Client data through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential retrieval or storage can expose Pushover application or team API tokens.

Mitigation: Require explicit approval before token retrieval or storage, and keep token values out of ordinary responses and logs.

Risk: The external CLI installer and connector have not been verified, so their credential protections and installation effects are uncertain.

Mitigation: Review the CLI installation separately before running it.

## Reference(s):

- [Pushover](https://pushover.net)
- [Pushover API documentation](https://pushover.net/api)
- [oo CLI on GitHub](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON action payloads and connector response data, summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include notification results, account data, or group and client information.]

## Skill Version(s):

1.0.6 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
