## Description:

Pushes text notifications from OpenClaw to an Aligenie/Tmall Genie device for voice broadcast.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to send task completion notices, reminders, and requested text announcements through an Aligenie/Tmall Genie device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A publicly exposed relay can allow unauthorized voice broadcasts or credentialed API use.

Mitigation: Require HTTPS, authenticate callers, and restrict source networks before deploying the relay.

Risk: Sending AppSecret from the client on every push increases credential exposure.

Mitigation: Keep secrets server-side or in a managed secret store, and avoid passing AppSecret in routine push requests.

Risk: Startup persistence can keep a risky relay active after reboot.

Mitigation: Audit the server artifact and deployment configuration before enabling startup persistence.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/axelhu/skills/openclaw-aligenie-push)
- [Deployment guide](DEPLOY.md)
- [Aligenie developer portal](https://iap.aligenie.com)
- [Taobao OAuth token endpoint](https://oauth.taobao.com/token)
- [Aligenie push message endpoint](https://api.aligenie.com/v1.0/push/pushMsg)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets, plus JSON-like success or error responses for push calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires caller-provided Aligenie credentials, device openId, and push server configuration.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
