## Description:

Open npm in Brave. Use when the user asks to use npm for this purpose.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent open npm.com in Brave while reusing an existing session or tab when available. It stops before credential entry, account creation, payments, or account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use an existing Brave session and display an already logged-in npm page.

Mitigation: Review the visible browser state before continuing; the skill must not enter credentials, create accounts, make payments, or modify account settings.

Risk: Navigation may stop at a login page when authentication is required.

Mitigation: The agent should stop at the login page and tell the user instead of attempting to authenticate.

## Reference(s):

- [npm website](https://www.npmjs.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-npm)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Text]

**Output Format:** [Markdown instructions with YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser navigation target is npm.com in Brave; the skill verifies the destination and stops at login when authentication is needed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
