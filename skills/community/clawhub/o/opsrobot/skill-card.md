## Description:

Helps developers install the opsrobot/openclaw observability platform and configure Apache Doris-backed log, metric, and trace collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[never112](https://clawhub.ai/user/never112)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to install opsrobot with Docker Compose and configure OpenClaw log and telemetry collection into Apache Doris. It provides setup guidance, shell commands, and configuration snippets for the observability workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run remote Docker Compose workloads without pinning a trusted release or commit.

Mitigation: Review the upstream Docker Compose file before installation and pin a trusted release, tag, or commit before running services.

Risk: The telemetry configuration can capture prompts, messages, system content, logs, and full telemetry streams.

Mitigation: Enable prompt, message, system-content, or full-log telemetry only with explicit approval, redaction, retention limits, access controls, and a trusted authenticated HTTPS collector.

Risk: The skill includes a repository-star request unrelated to the operational setup task.

Mitigation: Treat the star request as optional promotional text and ignore it unless the user independently chooses to star the repository.

## Reference(s):

- [opsrobot repository referenced by the skill](https://github.com/opsrobot-ai/opsrobot)
- [ClawHub skill page](https://clawhub.ai/never112/skills/opsrobot)
- [Publisher profile](https://clawhub.ai/user/never112)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-provided deployment paths, log directories, Doris targets, and telemetry collector endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
