## Description:

Convert rough project ideas into a human-readable blueprint and a clean OpenClaw execution packet for safe, scoped implementation and continuation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catcherintheroad-hub](https://clawhub.ai/user/catcherintheroad-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project owners use OpenClaw Pilot to turn fuzzy project goals or continuation feedback into a scoped blueprint and a packet-only OpenClaw handoff they can review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Execution packets are intended for later OpenClaw handoff and may carry incorrect or overbroad instructions if the initial goal or continuation feedback is ambiguous.

Mitigation: Review the generated blueprint and packet before handoff, confirming scope boundaries and removing instructions that exceed the requested work.

## Reference(s):

- [OpenClaw Pilot on ClawHub](https://clawhub.ai/catcherintheroad-hub/skills/openclaw-pilot)
- [New Project Example](artifact/examples/new-project.md)
- [Continuation Example](artifact/examples/continuation.md)
- [Output Contract Example](artifact/examples/output-contract.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown blueprint plus a plain text OpenClaw execution packet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Two-message contract: first a human-readable blueprint, then a packet-only handoff block.]

## Skill Version(s):

0.3.0-beta.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
