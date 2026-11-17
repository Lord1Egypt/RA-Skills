## Description:

Send a quick email via SkillBoss API Hub without a local mail client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send email through SkillBoss/HeyBossAI from an agent workflow, including recipients, subject, HTML body, CC, and BCC fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipient lists, CC/BCC values, subject lines, and HTML body content are sent to SkillBoss/HeyBossAI's external API.

Mitigation: Use the skill only with an organization-approved provider and avoid sensitive or regulated content unless that external processing is approved.

Risk: The skill requires SKILLBOSS_API_KEY for authentication.

Mitigation: Store the API key as a secret environment variable and avoid exposing it in prompts, logs, examples, or shared configuration.

Risk: Incorrect recipient, CC, or BCC values can send email to unintended recipients.

Mitigation: Review all recipient fields and generated payloads before executing the email API call.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/mar-email-send)
- [HeyBossAI API endpoint](https://api.heybossai.com/v1)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API Calls]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends email payloads to the SkillBoss/HeyBossAI API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
