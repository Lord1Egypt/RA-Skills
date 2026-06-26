## Description: <br>
Send NEAR reports and alerts via email with SMTP configuration, scheduling, and automatic reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaiss](https://clawhub.ai/user/shaiss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and NEAR account operators use this skill to configure SMTP delivery, generate account balance reports, and prepare email alerts or scheduled reporting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SMTP passwords can be exposed through shell history when passed with --pass and are stored locally in ~/.near-email/config.json. <br>
Mitigation: Use an app-specific SMTP password, verify local config file permissions, and avoid using this skill on shared machines. <br>
Risk: Alerts, scheduled reports, and actual email delivery are only partially implemented. <br>
Mitigation: Test reporting and delivery behavior before relying on the skill for operational notifications. <br>


## Reference(s): <br>
- [Nodemailer](https://nodemailer.com/) <br>
- [NEAR RPC API](https://docs.near.org/api/rpc) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes SMTP configuration to a local user config file when setup is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
