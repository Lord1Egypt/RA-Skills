## Description:

Analyzes PNG files for structure, CRC integrity, sRGB/gAMA/pHYs metadata, and common LSB steganography patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moxin1044](https://clawhub.ai/user/moxin1044)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security analysts, and CTF participants use this skill to inspect PNG structure, validate chunk CRCs, extract image metadata, and look for readable text in common LSB patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Large PNG files may consume significant local processing resources during image loading and pixel-level LSB analysis.

Mitigation: Use the skill on trusted or challenge-context PNGs of reasonable size, as recommended by the security guidance.

Risk: The optional JSON report can overwrite or modify a path chosen by the user.

Mitigation: Write reports only to intended output locations and review the path before execution.

Risk: Readable LSB output is a signal for manual review, not definitive proof of hidden content.

Mitigation: Treat decoded characters as leads and confirm findings with human analysis or additional tools.

## Reference(s):

- [LSB steganography pattern reference](artifact/references/lsb_patterns.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional JSON analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The analyzer reads a user-provided PNG, prints a text summary by default, and can write a JSON report when an output path is supplied.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
