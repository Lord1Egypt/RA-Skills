## Description: <br>
Reads Intercom conversations by listing, finding, or searching them with JSON input and output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duyeng](https://clawhub.ai/user/duyeng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and support operations agents use this skill to retrieve Intercom support conversations for read-only lookup, triage, and customer context review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose customer support conversations to the agent context. <br>
Mitigation: Install it only for agents permitted to view Intercom conversations and treat returned content as customer-sensitive. <br>
Risk: A broad Intercom token could grant more conversation access than the intended workflow requires. <br>
Mitigation: Use the narrowest available read-only Intercom access token and avoid broad workspace tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duyeng/intercom-conversations) <br>
- [OpenAPI contract](artifact/openapi.yaml) <br>
- [Skill usage documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Guidance] <br>
**Output Format:** [JSON objects with ok/action status, conversation data, pagination cursors, or structured errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires INTERCOM_ACCESS_TOKEN and returns Intercom conversation content that may be customer-sensitive.] <br>

## Skill Version(s): <br>
1.0.1 (source: clawhub.skill.json, package.json, openapi.yaml, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
