## Description:

Maintains AI-readable project memory for software repositories, including project context, progress, decisions, risks, and cross-agent instruction files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitzo](https://clawhub.ai/user/bitzo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to onboard into repositories, initialize shared project memory, and keep implementation history, verification notes, decisions, and risks consistent across sessions and AI tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be invoked implicitly by short setup requests such as init and may create persistent repository documentation or instruction files.

Mitigation: Review this skill before installing where short init commands are used for other workflows, and inspect generated files before committing them.

Risk: Generated project memory can become misleading if repository facts are inferred from stale prose or unverified assumptions.

Mitigation: Ground updates in source, tests, configuration, and command output; mark unknown or unverified behavior explicitly.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/Bitzo/project-memory-skill/tree/main/skills/project-memory-workflow)
- [Project Memory Workflow on ClawHub](https://clawhub.ai/bitzo/skills/project-memory-workflow)
- [Agent instruction file compatibility](references/agent-file-compatibility.md)
- [Project memory file design](references/memory-file-design.md)
- [Progress entry template](references/progress-entry-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown documents, repository instruction files, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project memory files and agent instruction files only when user intent or repository state supports it.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
