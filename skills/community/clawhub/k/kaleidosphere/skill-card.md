## Description:

Use for bounded KaleidoSphere status, discovery, analyze, plan, preview, readback, or advisory BI presentation review; reject unsafe authority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jofe2](https://clawhub.ai/user/jofe2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare bounded KaleidoSphere requests for status, discovery, analysis, planning, preview, readback, or advisory BI presentation review while preserving an authority-free contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local validator may not provide complete data-loss-prevention coverage.

Mitigation: Use host-side schema validation before external dispatch and avoid placing sensitive data or raw BI rows in optional fields.

Risk: Requests could be routed through untrusted transport if a configured KaleidoSphere transport is missing.

Mitigation: Stop with WAITING_EXTERNAL when no trusted transport is configured, and do not accept arbitrary URLs or user-supplied secrets as a workaround.

Risk: Advisory visual review could be mistaken for evidence of BI truth or production readiness.

Mitigation: Verify data, claims, provenance, accessibility, approvals, and readiness independently before relying on presentation guidance.

## Reference(s):

- [KaleidoSphere contract](references/contract.json)
- [ClawHub skill page](https://clawhub.ai/jofe2/skills/kaleidosphere)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Markdown sections with closed JSON request details and validation status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed facts, computed facts, inferred candidates, human decisions, authority boundaries, and non-claims when present.]

## Skill Version(s):

0.18.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
