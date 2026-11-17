## Description:

Query Grok AI (grok.com) for real-time information via browser automation. Requires: OpenClaw browser enabled, user pre-logged-in to grok.com, and a Grok account (free tier works).

This skill is ready for commercial/non-commercial use.

## Publisher:

[inphinitiz](https://clawhub.ai/user/inphinitiz)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to query Grok through an authenticated OpenClaw browser session for current information, news, fact checks, and multi-turn external research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and context are submitted to Grok through the user's logged-in browser session.

Mitigation: Avoid sending private, regulated, or account-sensitive data unless that use matches the user's Grok privacy expectations.

Risk: The skill depends on browser automation and cannot complete login, CAPTCHA, or human-verification flows automatically.

Mitigation: Confirm the user is logged in to grok.com and ask them to complete any manual verification before continuing.

## Reference(s):

- [Grok](https://grok.com)
- [Grok Query on ClawHub](https://clawhub.ai/inphinitiz/skills/grok-query)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text, markdown]

**Output Format:** [Markdown with inline shell commands and browser-operation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenClaw browser session already logged in to grok.com; responses may include Grok-generated text or image URLs captured from the browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
