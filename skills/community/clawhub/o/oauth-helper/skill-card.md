## Description:

Automate OAuth login flows with user confirmation via Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helloliuyongsheng-bot](https://clawhub.ai/user/helloliuyongsheng-bot)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to help an agent navigate OAuth login and authorization flows while requesting Telegram confirmation before provider selection or consent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses live logged-in browser sessions for OAuth flows.

Mitigation: Use a browser profile dedicated to OAuth testing and only run the skill on websites you trust.

Risk: Authentication screenshots may be sent through Telegram.

Mitigation: Use only a Telegram destination you control and send cropped or redacted screenshots instead of full authentication pages.

Risk: The agent may reach an OAuth consent page for the wrong site, provider, account, or permission set.

Mitigation: Confirm the exact site, provider, account, and requested permissions before allowing the agent to click through consent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/helloliuyongsheng-bot/skills/oauth-helper)
- [Publisher profile](https://clawhub.ai/user/helloliuyongsheng-bot)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with browser command examples and step-by-step workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation via Telegram before OAuth provider selection or authorization.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
