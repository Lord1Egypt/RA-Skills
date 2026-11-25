## Description:

Converts Meta short-lived access tokens into long-lived tokens, checks validity and expiry, and guides renewal without accessing ad data; configuration changes require explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to exchange and check Meta user access tokens and track when they need renewal. It also guides safe, explicitly confirmed configuration updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access tokens and app secrets are sensitive credentials used in the renewal workflow and may appear in chat history or configuration.

Mitigation: Follow the skill's guidance not to echo credentials or place them in logs, and review the token-handling steps before use.

Risk: Updating gateway configuration can affect which token the integration uses.

Mitigation: Require explicit user confirmation before saving a token, preserve the existing configuration, and do not restart the gateway automatically.

## Reference(s):

- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer)
- [Meta token exchange endpoint](https://graph.facebook.com/v21.0/oauth/access_token)
- [ClawHub skill release](https://clawhub.ai/thinhbuiii/skills/meta-long-lived-token)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides step-by-step token renewal and expiry-check guidance.]

## Skill Version(s):

1.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
