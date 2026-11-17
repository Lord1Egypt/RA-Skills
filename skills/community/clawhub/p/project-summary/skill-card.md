## Description:

Generate an instant codebase overview of language, framework, architecture, entry points, and key files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fratua](https://clawhub.ai/user/fratua)

### License/Terms of Use:


## Use Case:

Developers, engineers, and agents use this skill to quickly understand an unfamiliar codebase by summarizing project structure, frameworks, entry points, dependencies, tests, CI/CD, and notable files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local project files to summarize structure, dependencies, tests, and CI.

Mitigation: Run it only in repositories where agent access to project files is acceptable.

Risk: Broad prompts such as 'what is this project' may activate the skill.

Mitigation: Review agent tool and skill activation behavior before installing it in sensitive workspaces.

Risk: Generated summaries can omit context or misclassify unfamiliar architectures.

Mitigation: Review the summary against source files before using it for onboarding, audits, or follow-on automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fratua/skills/project-summary)
- [Publisher Profile](https://clawhub.ai/user/fratua)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The summary is concise and organized for developer onboarding or agent context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
