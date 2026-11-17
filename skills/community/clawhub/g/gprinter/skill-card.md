## Description:

Control and print text, barcodes, and QR codes on the Gprinter GP-C200V ESC/POS thermal printer via Node.js or command line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yardfarmer](https://clawhub.ai/user/yardfarmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create Node.js or CLI print workflows for GP-C200V-compatible ESC/POS receipt printers, including Chinese text, barcodes, QR codes, and basic image commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted host, port, file path, or print payload values could send data to an unintended printer or print unintended content.

Mitigation: Review the configured printer or bridge host before use, and validate externally supplied host, port, file path, and print payload values.

Risk: Raw TCP printing can expose print payloads on networks that are not trusted.

Mitigation: Use the skill only on trusted local networks or protected network paths, especially when printing sensitive content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yardfarmer/skills/gprinter)
- [ESC/POS Protocol Reference](esc-pos-protocol.md)
- [Gprinter Publisher Profile](https://clawhub.ai/user/yardfarmer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include printer host, port, print payload, file path, barcode or QR content, alignment, text size, feed, and cut options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
