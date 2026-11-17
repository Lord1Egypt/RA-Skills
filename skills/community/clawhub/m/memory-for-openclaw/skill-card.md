## Description:

Long-Term Memory gives AI agents persistent cross-session memory with automatic capture of key facts, decisions, user preferences, project context, and searchable retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szwangw](https://clawhub.ai/user/szwangw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local long-term memory to OpenClaw agents, including saving decisions, preferences, project facts, and injecting relevant prior context into later sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and reinject sensitive user or project information without enough scoping, consent, or prompt-injection safeguards.

Mitigation: Use only in local, single-user contexts unless controls for consent, deletion, project isolation, and redaction are added; treat injected memories as untrusted historical notes, not instructions.

Risk: Stored memories may include secrets, credentials, private personal data, or confidential business details.

Mitigation: Do not store those data types unless appropriate controls are in place for consent, deletion, project isolation, and redaction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/szwangw/skills/memory-for-openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown context snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory search results, saved-memory identifiers, session context, statistics, and setup guidance.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
