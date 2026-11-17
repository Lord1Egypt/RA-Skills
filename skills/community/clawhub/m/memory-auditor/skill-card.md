## Description:

Audits an agent's current claims against stored memory to detect fabricated, drifted, or inconsistent memory details using token-level analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crftsmnd](https://clawhub.ai/user/crftsmnd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and QA teams use this skill to audit agent memory consistency, compare current claims with stored memory, and identify likely performed memory or context drift.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends raw agent memory and behavior text to a third-party endpoint, which may expose sensitive conversations, customer data, regulated data, or private memory contents.

Mitigation: Use only with non-sensitive data unless the operator has explicit privacy, retention, and service-trust assurances.

Risk: The evidence reports an exposed, unnecessary API key.

Mitigation: The publisher should remove or rotate the exposed key before production use.

Risk: The evidence warns that payment validation is not implemented properly.

Mitigation: Treat the paid flow as untrusted until the publisher implements proper payment validation.

## Reference(s):

- [Memory-Auditor ClawHub page](https://clawhub.ai/crftsmnd/skills/memory-auditor)
- [Memory Auditor API endpoint](https://memory-auditor.cvapi.workers.dev/audit)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON audit result with verdict, confidence score, analysis details, and comparison statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current behavior text, stored memory text, and optional threshold; paid audit flow is described by the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
