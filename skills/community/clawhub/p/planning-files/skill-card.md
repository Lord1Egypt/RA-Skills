## Description:

File-based planning for complex tasks that uses persistent markdown files as working memory to survive context resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep complex, multi-step work organized across context resets by maintaining task plans, findings, and progress logs in project markdown files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists task context in project-root markdown files, which can expose secrets, credentials, personal data, or sensitive research if those details are written into the files.

Mitigation: Review before installing, redact sensitive information before writing planning files, and avoid using it for sensitive work unless cleanup and retention expectations are clear.

Risk: The artifact documents mutable remote install commands, so the installed content may differ over time if the source is not pinned and reviewed.

Mitigation: Install from a pinned, reviewed source whenever possible and inspect the artifact before enabling it in an agent environment.

## Reference(s):

- [Manus Context Engineering Principles](references/manus-principles.md)
- [Context Engineering for AI Agents: Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates task_plan.md, findings.md, and progress.md in the project root when the workflow or helper script is used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
