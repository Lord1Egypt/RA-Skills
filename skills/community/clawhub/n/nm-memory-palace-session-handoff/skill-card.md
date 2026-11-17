## Description:

Decompose a session into typed handoff units and recall them later

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people working with AI agents use this skill to preserve decisions, findings, current state, and unresolved questions between sessions, then retrieve relevant notes when work resumes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial because some local references were not available to the scanner.

Mitigation: Review the resolved references and their contents before relying on behavior that depends on them.

Risk: The handoff staging file is process-global, so concurrent sessions in one checkout can drain each other’s staged units.

Mitigation: Avoid concurrent captures in the same checkout, or use separate checkouts for simultaneous sessions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-memory-palace-session-handoff)
- [Memory Palace homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [Unit Schema](artifact/modules/unit-schema.md)
- [Two-Phase Extraction](artifact/modules/two-phase-extraction.md)
- [Temporal Awareness](artifact/modules/temporal-awareness.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured Markdown guidance and JSON handoff-unit records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handoff units use typed fields and can identify file dependencies for later staleness checks.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
