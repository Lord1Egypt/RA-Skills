## Description: <br>
Pushes text notifications from OpenClaw to an Aligenie/Tmall Genie device for spoken playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to send task status, reminders, and other short messages to a configured Aligenie/Tmall Genie device for voice playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The push server and credential flow are under-protected if exposed without access controls. <br>
Mitigation: Operate the push server behind authentication, HTTPS, and restricted ingress, and do not expose /push publicly without access control. <br>
Risk: AppSecret and device openId can be mishandled if stored in shared markdown or version-controlled files. <br>
Mitigation: Store Aligenie credentials and device identifiers in private environment configuration rather than shared documents or repositories. <br>
Risk: Voice playback can disclose sensitive reminders, personal data, secrets, or private task results to nearby listeners. <br>
Mitigation: Limit pushed content to non-sensitive notifications and review message content before sending it to a voice device. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-aligenie-push) <br>
- [Publisher profile](https://clawhub.ai/user/axelhu) <br>
- [Deployment guide](artifact/DEPLOY.md) <br>
- [Aligenie developer portal](https://iap.aligenie.com) <br>
- [Taobao OAuth token endpoint](https://oauth.taobao.com/token) <br>
- [Aligenie push API endpoint](https://api.aligenie.com/v1.0/push/pushMsg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and JSON status responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces voice-push request content and deployment/configuration instructions for an OpenClaw agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
