## Description:

Fetches and displays OpenRouter model pricing and context limits, then helps configure OpenClaw model routing through automatic or fallback settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notestone](https://clawhub.ai/user/notestone)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to compare model costs, plan task-specific model routing, and generate cost-aware configuration patches. Optional execution mode can spawn multi-agent workflows, so it should be used carefully in sensitive workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional execution mode can spawn agents that write files in the active workspace.

Mitigation: Use planning mode for routine model-routing decisions, and run execution mode only in a workspace where generated files can be reviewed or discarded.

Risk: Task text, execution status, and error snippets may be retained in local swarm memory and insight files.

Mitigation: Avoid sensitive tasks with execution mode and periodically remove ~/.openclaw/workspace/swarm_memory.json and ~/.openclaw/workspace/swarm_insights.json.

Risk: The smart file finder can print matched local file contents.

Mitigation: Run file-search helpers only from intended directories and avoid using them in repositories that contain secrets or private data.

Risk: Configuration updates affect the local OpenClaw model fallback settings.

Mitigation: Review generated configuration patches before applying them and keep a backup of existing OpenClaw configuration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/notestone/skills/model-manager)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [Model Benchmarks Companion Skill](https://clawhub.ai/skills/model-benchmarks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables, JSON configuration patches, shell commands, and local report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write OpenClaw configuration changes and local swarm memory or insight JSON when execution or consolidation modes are used.]

## Skill Version(s):

1.5.0 (source: server release metadata and artifact title)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
