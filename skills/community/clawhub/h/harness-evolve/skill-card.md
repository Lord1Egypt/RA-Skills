## Description:

Harness Evolve helps AI agent systems consume research logs, self-check configuration and recent logs, propose or safely apply graded improvements, and write a daily evolution summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dottythehomeless](https://clawhub.ai/user/dottythehomeless)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn research findings and system self-checks into safe maintenance actions, review proposals, and daily evolution summaries for AI agent projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read recent logs or memory that contain sensitive operational context.

Mitigation: Run it only in projects where log and memory access is approved, and redact secrets or sensitive records before use.

Risk: The skill can edit project files and create commits automatically.

Mitigation: Require explicit confirmation for every write, delete, and commit, and keep runtime configuration changes as proposal-only.

Risk: The optional notify_command path can execute shell commands from project configuration.

Mitigation: Remove notify_command or restrict it to a fixed, reviewed allowlist before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dottythehomeless/skills/harness-evolve)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, review proposals, file edits, commits, and optional shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an overwriteable daily evolution summary and may append proposal or status entries to project files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
