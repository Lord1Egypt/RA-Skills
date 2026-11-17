## Description:

Controls Buttplug.io-compatible BLE intimate devices through Intiface Central and buttplug-mcp using natural-language agent commands across macOS, Windows, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amandaclarke61](https://clawhub.ai/user/amandaclarke61)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent list, start, stop, and set vibration strength for locally connected Intiface/Buttplug-compatible devices after installing Intiface Central, buttplug-mcp, and mcporter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can activate intimate hardware without sufficient consent, device verification, or safety controls.

Mitigation: Use only where all affected people have explicitly consented, list and verify the connected device before control, start at low intensity, and keep the stop command available.

Risk: A local Intiface server left running after use can leave connected device control available longer than intended.

Mitigation: Stop vibration after timed sessions and close or stop the local Intiface server when it is not in use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amandaclarke61/skills/intiface-control)
- [Buttplug.io compatible device index](https://iostindex.com)
- [Intiface Central](https://intiface.com/central/)
- [buttplug-mcp releases](https://github.com/ConAcademy/buttplug-mcp/releases)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Intiface Central, buttplug-mcp, and mcporter; device vibration strength is controlled with numeric values from 0.0 to 1.0.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
