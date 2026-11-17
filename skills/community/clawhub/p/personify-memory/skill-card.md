## Description:

Personify Memory helps an OpenClaw agent record user-directed memories, identify important moments, and organize conversation-derived memories into core, emotional, knowledge, daily, and archive stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsa03](https://clawhub.ai/user/lsa03)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to give an OpenClaw agent durable personal memory workflows, including explicit "remember" commands, optional memory recommendations, scheduled review, and archive management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically processes private conversation history.

Mitigation: Review memory extraction behavior before installation and require user review before promoting conversation excerpts into long-term memory.

Risk: Conversation excerpts may be sent to a configurable external LLM endpoint.

Mitigation: Use a dedicated low-privilege LLM API key and restrict the endpoint to a trusted provider.

Risk: The skill writes durable memory and archive files that may retain sensitive information.

Mitigation: Back up OpenClaw session files before enabling cron and review retention settings for the deployment.

Risk: Security evidence reports misleading destructive test modes.

Mitigation: Disable or fix destructive test modes before normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lsa03/skills/personify-memory)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Default configuration](artifact/config/default-config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with code, shell command, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local memory, index, daily review, and archive files when enabled by the host agent.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
