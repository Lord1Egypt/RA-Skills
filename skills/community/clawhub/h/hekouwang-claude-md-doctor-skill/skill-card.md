## Description:

Audits project AGENTS.md and CLAUDE.md files for runtime-configuration quality and produces a scored review with prioritized fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huiyonghkw](https://clawhub.ai/user/huiyonghkw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess a project's AGENTS.md or CLAUDE.md for clarity, useful routing, maintainability, and security guidance, then receive a scorecard and prioritized recommendations. It can also propose file edits when the user approves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence, citing an unpinned Docker image, a CI workflow that runs a remotely downloaded script, and audits beyond the stated configuration-file purpose.

Mitigation: Before using Docker or CI flows, assess whether you trust the image source and remote script, and review whether the broader skill and environment audits fit your needs. Scanner coverage is partial, and the verdict does not establish malicious intent.

## Reference(s):

- [Project homepage](https://github.com/huiyonghkw/hekouwang-claude-md-doctor-skill)
- [Doctor suite guide](artifact/references/doctor-suite.md)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Configuration guidance]

**Output Format:** [Markdown scorecard and prioritized recommendations, with an optional JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to project configuration files after user approval.]

## Skill Version(s):

1.3.4 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
