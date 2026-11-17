## Description:

Detect and repair partial failures in Gougoubi PBFT operations, including missing activation, missing risk LP, missing results, and pending reward claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit a Gougoubi proposal after a partial batch failure and run only the requested recovery actions for activation, risk LP, result submission, or reward claiming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive state-changing crypto repairs through external local scripts that are not bundled or integrity-verified.

Mitigation: Use it only in a trusted Gougoubi checkout, review the exact script contents before repair, and prefer scan-only review before any state-changing action.

Risk: Incorrect transaction details, chain selection, or contract addresses could cause unintended repair or reward-claim actions.

Mitigation: Verify chain and contract addresses, inspect transaction details, and require wallet confirmation for every state-changing action or reward claim.

## Reference(s):

- [Gougoubi Recovery Ops on ClawHub](https://clawhub.ai/chinasong/skills/gougoubi-recovery-ops)
- [Gougoubi project repository declared in clawhub.json](https://github.com/gougoubi/gougoubi)
- [Gougoubi website declared in clawhub.json](https://gougoubi.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, structured JSON]

**Output Format:** [Structured JSON report with concise repair guidance and transaction hashes when repairs run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports detected gaps, repaired counts, transaction hashes, failures, warnings, and retryable failure status.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact clawhub.json declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
