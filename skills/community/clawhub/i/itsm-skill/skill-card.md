## Description: <br>
Automates ITSM ticket submission through Chromium and Selenium for quote requests, batch queries, and issue feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tutututu2020](https://clawhub.ai/user/Tutututu2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and support users can use this skill to submit ITSM tickets from an agent workflow, including ticket type, SKU, warehouse, remarks, and optional attachment details. It drives a browser session to interact with the ITSM system rather than producing a draft only. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds credentials that may be real. <br>
Mitigation: Review the code before installation, remove or replace embedded credentials, and rotate the credential if it is valid. <br>
Risk: The skill can submit real ITSM tickets without a separate review step. <br>
Mitigation: Run it only after confirming the ticket details and use an isolated environment or browser profile for execution. <br>
Risk: The setup flow may install packages or execute downloaded setup code on the user's machine. <br>
Mitigation: Review the setup behavior first and allow dependency installation only in an environment where those changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tutututu2020/itsm-skill) <br>
- [ITSM service endpoint used by the skill](https://itsm.westmonth.com/#/create) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files] <br>
**Output Format:** [Terminal logs and screenshot files from browser automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submits real tickets to an external ITSM system and may install local browser or Python dependencies during setup.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
