## Description: <br>
Control Nanoleaf light panels via the Picoleaf CLI. Use for turning Nanoleaf on/off, adjusting brightness, setting colors (RGB/HSL), changing color temperature, or any Nanoleaf lighting control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rstierli](https://clawhub.ai/user/rstierli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to control Nanoleaf light panels through the Picoleaf CLI, including power, brightness, color, and color temperature changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup stores a Nanoleaf access token in ~/.picoleafrc. <br>
Mitigation: Keep ~/.picoleafrc private, preferably mode 600, and revoke or regenerate the token if the file is shared, backed up insecurely, or exposed. <br>
Risk: The skill depends on installing and trusting the Picoleaf CLI package source. <br>
Mitigation: Install only from package sources the user trusts and review the CLI source or release before deployment when required by local policy. <br>
Risk: Token generation requires physical access to the Nanoleaf controller. <br>
Mitigation: Only generate tokens when authorized to access the target device and complete pairing while physically present. <br>


## Reference(s): <br>
- [Picoleaf GitHub Project](https://github.com/tessro/picoleaf) <br>
- [Picoleaf Linux AMD64 Release Download](https://github.com/tessro/picoleaf/releases/latest/download/picoleaf_1.4.0_linux_amd64.tar.gz) <br>
- [Nanoleaf (Picoleaf) on ClawHub](https://clawhub.ai/rstierli/nanoleaf) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for a local Picoleaf CLI connected to a Nanoleaf controller.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
