## Description:

Decompose a session into typed handoff units and recall them later

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture session findings, decisions, temporary state, and open questions as typed handoff units, then retrieve relevant units when work resumes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Four referenced materials could not be matched to bundled artifacts, so their contents are not covered by the available scan results.

Mitigation: Review those referenced materials before installing if they are available.

Risk: The handoff staging file is process-global, so concurrent sessions in one checkout can drain one another's staged units.

Mitigation: Avoid concurrent capture sessions in the same checkout, or use separate checkouts.

## Reference(s):

- [Homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-memory-palace-session-handoff)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured JSON handoff units with concise Markdown recall guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Units can include thread type, date, state, reasoning, unresolved questions, session reference, and optional file dependencies.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
