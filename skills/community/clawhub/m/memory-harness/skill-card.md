## Description:

Runtime-enforced memory harness for OpenClaw that implements staged recall, pre-execution recall checks, intent classification, entity detection, memory compression, and status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taka3693](https://clawhub.ai/user/taka3693)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route memory recall for OpenClaw sessions, keeping generic turns lightweight while retrieving compact project or constraint context when prior work matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release overstates automatic safety and memory-control behavior.

Mitigation: Treat recall and pre-execution checks as advisory unless the publisher documents enforceable blocking behavior and fail-closed handling.

Risk: Broad recall triggers and optional writeback may persist selected conversation details.

Mitigation: Install only with clear retention, consent, and trigger policies for the workspace where it will run.

Risk: Structured logging can expose raw user messages.

Mitigation: Redact or disable raw prompt logging before use with sensitive, private, or regulated content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/taka3693/skills/memory-harness)
- [Publisher profile](https://clawhub.ai/user/taka3693)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance plus JSON and structured log lines from bundled Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recall digests are capped to five memory items; structured logs can include raw user message text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
