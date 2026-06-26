## Description: <br>
Bridge OpenClaw agent interactions to external programs such as Snarling, including state display, physical approval requests, notifications, and notification feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snarflakes](https://clawhub.ai/user/snarflakes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this plugin to route agent state, approval requests, and notifications to Snarling or another local interaction surface for physical approvals and feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval prompts, notification text, session identifiers, and callback secrets are sent to a local HTTP service. <br>
Mitigation: Install only with a controlled and trusted Snarling or custom endpoint, keep callback routes on localhost or private networks, and avoid putting sensitive content in notification text. <br>
Risk: Reusable callback secrets and session identifiers protect approval and notification callbacks. <br>
Mitigation: Set a strong OPENCLAW_APPROVAL_SECRET and rotate or restart if logs, endpoint access, or callback data may have been exposed. <br>
Risk: The security evidence says failed approval callbacks can log the expected approval secret. <br>
Mitigation: Patch or verify the installed version so failed callbacks never log the expected secret before relying on the bridge for approvals. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snarflakes/openclaw-interaction-bridge) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/snarflakes) <br>
- [Snarling interaction surface](https://github.com/snarflakes/snarling) <br>
- [Notification policy](https://github.com/snarflakes/openclaw-interaction-bridge/blob/main/NOTIFICATION_POLICY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, configuration] <br>
**Output Format:** [Text status strings and JSON callback payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Approval calls block until approved, rejected, timed out, or blocked; notifications can return reveal, dismiss, timeout, and timing feedback.] <br>

## Skill Version(s): <br>
1.6.3 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
