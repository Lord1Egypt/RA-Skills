## Description:

Provides decision support for medical-device adverse-event reporting pathways and rationales in structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device vigilance teams use this skill to triage adverse-event reports and obtain a suggested reporting pathway with supporting rationale for human review. It is decision support, not a final regulatory determination.

### Deployment Geography for Use:

China (regulatory context)

## Known Risks and Mitigations:

Risk: Adverse-event reports may contain identifiable patient, reporter, or company-confidential information.

Mitigation: Do not submit sensitive or regulated details until the processing and logging destination is confirmed; minimize or de-identify input.

Risk: The documentation-only skill requests command, file-write, and web access beyond its stated workflow.

Mitigation: Review permissions before installation; require explicit approval for external calls or file writes and restrict unnecessary access.

Risk: An incorrect suggested reporting pathway could affect a regulated reporting decision.

Mitigation: Have a qualified reviewer verify the recommendation against current official rules before acting.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/pms-vigilance-intake)
- [LGD theory referenced by the README](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggested reporting pathway and rationale; subject to human review.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
