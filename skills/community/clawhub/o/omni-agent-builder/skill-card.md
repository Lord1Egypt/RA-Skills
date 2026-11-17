## Description:

Builds secure OpenClaw agent and multi-agent workspaces, generating required workspace files plus guidance for orchestration, memory, evaluation, and CLI-driven setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ollieb89](https://clawhub.ai/user/ollieb89)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to design or update OpenClaw workspaces for single agents or Planner/Executor/Critic teams. It helps produce workspace files, safety guardrails, memory practices, and acceptance tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold script can overwrite existing OpenClaw workspace files when run against a non-empty target directory.

Mitigation: Run the scaffold in a new empty directory or back up AGENTS.md, SOUL.md, USER.md, and related files before execution.

Risk: Generated memory rules could expose private memory in inappropriate contexts if adopted without review.

Mitigation: Review generated memory rules before use, especially for group contexts, and keep curated memory limited to private main sessions.

## Reference(s):

- [OpenClaw Workspace](references/openclaw-workspace.md)
- [Templates](references/templates.md)
- [Architecture](references/architecture.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with fenced code blocks and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate complete OpenClaw workspace file contents and acceptance test prompts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
