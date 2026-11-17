## Description:

Integrates Modellix's unified API and CLI for AI image, video, and audio workflows, including schema lookup, task submission, waiting, and result download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modellix](https://clawhub.ai/user/modellix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Modellix media generation and transformation workflows, inspect model request schemas, manage authentication, and retrieve asynchronous task results. It supports CLI-first operation with REST fallback for image, video, speech, transcription, and voice-cloning tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically install or update the global modellix-cli package from npm before paid work.

Mitigation: Review before installing, set MODELLIX_CLI_AUTO_UPDATE=0 when environments require a pinned CLI, or install a trusted modellix-cli version manually.

Risk: The skill uses MODELLIX_API_KEY for Modellix CLI and REST calls.

Mitigation: Prefer session-only credentials, avoid printing keys, and run in an environment without unrelated sensitive credentials exposed to child processes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/modellix/skills/modellix)
- [Modellix AI onboarding](https://docs.modellix.ai/get-started.md)
- [Modellix REST API](https://docs.modellix.ai/ways-to-use/api.md)
- [Modellix full models index](https://docs.modellix.ai/llms.txt)
- [Modellix Docs MCP](https://docs.modellix.ai/mcp)
- [modellix-cli package](https://www.npmjs.com/package/modellix-cli)
- [Capability matrix](references/capability-matrix.md)
- [CLI playbook](references/cli-playbook.md)
- [REST playbook](references/rest-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON and shell command examples; task-result JSON and downloaded media files when workflows execute]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Modellix task IDs and resource URLs; downloaded resources should be persisted promptly because resource URLs may expire.]

## Skill Version(s):

1.0.24 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
