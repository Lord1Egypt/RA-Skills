## Description:

Validate Mexican CURP, RFC, and NSS offline — checksum, structure, and birth date. No network, no PII leaves the machine. Use for Mexican KYC, onboarding, payroll, or form validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gfuentesdev](https://clawhub.ai/user/gfuentesdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can validate Mexican CURP, RFC, and NSS values locally during KYC, onboarding, payroll, and form processing. Use an authoritative identity check when you need to confirm a number belongs to a real person.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A valid format and checksum do not prove that an identifier belongs to a real person or matches a name.

Mitigation: Use an authoritative identity verification process when person or name matching is required.

Risk: Validation results can echo the submitted identifier and parsed personal details.

Mitigation: Handle results under your PII policies and avoid storing or logging them unless needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gfuentesdev/skills/mx-id-validators)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON validation results with structured error codes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include the submitted identifier and parsed fields.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
