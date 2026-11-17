## Description:

OpenClaw Memory Enhancer gives OpenClaw long-term local memory by loading memory files, searching for relevant context, and supporting recall across conversations on edge devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryfcb](https://clawhub.ai/user/henryfcb)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to add local, cross-session memory, semantic search, and contextual recall to agents and long-running projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can feed persistent memory contents back into future prompts without clear trust boundaries.

Mitigation: Do not store credentials, private keys, confidential notes, or untrusted instructions in the memory directory unless filtering and clear user controls are added.

Risk: The security review says the skill relies on unreviewed remote code.

Mitigation: Review the upstream code before use, prefer a pinned commit or audited package, and install dependencies in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henryfcb/skills/openclaw-memory-enhancer)
- [Publisher profile](https://clawhub.ai/user/henryfcb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local memory operations and recalled context; no external service output is required by the skill itself.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
