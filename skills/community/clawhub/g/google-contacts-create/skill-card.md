## Description: <br>
Creates a new Google contact from JSON input and retries internally until the operation succeeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to add a contact to a configured Google account through the required `gog` tool and Composio credential. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create contacts in the configured Google account. <br>
Mitigation: Require explicit user approval and check for duplicate contacts before each creation. <br>
Risk: The skill depends on a local `gog` binary and a Composio API credential. <br>
Mitigation: Use a trusted `gog` binary and keep the Composio credential least-privilege where possible. <br>


## Reference(s): <br>
- [Google Contacts Create on ClawHub](https://clawhub.ai/zvirb/google-contacts-create) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls] <br>
**Output Format:** [JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a single operation result for the requested contact creation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
