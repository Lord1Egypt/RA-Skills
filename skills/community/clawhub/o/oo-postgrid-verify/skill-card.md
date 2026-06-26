## Description: <br>
PostGrid Verify (postgrid.com). Use this skill for any PostGrid Verify request involving address search, parsing, verification, and lookup through the OOMOL connector rather than calling the API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run PostGrid Verify address autocomplete, parsing, standardization, and postal-code lookup actions through an OOMOL-connected account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address information is routed through OOMOL and PostGrid Verify. <br>
Mitigation: Use the skill only when the user is comfortable sending the relevant address data through those services. <br>
Risk: The skill may require installing or authenticating the OOMOL CLI and connecting a PostGrid Verify account. <br>
Mitigation: Run installation, login, or connection steps only when needed for the requested action or after an authentication or connection failure. <br>
Risk: Connector schemas can change over time. <br>
Mitigation: Inspect the live connector schema before constructing payloads for PostGrid Verify actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oomol/oo-postgrid-verify) <br>
- [OOMOL publisher profile](https://clawhub.ai/user/oomol) <br>
- [PostGrid Verify homepage](https://www.postgrid.com/address-verification/) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payloads or responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use the OOMOL oo CLI and should inspect the live connector schema before running an action.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
