## Description:

Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pipsqueakup](https://clawhub.ai/user/pipsqueakup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find installable agent skills for a requested capability and receive search terms, candidate links, and installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide users toward broad persistent installation of third-party skills with limited review.

Mitigation: Review the exact repository, version, and destination before installation; avoid the suggested global non-interactive install form unless the source and package are trusted.

Risk: The included Python demo writes sample_skill/SKILL.md and reads DASHSCOPE_API_KEY if run or imported.

Mitigation: Do not run or import the demo unless that behavior is intended; use an isolated workspace and scoped environment variables when evaluating it.

Risk: Search results and suggested skills may point to untrusted third-party code.

Mitigation: Prefer pinned and vetted Skills CLI versions, inspect candidate skill contents, and require explicit user confirmation before adding a skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pipsqueakup/skills/new-slug)
- [Find Skills reference](references/DOC.md)
- [Skills directory](https://skills.sh/)
- [Anthropic Skills blog](https://claude.com/blog/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Skills CLI searches and installs; installation commands should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
