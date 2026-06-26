## Description: <br>
Send a quick email via SkillBoss API Hub without a local mail client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to compose outbound email requests through the SkillBoss API Hub, including recipient, CC, BCC, subject, and HTML body fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outbound email content, recipient addresses, and authentication credentials are handled through the SkillBoss API provider. <br>
Mitigation: Install only when the provider is trusted, keep SKILLBOSS_API_KEY secret, and avoid regulated or highly sensitive email content unless the provider is approved by the organization. <br>
Risk: Mistyped recipient, CC, or BCC fields can send email to unintended recipients. <br>
Mitigation: Review recipient fields and message body before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/mar-email-send) <br>
- [SkillBoss API endpoint referenced by the skill](https://api.heybossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends user-provided email data to the SkillBoss API endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
