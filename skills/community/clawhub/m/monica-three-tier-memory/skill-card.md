## Description:

Three Tier Memory helps agents manage short-term, summary-based medium-term, and vector-retrieved long-term memory for conversation history, context compression, personal knowledge bases, and persistent recall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forvendettaw](https://clawhub.ai/user/forvendettaw)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add local memory workflows to agents: sliding-window context for active conversations, summaries for compressed history, and ChromaDB-backed retrieval for longer-term recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist arbitrary conversation and preference data in plaintext local files.

Mitigation: Use it only with informed consent and add retention, deletion, encryption, and file-permission controls before storing sensitive data.

Risk: Secrets, credentials, regulated personal data, or confidential business information may be captured in memory content.

Mitigation: Avoid storing sensitive content unless appropriate consent, access control, retention, and deletion safeguards are implemented.

## Reference(s):

- [Memory Manager command reference](references/references.md)
- [ClawHub skill page](https://clawhub.ai/forvendettaw/skills/monica-three-tier-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash and Python examples; CLI text output and JSON memory files when scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local memory files under a workspace memory directory and uses ChromaDB for long-term retrieval when installed.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
