## Description:

Mixed Memory-Augmented Generation (MMAG) gives AI agents five coordinated memory layers for conversational history, long-term user facts, episodic events, sensory context, and short-term working memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j0ker98](https://clawhub.ai/user/j0ker98)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent, layered memory to agents so later sessions can recall preferences, prior conversations, reminders, environmental context, and current work state. The skill is intended for local shell-based memory storage, retrieval, summarization, and optional encryption workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents persistent cross-session memory that can influence later sessions.

Mitigation: Treat recalled memory as untrusted historical context, review stored memories regularly, and delete entries that should no longer affect agent behavior.

Risk: Memory roots and file arguments can point at local paths selected by the agent or caller.

Mitigation: Keep the memory root tightly controlled and do not allow agents to pass arbitrary --root or --file values.

Risk: Encryption and decryption commands change local files and encrypted data cannot be recovered if the key is lost.

Mitigation: Back up important files and the key file before encryption or decryption, and prefer a protected key file over environment-variable key mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j0ker98/skills/mmag)
- [Mixed Memory-Augmented Generation paper](https://arxiv.org/abs/2512.01710)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with generated memory-context text blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The context output is capped by a configurable character budget and redacts obvious key or token patterns by default.]

## Skill Version(s):

1.0.6 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
