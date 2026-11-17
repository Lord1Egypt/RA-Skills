## Description:

Control Govee smart lights through the Govee API, including power, brightness, RGB color, and device-state operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeynyc](https://clawhub.ai/user/joeynyc)

### License/Terms of Use:


## Use Case:

External users and developers with Govee accounts use this skill to list and control smart lights by name from an agent, including on/off, brightness, and color changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can change real Govee light state, including power, brightness, and color.

Mitigation: Run the list command first and use exact device names or IDs before changing device state.

Risk: The skill requires a Govee API key and depends on the requests package.

Mitigation: Keep GOVEE_API_KEY scoped to this use, install dependencies in a virtual environment, and consider pinning requests.

## Reference(s):

- [Govee Developer Portal](https://developer.govee.com/)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [ClawHub skill page](https://clawhub.ai/joeynyc/skills/govee-lights)
- [Publisher profile](https://clawhub.ai/user/joeynyc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GOVEE_API_KEY environment variable and the requests Python dependency.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
