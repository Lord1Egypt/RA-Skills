## Description:

This skill helps agents install, configure, and use memory-lancedb-pro, a long-term memory plugin for OpenClaw AI agents with Smart Extraction, hybrid retrieval, memory lifecycle management, multi-scope isolation, and self-improvement governance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darcy-wang](https://clawhub.ai/user/darcy-wang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure persistent memory for OpenClaw agents, choose provider plans, validate API keys, update memory plugin configuration, and run verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to expose provider API keys during setup.

Mitigation: Use environment variables or a secret manager, avoid pasting keys into chat, and do not store literal keys in openclaw.json.

Risk: The setup flow references remote installer and validator code that may be unpinned.

Mitigation: Review remote source before execution and prefer pinned commits or exact package versions.

Risk: The plugin can persist and recall conversation-derived memory and alter agent behavior through self-improvement files or agent guidance.

Mitigation: Review autoCapture, autoRecall, management tools, self-improvement files, and AGENTS.md or CLAUDE.md changes before enabling them.

## Reference(s):

- [Memory Lancedb Pro Skill ClawHub Page](https://clawhub.ai/darcy-wang/skills/memory-lancedb-pro-skill)
- [Full Technical Reference](artifact/references/full-reference.md)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose configuration changes, validation commands, memory tool calls, and setup steps for third-party services.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
