## Description: <br>
Control LG smart appliances via ThinQ API, including checking status, changing refrigerator temperatures, toggling express and eco modes, and monitoring door status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiofreitas](https://clawhub.ai/user/kaiofreitas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and control their LG ThinQ appliances through the ThinQ Connect API. It is intended for appliance status checks, refrigerator temperature updates, mode toggles, and washer or dryer monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send unrestricted raw control commands to real appliances using the user's ThinQ account token. <br>
Mitigation: Avoid the raw command unless the exact payload and target device have been personally reviewed. <br>
Risk: The ThinQ token file grants appliance-control access if exposed. <br>
Mitigation: Store the token file securely and install the skill only when you trust the publisher. <br>
Risk: The bundled CLI depends on the external thinqconnect package. <br>
Mitigation: Verify the thinqconnect package before installing or running the skill. <br>


## Reference(s): <br>
- [LG ThinQ Personal Access Token Portal](https://connect-pat.lgthinq.com) <br>
- [ClawHub LG ThinQ Skill Page](https://clawhub.ai/kaiofreitas/lg-thinq) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke ThinQ API calls that read appliance status or send appliance-control commands when the agent runs the bundled CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
