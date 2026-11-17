## Description:

Memory Layer helps agents design and operate a three-layer memory system with Index, Topic, and Transcript files, optional autoDream cleanup, and importance-based retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whyischen](https://clawhub.ai/user/whyischen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure persistent local memory, migrate existing memory files into layered storage, configure optional scheduled cleanup, and reduce context-window load during retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent plaintext transcripts can expose sensitive or private material if used for secrets, health records, financial identifiers, or similar data.

Mitigation: Store only summaries, rules, timestamps, and non-sensitive references in transcripts; keep sensitive material in an encrypted system and reference it by ID.

Risk: Scheduled memory cleanup can mutate local memory files unexpectedly if enabled before the operator understands its behavior.

Mitigation: Keep autoDream disabled or in dry-run until backups exist and the operator has reviewed which files it will read, update, archive, or summarize.

Risk: The rollback guide includes a deletion command that can remove memory directories if run without confirming backup integrity.

Mitigation: Verify backups first and move directories aside for recovery instead of running the deletion command as written.

## Reference(s):

- [Architecture Design](references/architecture.md)
- [Index Layer Specification](references/index-spec.md)
- [Topic Layer Specification](references/topic-spec.md)
- [Transcript Layer Specification](references/transcript-spec.md)
- [autoDream Cleanup](references/autodream.md)
- [Configuration Reference](references/config.md)
- [Migration Guide](guides/MIGRATION.md)
- [Usage Examples](guides/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no API keys or additional environment variables are required by the artifact.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
