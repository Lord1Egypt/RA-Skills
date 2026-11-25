## Description:

Connect OpenClaw to LeadJourney to analyze marketing attribution, lead journeys, reports, live ad data, and website tracking, and to request ad account changes for human confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leadjourney](https://clawhub.ai/user/leadjourney)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask which campaigns and channels drive leads and revenue, review an individual lead's journey, and run attribution reports. They can also inspect live ad platform data, set up tracking, or prepare ad account changes that require confirmation in LeadJourney.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting grants the LeadJourney service access to workspace data using the signed-in user's permissions.

Mitigation: Connect only if the user trusts LeadJourney; have the user sign in and approve OAuth, and explain that access can be revoked in LeadJourney.

Risk: Website tracking records visits, clicks, and form submissions and sends them to LeadJourney.

Mitigation: Explain the tracking before installation and follow the site's cookie consent setup.

Risk: Requested ad account changes could affect campaign settings if approved.

Mitigation: Describe the proposed change and state that it takes effect only after a person confirms it inside LeadJourney.

## Reference(s):

- [LeadJourney](https://leadjourney.io)
- [LeadJourney MCP service](https://api.leadjourney.io/mcp)
- [LeadJourney ClawHub release](https://clawhub.ai/leadjourney/skills/leadjourney)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown text with inline shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include attribution summaries, report results, lead journey summaries, tracking setup guidance, or ad change requests awaiting human confirmation.]

## Skill Version(s):

1.0.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
