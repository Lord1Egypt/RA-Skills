## Description:

Beamer (getbeamer.com). Use this skill for ANY Beamer request — reading, creating, and updating data. Whenever a task involves Beamer, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to read Beamer posts and feeds, count unread posts, and create posts through a connected Beamer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI dependency may change other agents’ installed skills without clear notice.

Mitigation: Review and approve a specific CLI release and installer; set OO_SKILLS_SYNC_DISABLED=1 to disable startup skill synchronization.

Risk: Creating a post changes content in the connected Beamer account.

Mitigation: Keep the required confirmation before running create_post.

## Reference(s):

- [Beamer homepage](https://www.getbeamer.com)
- [Beamer API documentation](https://help.userflow.com/beamer/docs/how-to-install-beamer-using-our-api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Beamer on ClawHub](https://clawhub.ai/oomol/skills/oo-beamer)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands]

**Output Format:** [Markdown with shell commands and JSON payloads or responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creating a post changes Beamer data and requires confirmation before execution.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
