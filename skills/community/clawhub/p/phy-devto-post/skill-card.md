## Description:

Post articles to DEV.to using AppleScript Chrome control for technical blog posts, showdev articles, or open source project announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical publishers use this skill to prepare and publish DEV.to articles through a logged-in Chrome session on macOS. It is suited for technical blog posts, showdev articles, and open source project announcements where the agent returns the published article link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish a live DEV.to article through the user's logged-in Chrome session without a required review or confirmation step.

Mitigation: Add a draft-first workflow and require explicit confirmation of the title, tags, target account, and publication status before posting.

Risk: Long-article handling uses temporary files for article content.

Mitigation: Use safer temporary-file handling, remove temporary files after use, and avoid storing sensitive draft content in predictable paths.

## Reference(s):

- [Phy Devto Post on ClawHub](https://clawhub.ai/phy041/skills/phy-devto-post)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)
- [DEV.to](https://dev.to)

## Skill Output:

**Output Type(s):** [markdown, shell commands, code, guidance]

**Output Format:** [Markdown with inline bash, AppleScript, JavaScript, and JXA code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May publish a live DEV.to article through the user's logged-in Chrome session and should return the final article link.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
