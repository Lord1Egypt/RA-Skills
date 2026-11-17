## Description:

Discovers, searches, and installs agent skills from multiple marketplaces using the SkillKit CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find relevant agent skills, browse skill marketplaces, present install options, and install selected skills from partner or community repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage broad discovery and installation of third-party skills that may affect future agent behavior.

Mitigation: Review target repositories and skill contents before installation, and require explicit user confirmation before installing or enabling skills.

Risk: The documented commands use latest package resolution for SkillKit, which can change behavior over time.

Mitigation: Prefer pinned and reviewed SkillKit versions in managed or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/miknasbh-stack/skills/miknas-find-skills)
- [SkillKit website](https://agentskills.com)
- [SkillKit GitHub repository](https://github.com/rohitg00/skillkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include marketplace search results, repository references, installation commands, and cautionary installation guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
