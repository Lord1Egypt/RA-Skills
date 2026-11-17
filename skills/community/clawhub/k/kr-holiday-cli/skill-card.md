## Description:

Korean public holidays, business-day calculations, and Korean lunar-solar date conversion through a local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to answer Korean public-holiday questions, calculate business days for scheduling workflows, and convert Korean lunar and solar dates without a runtime API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency updates can change holiday or lunar-calendar calculations over time.

Mitigation: Install in a virtual environment and pin or lock the holidays and korean-lunar-calendar dependencies for reproducible scheduling.

Risk: Ad-hoc Korean public holidays or legislative changes may not appear until the underlying holiday data is updated.

Mitigation: For high-impact scheduling, verify dates against official Korean holiday notices and update the holidays dependency before use.

## Reference(s):

- [holidays Python package](https://pypi.org/project/holidays/)
- [korean-lunar-calendar Python package](https://pypi.org/project/korean-lunar-calendar/)

## Skill Output:

**Output Type(s):** [Shell commands, Text, Guidance]

**Output Format:** [JSON responses and plain-text calendar output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [UTF-8 output with Korean holiday names preserved; no runtime network access or API key required.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
