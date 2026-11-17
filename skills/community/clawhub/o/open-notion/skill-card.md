## Description:

Open Notion in the user's Brave browser and take the user to their Notion workspace/dashboard when possible.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to open Notion in Brave, reuse an existing Notion tab or authenticated session when available, and reach their Notion workspace without handling credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An authenticated Notion workspace may become visible when Brave opens or focuses an existing session.

Mitigation: Review the visible browser state before sharing your screen or allowing others to view the session.

Risk: The skill may stop at a Notion login page when no authenticated session is available.

Mitigation: Authenticate manually in the browser; the skill should not request, enter, or store credentials.

## Reference(s):

- [Notion](https://www.notion.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-notion)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with browser-operation guidance and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Opens or focuses Brave, reuses an existing Notion tab when possible, stops at login, and verifies the visible destination before reporting success.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
