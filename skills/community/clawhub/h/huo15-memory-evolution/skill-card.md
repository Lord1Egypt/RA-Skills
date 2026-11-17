## Description:

Huo15 Memory Evolution helps OpenClaw agents capture, organize, recall, summarize, and share persistent memories across personal and team workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of OpenClaw agents use this skill to maintain long-lived user, feedback, project, and reference memory, recover session state, track asynchronous work, and share selected team context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private agent memory and may send log or memory content to an external LLM service.

Mitigation: Review external data sharing before installation, avoid sensitive workspaces until documented, and require explicit user approval for any memory export.

Risk: The security review reports bundled credentials and disabled TLS verification in external API behavior.

Mitigation: Remove bundled API keys, load secrets from a managed environment, and restore normal TLS certificate verification before use.

Risk: Batch installation and team-memory scripts can modify multiple agent workspaces.

Mitigation: Require explicit target selection, validate persistent memory paths, and take backups before cross-agent changes.

Risk: Unpinned dependencies or helper tools can change behavior across installations.

Mitigation: Pin dependencies and document required tool versions before approving production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/huo15-memory-evolution)
- [Memory type configuration](artifact/config/memory-types.json)
- [Memory file template](artifact/templates/memory-file.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown memory files, shell command output, JSON configuration, and plain-text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent memory, session-state, task-progress, and team-memory files in OpenClaw workspaces.]

## Skill Version(s):

3.4.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
