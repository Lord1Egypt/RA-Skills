## Description: <br>
A passive anti-distillation monitoring and alerting skill that watches request patterns for possible knowledge-distillation activity and alerts the operator without modifying responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to monitor request metadata for suspicious distillation patterns and receive alerts for manual review. It is intended for passive detection and audit logging, not automated countermeasures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The public listing name and version differ from the artifact frontmatter, which can make release identity harder to verify. <br>
Mitigation: Confirm the ClawHub listing, publisher handle, and release hash before installation. <br>
Risk: Webhook or email alert channels can send detection metadata to external destinations. <br>
Mitigation: Configure only trusted alert endpoints or recipients, and store webhook URLs and SMTP credentials in platform secret storage. <br>
Risk: The skill reads request metadata and does not specify a retention period for audit logs. <br>
Mitigation: Review the disclosed metadata fields and confirm logging retention is acceptable for the deployment environment. <br>
Risk: Model or autonomous invocation would be inappropriate for a passive monitoring skill. <br>
Mitigation: Verify after installation that autonomous execution and model invocation remain disabled in the platform. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wscats/omg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Configuration, Guidance] <br>
**Output Format:** [Structured alert reports, audit log entries, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alerts may be written to logs by default or sent through configured webhook or email channels.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release metadata; SKILL.md frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
