## Description: <br>
Automates MocCard website workflows to turn long article content into styled card images and return a ZIP download link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moccard](https://clawhub.ai/user/moccard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, or content creators use this skill to drive a browser session on MocCard, submit a long article with style choices, generate card images, and retrieve a ZIP or file download path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback download path can send live browser cookies to a configured backup server. <br>
Mitigation: Run only with a trusted backup server and a non-sensitive browser session, or remove/restrict the cookie-forwarding fallback to a verified first-party endpoint with explicit consent. <br>
Risk: Automated browser actions depend on live MocCard UI selectors and configured server values. <br>
Mitigation: Review input parameters and validate the workflow in a disposable session before using it on valuable content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moccard/memolecard-zh) <br>
- [MocCard website](https://www.moccard.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration] <br>
**Output Format:** [Bash execution output with a ZIP download URL or file URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires title, article content, style category, style index, and optional backup server URL inputs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
