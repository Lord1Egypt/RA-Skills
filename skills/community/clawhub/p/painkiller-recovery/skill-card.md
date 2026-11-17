## Description:

Use Painkiller to create a structured recovery prompt when an agent loses task context, repeats a failed approach, or needs a careful handoff in QA, software engineering, operations, research, data analysis, or customer support. It preserves supplied objectives, evidence, failures, and constraints while selecting one bounded next step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gggggggg424242](https://clawhub.ai/user/gggggggg424242)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use the skill to frame a concise recovery prompt after task drift, repeated failed attempts, or a handoff. The prompt carries forward verified context, failed attempts, and constraints so a receiving agent can choose a bounded next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint content is sent to an external service, and the service's privacy claims have not been independently verified.

Mitigation: Send only a minimal, non-sensitive checkpoint; exclude credentials, personal data, and unrelated conversation history. Review the returned prompt before reuse.

Risk: The full endpoint charges $0.99 USDC per successful request.

Mitigation: Use the free preview or explicitly choose the paid route only after reviewing the charge.

## Reference(s):

- [Painkiller Recovery on ClawHub](https://clawhub.ai/gggggggg424242/skills/painkiller-recovery)
- [Project repository link listed in README](https://github.com/gggggggg424242/painkiller-recovery-skill)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain-text recovery prompt or JSON messages array]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Frames supplied checkpoint details into a bounded next step; does not perform the task or guarantee recovery or correctness.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
