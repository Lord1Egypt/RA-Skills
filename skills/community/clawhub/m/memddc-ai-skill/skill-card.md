## Description:

MemDDC helps agents scan software projects, generate and synchronize project documentation, build DDD-oriented context, and use structured memory snapshots during code iteration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qihao123](https://clawhub.ai/user/qihao123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create and maintain project knowledge bases, DDD models, code-change impact context, and synchronized documentation for long-lived software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may scan broad local project content, VCS history, configuration files, user documents, and possible database connection material into persistent shared artifacts.

Mitigation: Use it only on repositories where that analysis and storage is acceptable; exclude secrets and environment files, avoid live database credentials, and review .memddc contents before committing or sharing.

Risk: Generated project memory and documentation may expose sensitive implementation or business context if shared with a team or committed to version control.

Mitigation: Prefer sanitized schema exports and curated documentation, and apply repository access controls before synchronizing generated artifacts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/qihao123/skills/memddc-ai-skill)
- [Project homepage listed in artifact](https://github.com/qihao123/memddc-ai-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .memddc documentation, memory snapshots, logs, diagrams, and configuration files.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact skill information)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
