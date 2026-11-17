## Description:

Provides a real-time dashboard for visualizing AI agent project progress, decision trees, and test results, with commands to install, start, stop, configure, export, and import dashboard state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakilmostak](https://clawhub.ai/user/sakilmostak)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to set up and manage a dashboard for monitoring AI agent project state, including implementation progress, decision paths, and test results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to globally install and run an unpinned third-party npm package whose implementation is not included for review.

Mitigation: Install only from a trusted npm publisher, prefer a pinned reviewed package version, inspect package source and lifecycle scripts, and run it in an isolated project or container when it may access sensitive project or agent state.

Risk: Dashboard configuration, database, and logs are stored under the user's home directory and may contain project or agent state.

Mitigation: Avoid placing secrets in dashboard state, protect the local state directory, and review exported files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sakilmostak/skills/pm-dashboard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers dashboard lifecycle commands and local state locations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
