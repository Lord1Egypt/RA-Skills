## Description:

Checks a badge certificate's required fields and fingerprint, with an optional registry lookup for a matching serial and fingerprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Supply-chain reviewers and compliance teams can use it for preliminary checks of badge certificate structure and fingerprints, and optionally compare a serial and fingerprint with a supplied registry. Do not use a passing result alone to establish authenticity or approve a supplier.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A passing result can still approve a fabricated certificate and does not establish authenticity or non-revocation.

Mitigation: Do not rely on this result alone for supplier approval; verify against an issuer-controlled registry with explicit revocation enforcement and strict evidence-hash validation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/lgd-badge-verify)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)
- [LGD formal paper](https://doi.org/10.5281/zenodo.22456647)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Human-readable verification report or JSON report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports certificate check results and, when a registry is supplied, serial and fingerprint comparison.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
