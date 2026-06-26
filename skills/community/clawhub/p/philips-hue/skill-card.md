## Description: <br>
Local control of Philips Hue lights via API v1. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Aprilox](https://clawhub.ai/user/Aprilox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and home automation users can use this skill to check and update Philips Hue lights on a local network through a Hue Bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted color values can cause hue.sh to run unintended local Python code. <br>
Mitigation: Validate hex colors with a strict pattern such as #[0-9A-Fa-f]{6}, and pass only trusted color values until the script is patched. <br>
Risk: The Hue Bridge API key is stored in a skill-local .env file. <br>
Mitigation: Keep the .env file private, do not commit it, and avoid placing the API key in shared prompts, screenshots, or workspace documentation. <br>


## Reference(s): <br>
- [Philips Hue Developer Portal](https://developers.meethue.com/) <br>
- [ClawHub Philips Hue skill page](https://clawhub.ai/Aprilox/philips-hue) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Philips Hue Bridge settings from a skill-local .env file.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
