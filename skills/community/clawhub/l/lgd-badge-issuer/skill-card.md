## Description:

Issues an lgd-certified badge certificate with a SHA-256 fingerprint and dated issuance record based on supplied evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automated review workflows use this skill to produce a badge certificate and issuance record from submitted qualification evidence. Treat the result as a local record, not verified proof of compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A badge may be issued even when supplied evidence says required checks failed, weakening its value as an approval or audit credential.

Mitigation: Require independently validated passing results tied to the holder, record refusals, and treat generated badges as local records rather than verified compliance credentials.

Risk: Writing the registry or certificate through a symbolic link or into an unsuitable output location may affect unintended files.

Mitigation: Use a dedicated output directory and avoid symbolic links.

## Reference(s):

- [LGD theory (canonical reference)](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [Protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [JSON, Files, Text]

**Output Format:** [JSON certificate and issuance ledger records, with text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Certificates include a SHA-256 fingerprint and issuance timestamp. A generated badge does not by itself establish that the supplied checks passed.]

## Skill Version(s):

1.0.12 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
