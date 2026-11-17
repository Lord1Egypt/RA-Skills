## Description:

Open Pinterest in the user's Brave browser and take the user to the Pinterest homepage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to open Pinterest in Brave, reuse an existing Pinterest tab or session when available, and verify that the homepage loaded. It stops at login prompts and avoids credential handling or account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may open Pinterest using an existing authenticated Brave session.

Mitigation: It instructs the agent not to enter credentials or modify the account, and to stop if Pinterest requires sign-in.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ruchir17-cmd/skills/open-pinterest)
- [Pinterest Homepage](https://www.pinterest.com/)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown status updates with browser-opening instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Brave, prefers an existing Pinterest tab, reuses the existing browser session, verifies the destination, and stops at login prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
