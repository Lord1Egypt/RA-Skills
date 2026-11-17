## Description:

Linear项目管理 is a Chinese-language Linear project-management API wrapper that helps agents turn user instructions into project, task, progress-tracking, and collaboration operations with structured responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automation teams use this skill to ask an agent for Linear project-management API operations such as task planning, project updates, progress tracking, and team-collaboration workflows. It is not intended for actual personnel performance evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ClawHub security scan describes the skill as a vague Linear/API automation wrapper that requests broad local command, file, and API authority.

Mitigation: Install only in an agent environment with restricted shell execution, limited file access, and scoped API credentials until exact supported operations and allowed commands are defined.

Risk: The skill can involve Linear or external API operations without clearly documented confirmation requirements.

Mitigation: Require user confirmation before create, update, delete, bulk, or paid-tier operations, and prefer least-privilege Linear tokens.

Risk: The artifact describes API key configuration and API automation, which can expose credentials if the runtime or logs are broad.

Mitigation: Use environment variables or secret storage, avoid broad local-system permissions, and redact credentials from prompts, responses, logs, and generated files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/linear-project-manager)
- [Publisher Profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON response examples and shell environment commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return structured success, data, and error fields for API-style operations.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
