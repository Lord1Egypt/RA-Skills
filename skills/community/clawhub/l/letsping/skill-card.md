## Description: <br>
Human-in-the-loop approval for high-risk agent actions (sudo protocol). Agent must call letsping_ask before destructive/financial/social/infra changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cordialabsio](https://clawhub.ai/user/cordialabsio) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use letsping to route high-risk agent actions through a human approval step before destructive, financial, social, or infrastructure changes proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approval payloads could expose sensitive data if secrets are included. <br>
Mitigation: Use a dedicated LetsPing agent key and avoid sending secrets in approval payloads. <br>
Risk: The external runtime must be trusted before installation. <br>
Mitigation: Review the @letsping/openclaw-skill runtime before installing or deploying it. <br>
Risk: Human approval can reduce risk but does not replace OpenClaw permissions, authentication, or sandboxing. <br>
Mitigation: Keep OpenClaw permissions and sandbox controls in place and treat letsping as an added approval workflow. <br>


## Reference(s): <br>
- [ClawHub letsping listing](https://clawhub.ai/cordialabsio/letsping) <br>
- [LetsPing OpenClaw pairing](https://letsping.co/openclaw/pair) <br>
- [LetsPing](https://letsping.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns an approval result and authorized payload; rejected or timed-out requests should halt, retry safely, or ask for guidance.] <br>

## Skill Version(s): <br>
0.3.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
