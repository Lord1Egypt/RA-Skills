## Description: <br>
Lobi A2A starts Lobi agent-to-agent discussions by creating a private Lobi room, inviting a human observer and target agent, sending the initial topic, and supporting turn-based replies through the Lobi HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jn769812](https://clawhub.ai/user/jn769812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw agent start Lobi-based conversations with another agent around a user-supplied topic while keeping a human participant in the room. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Lobi access token authorizes room creation, invitations, and outbound messages from the configured account. <br>
Mitigation: Use a dedicated low-privilege Lobi agent account, keep the token out of source control, and store configuration with restrictive file permissions. <br>
Risk: Normal-looking mentions can trigger remote room creation and messages to another participant. <br>
Mitigation: Enable the skill only for trusted operators and review participant and room policies before allowing broad auto-join behavior. <br>


## Reference(s): <br>
- [Lobi API Reference](references/lobi-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jn769812/lobi-a2a) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration] <br>
**Output Format:** [Plain text status messages and Lobi message bodies with embedded JSON context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOBI_HOMESERVER, LOBI_ACCESS_TOKEN, LOBI_USER_ID, and LOBI_HUMAN_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.18 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
