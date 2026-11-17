## Description:

Open Instagram in the user's Brave browser and take the user to the Instagram homepage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruchir17-cmd](https://clawhub.ai/user/ruchir17-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Users ask an agent to open, visit, or go to Instagram in Brave while reusing an existing browser session and avoiding duplicate Instagram tabs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use an already signed-in Instagram browser session.

Mitigation: It is limited to opening and verifying Instagram, and it instructs the agent not to enter credentials or make account changes.

Risk: Instagram may require authentication before the homepage is available.

Mitigation: The skill stops at the login prompt and tells the user authentication is required.

## Reference(s):

- [Instagram homepage](https://www.instagram.com/)
- [ClawHub skill page](https://clawhub.ai/ruchir17-cmd/skills/open-instagram)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Natural-language status with browser navigation actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Brave, prefers an existing Instagram tab, stops at login prompts, and does not handle credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
