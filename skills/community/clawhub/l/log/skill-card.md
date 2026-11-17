## Description:

A privacy-first, local-first provenance protocol for agent workflows that emits structured audit records for important decisions, tool calls, state changes, and errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agistack](https://clawhub.ai/user/agistack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to emit privacy-safe structured audit records for important workflow events, debugging traces, source-aware decision summaries, and approval signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit records may expose secrets, private data, or hidden reasoning if agents include raw sensitive content.

Mitigation: Emit minimal factual summaries, redact secrets as [SECRET_REDACTED], avoid hidden chain-of-thought, and log sensitive personal data only by category unless explicitly required and authorized.

Risk: Users may assume the skill enforces persistence, retention, encryption, immutability, or approval blocking.

Mitigation: Configure those controls in the host environment; this skill only formats records and emits approval signals.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Markdown fenced json block prefixed by [LOG_ENTRY]]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records should be concise, redacted, source-aware, and limited to important workflow events.]

## Skill Version(s):

1.1.1 (source: skill.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
