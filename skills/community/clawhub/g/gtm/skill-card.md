## Description: <br>
Register and operate a SendClaw email address so an agent can send, receive, reply to, and monitor low-volume outreach email. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to set up a SendClaw mailbox for task-oriented email communication, including outreach, replies, inbox checks, and follow-up under human-defined rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad authority to send and manage external email. <br>
Mitigation: Set explicit rules for approved recipients, allowed outreach, personal-information handling, and when drafts require human review before use. <br>
Risk: The sales framing can conflict with the service's acceptable-use limits for unsolicited or large-scale outreach. <br>
Mitigation: Use the skill only for permitted low-volume, task-oriented communication and do not use it for spam, deceptive messaging, or bulk campaigns. <br>
Risk: API keys, claim tokens, and remote heartbeat instructions can affect account control and agent behavior. <br>
Mitigation: Protect credentials, share claim tokens only with the account owner, and review remote heartbeat instructions before allowing the agent to follow them. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/codejika/gtm) <br>
- [SendClaw skill reference](https://sendclaw.com/skill.md) <br>
- [SendClaw heartbeat routine](https://sendclaw.com/heartbeat.md) <br>
- [SendClaw homepage](https://sendclaw.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, configuration] <br>
**Output Format:** [Markdown instructions with HTTP and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SendClaw API key; outbound email is subject to service quotas and monitoring.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
