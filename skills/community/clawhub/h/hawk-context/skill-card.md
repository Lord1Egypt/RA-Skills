## Description:

Context Compressor compresses the current conversation history into a shorter prompt while preserving system instructions, recent messages, and key task context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to reduce long conversation context into a compact continuation prompt with preserved instructions, recent turns, and compression metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change agent behavior automatically through context-threshold triggers.

Mitigation: Keep compression explicit and opt-in unless the user has reviewed and accepted the auto-trigger behavior.

Risk: Compression history can persist conversation-derived records that may contain secrets or sensitive data.

Mitigation: Avoid enabling memory logging for sensitive chats and review generated records before retaining or sharing them.

Risk: The installer can alter the user's shell environment by adding ~/bin to PATH and creating command symlinks.

Mitigation: Run the installer only after reviewing the shell changes, or invoke the script directly without modifying shell startup files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/relunctance/skills/hawk-context)
- [Compression Logic](references/compression-logic.md)
- [Auto-Trigger](references/auto-trigger.md)
- [Structured Output](references/structured-output.md)
- [CLI Reference](references/cli.md)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include compression statistics, retained-message counts, summarized-message counts, and suggested compression levels.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
