## Description: <br>
Generates an OpenClaw mobile control center pairing code using the local gateway token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szx19970521](https://clawhub.ai/user/szx19970521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to create a pairing code for connecting a mobile control app to a BFF URL, then receive the pairing code, output file path, and next step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced PowerShell script is missing from the artifact, so its handling of the gateway token and pairing data cannot be reviewed from the submitted files. <br>
Mitigation: Obtain and inspect scripts/generate-mobile-pairing.ps1 before use; confirm the BFF URL is trusted and understand where the gateway token, pairing code, output file, and clipboard contents go. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szx19970521/openclaw-mobile-pair) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with a PowerShell command and short actionable text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a pairing code, output file path, and clipboard-copy behavior when the referenced script is present.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
