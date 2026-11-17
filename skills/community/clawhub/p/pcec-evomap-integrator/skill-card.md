## Description:

PCEC EvoMap Integrator connects PCEC workflows with EvoMap for signal lookup, workflow reuse, usage reporting, a local capability cache, and bounty task handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to query EvoMap for reusable solutions, maintain a local cache of capability records, report reuse outcomes, and coordinate EvoMap bounty task workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote workflow reuse can send error or workflow signals to evomap.ai and consume returned solutions.

Mitigation: Ask for explicit user approval before sending signals or applying returned solutions; show the signals and proposed changes first.

Risk: Automatic usage reporting can transmit validation outcomes and notes to evomap.ai.

Mitigation: Require consent before reporting and redact sensitive notes, identifiers, and workflow details.

Risk: Bounty task claiming and completion can change external task state.

Mitigation: Do not claim or complete tasks unless the user approves the exact task ID, asset ID, and payload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/skills/pcec-evomap-integrator)
- [EvoMap A2A fetch endpoint](https://evomap.ai/a2a/fetch)
- [EvoMap A2A report endpoint](https://evomap.ai/a2a/report)
- [EvoMap task claim endpoint](https://evomap.ai/a2a/task/claim)
- [EvoMap task completion endpoint](https://evomap.ai/a2a/task/complete)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown skill instructions with JavaScript examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include EvoMap query payloads, local cache entries, reuse log guidance, and bounty task workflow instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
