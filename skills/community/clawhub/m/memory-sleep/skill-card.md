## Description:

Lightweight memory consolidation for OpenClaw agents that reviews recent daily memory files, extracts durable knowledge, and merges it into MEMORY.md without imposing a new file architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[balukov](https://clawhub.ai/user/balukov)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to consolidate recent daily memory journals into long-term MEMORY.md while preserving the existing memory structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Accidental or overly broad persistent memory updates could preserve, change, or remove long-term memory content.

Mitigation: Use explicit invocation or a clearly configured schedule, then review MEMORY.md changes before accepting them.

Risk: Sensitive details from daily memory files could be carried into reports or long-term memory.

Mitigation: Keep run notes brief and avoid copying secrets into reports or memory summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/balukov/skills/memory-sleep)

## Skill Output:

**Output Type(s):** [markdown, text, guidance]

**Output Format:** [Markdown edits to MEMORY.md plus a brief text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append a short consolidation note to today's daily memory file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
