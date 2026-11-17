## Description:

Export a research session into knowledge-intake compatible markdown. Use after a research session to hand findings to memory-palace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers use this skill after gathering findings to export them as a Markdown file that can be reviewed and handed to memory-palace knowledge intake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An export can be empty or contain findings that have not been evaluated for intake.

Mitigation: Check the finding count and review the exported file before sending it to knowledge intake.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-tome-export)
- [Tome project page listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/tome)

## Skill Output:

**Output Type(s):** [Markdown, Files]

**Output Format:** [Markdown file with YAML frontmatter and findings grouped by channel]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes session metadata and rendered finding details such as source, URL, relevance, summary, and channel-specific metadata.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
