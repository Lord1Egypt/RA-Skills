## Description:

Agent-native memory for OpenClaw that structures memory from agent trace, execution history, decisions, tool calls, and conversations into durable long-term memory primitives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rpkruse](https://clawhub.ai/user/rpkruse)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and OpenClaw users use Memori to add opt-in, cloud-backed long-term memory to agents, including structured recall of prior decisions, workflow history, tool usage, and conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured use stores OpenClaw session content, tool-use history, and related memory data with Memori.

Mitigation: Enable the plugin only after reviewing Memori privacy and retention controls, and keep projectId and entityId scopes narrow.

Risk: MEMORI_API_KEY exposure could allow unauthorized access to a user's Memori configuration.

Mitigation: Keep the API key in environment or secret storage, avoid printing it in logs or chat, and prefer a reviewed, pinned plugin version.

Risk: Broad memory capture or recall may surface more historical context than needed.

Mitigation: Use narrow project scopes and date-bounded recall where possible, and monitor quota and stored memory volume.

## Reference(s):

- [Memori OpenClaw documentation](https://memorilabs.ai/docs/memori-cloud/openclaw/overview/)
- [Memori npm package](https://www.npmjs.com/package/@memorilabs/openclaw-memori)
- [Memori GitHub repository](https://github.com/MemoriLabs/Memori)
- [Memori API dashboard](https://app.memorilabs.ai/)
- [Memori API service](https://api.memorilabs.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMORI_API_KEY, ENTITY_ID, PROJECT_ID, and the memori CLI; uses the Memori API service after user configuration.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
