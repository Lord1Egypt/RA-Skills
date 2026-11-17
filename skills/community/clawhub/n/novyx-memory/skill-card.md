## Description:

Enterprise-grade persistent memory for AI agents with rollback, audit trails, a knowledge graph, governed actions, time-travel debugging, and 60+ Novyx Core commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[novyxlabs](https://clawhub.ai/user/novyxlabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent, searchable memory to OpenClaw agents, including automatic save and recall, rollback, audit, shared context spaces, and governance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation turns, assistant responses, search queries, traces, and memory operations may be sent to third-party Novyx storage.

Mitigation: Use only with data appropriate for third-party storage, redact sensitive content, and consider disabling autoSave and autoRecall by default.

Risk: The NOVYX_API_KEY and optional NOVYX_API_URL control access to external memory operations.

Mitigation: Store credentials in a secret manager or protected environment variables, rotate exposed keys, and avoid committing them to project files.

Risk: Rollback, delete, share, and approval commands can change or expose stored memory state.

Mitigation: Require explicit user confirmation for rollback, delete, share, and approval actions, and use preview commands before destructive changes when available.

## Reference(s):

- [Novyx Labs](https://novyxlabs.com)
- [Novyx Memory on ClawHub](https://clawhub.ai/novyxlabs/skills/novyx-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown text with command responses, recalled context, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOVYX_API_KEY for API-backed memory operations; autoSave and autoRecall default to enabled.]

## Skill Version(s):

3.0.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
