## Description:

Use HackRF One SDR for frequency scanning, IQ capture, signal analysis, waterfall generation, and demodulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arsatyants](https://clawhub.ai/user/arsatyants)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, RF engineers, and authorized radio analysts use this skill to operate HackRF One workflows for lawful scanning, IQ capture, signal analysis, waterfall or spectrum visualization, and FM/AM/SSB demodulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support radio monitoring, capture, and demodulation workflows that may be unlawful or privacy-invasive without authorization.

Mitigation: Use only for lawful, authorized SDR work, and do not demodulate or record third-party communications without permission.

Risk: Fixed shared temporary capture paths can expose IQ or demodulated data in multi-user environments.

Mitigation: Run in a controlled single-user environment and replace fixed /tmp capture paths with private temporary directories before broader deployment.

## Reference(s):

- [Frequency Band Reference](references/frequency_bands.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide generation of IQ captures, PNG spectrum/waterfall plots, signal analysis reports, and WAV demodulation outputs through local HackRF and Python tooling.]

## Skill Version(s):

2.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
