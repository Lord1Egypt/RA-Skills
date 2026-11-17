## Description:

Print text, images, and QR codes to a wireless Bluetooth thermal printer from a MacOS device. Use `inkjet print` for output, `inkjet scan` to discover printers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronchartier](https://clawhub.ai/user/aaronchartier)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover Bluetooth thermal printers, print text or Markdown, print files and images, generate QR code printouts, and manage printer configuration from macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the inkjet package or Homebrew tap requires trusting third-party code.

Mitigation: Confirm that the package or tap is the intended source, use an unprivileged environment when possible, and avoid sudo.

Risk: Printed output is physical and may expose secrets, credentials, tokens, or personal data.

Mitigation: Do not print sensitive content unless the printer location and paper handling are trusted.

Risk: Printer configuration or aliases can route output to the wrong physical device.

Mitigation: Run `inkjet whoami` or specify `--address` before printing when device routing matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aaronchartier/skills/inkjet)
- [InkJet GitHub Homepage](https://github.com/AaronChartier/inkjet)
- [Publisher Profile](https://clawhub.ai/user/aaronchartier)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install or invoke `inkjet`, printer discovery steps, print commands, and configuration values for Bluetooth thermal printer setup.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
