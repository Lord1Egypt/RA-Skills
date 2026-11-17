## Description:

Run and integrate LM Studio with local model lifecycle control, OpenAI-compatible APIs, embeddings, and MCP-aware workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run local models with LM Studio, verify server readiness, load and swap models, connect OpenAI-compatible clients, test embeddings, and debug MCP-aware local workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep persistent local notes in ~/lm-studio/ about activation preferences, runtime baselines, models, and incidents.

Mitigation: Allow creation or updates to ~/lm-studio/ only after agreeing what will be stored, and do not save credentials or sensitive prompt contents in those files.

Risk: MCP servers or remote endpoints can change the local-only privacy boundary.

Mitigation: Keep MCP and remote endpoint use explicit-only, install only trusted MCP servers, and state when data may leave the machine.

## Reference(s):

- [ClawHub LM Studio Skill](https://clawhub.ai/ivangdavila/skills/lm-studio)
- [LM Studio Skill Homepage](https://clawic.com/skills/lm-studio)
- [Server Workflows](artifact/server-workflows.md)
- [Model Lifecycle](artifact/model-lifecycle.md)
- [API Recipes](artifact/api-recipes.md)
- [MCP Playbooks](artifact/mcp-playbooks.md)
- [Troubleshooting](artifact/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration examples, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-first guidance for LM Studio runtime checks, model operations, OpenAI-compatible API calls, embeddings, MCP setup, and troubleshooting]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
