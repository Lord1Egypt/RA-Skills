## Description:

Fast semantic memory system with JSON indexing, auto-consolidation, and <20ms search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent operators use this skill to persist learnings, decisions, insights, events, and interactions across sessions, then search or summarize those local memories when prior context is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist private, regulated, client, or credential-bearing information in local memory files.

Mitigation: Do not store secrets or raw sensitive conversations, and add redaction plus retention or deletion controls before using it with sensitive data.

Risk: Recalled memories may be stale, incomplete, or untrusted notes.

Mitigation: Treat recalled memory as context to verify against authoritative sources before acting on it.

Risk: Local markdown and JSON memory files may be readable by other local processes or users if file permissions are broad.

Mitigation: Store the memory directory with strict file permissions and review access controls before deployment.

Risk: The shell script constructs JSON records from command-line inputs.

Mitigation: Review JSON construction paths and test escaping behavior before relying on it for arbitrary user-provided memory content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sieyer/skills/memory-system-v2-1-0-0)
- [Memory System V2 README](artifact/README.md)
- [Memory System V2 Design](artifact/docs/memory-system-v2-design.md)
- [Memory System V2 Test Results](artifact/docs/memory-system-v2-test-results.md)
- [Project Homepage](https://github.com/austenallred/memory-system-v2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON-backed memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and jq; stores memories as local markdown logs and JSON index files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
