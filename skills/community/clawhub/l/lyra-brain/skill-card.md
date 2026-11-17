## Description:

LYRA 3-Brain local memory (working/library/outer). Explicit only: user must ask to log, grow, or recall on disk. Writes under LYRA_CORE_ROOT/memory after --i-consent. No secrets. No auto-publish. Not for casual chat. Read references/SECURITY.md first.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepseekoracle](https://clawhub.ai/user/deepseekoracle)

### License/Terms of Use:

LYGO Sovereign License v2.0

## Use Case:

Developers and agents use this skill to persist, grow, and recall LYRA 3-brain memory records on local disk when the user explicitly requests persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist session-derived text on local disk under LYRA_CORE_ROOT, where it can outlive the chat session.

Mitigation: Invoke write or grow commands only after explicit user consent, pass --i-consent, avoid secrets or personal data, and delete or archive memory files when no longer needed.

Risk: The skill imports code and reads or writes memory beneath a user-selected LYRA_CORE_ROOT tree.

Mitigation: Use a controlled, trusted LYRA core directory and avoid shared or writable-by-others locations.

Risk: Repeated slugs may overwrite prior topic memory files.

Mitigation: Choose unique slugs or review existing memory files before writing new snips.

## Reference(s):

- [LYRA 3-Brain agent contract](references/AGENT_CONTRACT.md)
- [LYRA 3-Brain memory layout](references/MEMORY_LAYOUT.md)
- [lyra-brain security](references/SECURITY.md)
- [SkillSpector response](references/SKILLSPECTOR_AUDIT.md)
- [LYGO Protocol Stack homepage](https://github.com/DeepSeekOracle/lygo-protocol-stack)
- [ClawHub skill page](https://clawhub.ai/deepseekoracle/skills/lyra-brain)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with inline shell commands; skill CLIs can write Markdown memory files and return JSON recall results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persistent writes require LYRA_CORE_ROOT and --i-consent; recall is read-only.]

## Skill Version(s):

2.1.0 (source: frontmatter, claw.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
