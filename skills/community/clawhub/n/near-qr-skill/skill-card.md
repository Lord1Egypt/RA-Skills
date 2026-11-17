## Description:

Generate QR codes for NEAR addresses and payment requests, and read NEAR QR codes from images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ussyalfaks](https://clawhub.ai/user/ussyalfaks)

### License/Terms of Use:

MIT

## Use Case:

Developers and users working with NEAR payment flows can generate QR image files for account addresses or payment requests, then decode NEAR QR images back into structured JSON for review or integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency and publishing-tool supply-chain exposure can affect local execution.

Mitigation: Install dependencies in a virtual environment, pin package versions where possible, and only run publishing commands for trusted package versions.

Risk: QR image decoding uses image parsing dependencies that may be exposed to malicious or malformed files.

Mitigation: Decode QR images only from trusted sources and keep image-processing dependencies updated.

Risk: Payment QR codes encode recipient and amount but do not verify recipient intent or submit transactions.

Mitigation: Review generated payment QR details before sharing or using them in a payment flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ussyalfaks/skills/near-qr-skill)
- [Publisher profile](https://clawhub.ai/user/ussyalfaks)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Configuration instructions]

**Output Format:** [PNG QR image files, JSON objects, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated payment QR codes encode recipient, amount, and optional memo; decoding requires pyzbar and the zbar system library.]

## Skill Version(s):

1.0.0 (source: frontmatter, molthub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
