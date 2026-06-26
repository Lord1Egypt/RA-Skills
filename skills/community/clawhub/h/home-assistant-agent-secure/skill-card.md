## Description: <br>
Control Home Assistant smart home devices securely using the Assist (Conversation) API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szafranski](https://clawhub.ai/user/szafranski) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to send natural-language smart-home requests through Home Assistant Assist while limiting agent behavior to the Conversation API and a restricted non-admin Home Assistant user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Home Assistant long-lived access token can authorize actions beyond the Conversation API according to the permissions of the Home Assistant user. <br>
Mitigation: Use a dedicated non-admin Home Assistant user with limited area and entity access, protect the token, and rotate it if exposed. <br>
Risk: Trusted Networks login bypass can undermine the restricted-user security model. <br>
Mitigation: Disable trusted-network login bypass by setting allow_bypass_login to false or removing the trusted_networks provider. <br>
Risk: Using curl with -k skips certificate verification for self-signed Home Assistant instances. <br>
Mitigation: Remove the -k option when the Home Assistant certificate is trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/szafranski/home-assistant-agent-secure) <br>
- [Publisher Profile](https://clawhub.ai/user/szafranski) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, HOME_ASSISTANT_URL, and HOME_ASSISTANT_TOKEN; sends requests to the Home Assistant Assist conversation endpoint.] <br>

## Skill Version(s): <br>
1.1.0 (source: _meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
