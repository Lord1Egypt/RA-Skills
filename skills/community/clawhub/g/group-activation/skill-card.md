## Description: <br>
Handles joining and leaving group conversations on messaging platforms (WhatsApp, Signal, Telegram, etc.). Use when the owner tags the agent into a group chat to participate for a time-limited window, and when the agent needs to open or close the participation gate for a specific group. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanblanchfield](https://clawhub.ai/user/seanblanchfield) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to let an agent participate in an owner-approved group chat for a limited time, then return that group to mention-required mode automatically. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A group participation window could be opened for the wrong group or platform if message metadata is not trustworthy. <br>
Mitigation: Review the platform, group identifier, and requested duration before allowing the agent to patch live configuration. <br>
Risk: A failed scheduled cleanup could leave the agent responding in a group longer than intended. <br>
Mitigation: Monitor active group windows and verify that the closing job restores mention-required mode at the expected time. <br>
Risk: Unauthorized group activation could occur if owner-only wake controls are misconfigured. <br>
Mitigation: Confirm that OpenClaw restricts group activation to the owner before installing or using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seanblanchfield/group-activation) <br>
- [Publisher profile](https://clawhub.ai/user/seanblanchfield) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with configuration patch and scheduled job instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces time-limited group participation instructions for supported messaging platforms.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
