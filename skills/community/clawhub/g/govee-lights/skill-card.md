## Description: <br>
Control Govee smart lights via the Govee API. Supports turning lights on/off, adjusting brightness, setting colors, and scenes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeynyc](https://clawhub.ai/user/joeynyc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to control Govee smart lights by name, including turning devices on or off, adjusting brightness, and setting RGB colors through the Govee API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Govee API key that can control devices linked to the account. <br>
Mitigation: Keep the API key private and revocable, and only install the skill where device-control access is acceptable. <br>
Risk: Partial device-name matching can affect the wrong light when names are ambiguous. <br>
Mitigation: Run the list command first and use exact or distinctive device names before sending control commands. <br>
Risk: The skill depends on the third-party requests package and live Govee API availability. <br>
Mitigation: Install dependencies in a virtual environment and verify API errors against the included troubleshooting guidance. <br>


## Reference(s): <br>
- [Govee Developer Portal](https://developer.govee.com/) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/joeynyc/govee-lights) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require GOVEE_API_KEY and network access to the Govee API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
