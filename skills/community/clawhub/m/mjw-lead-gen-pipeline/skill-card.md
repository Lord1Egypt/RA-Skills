## Description:

Full automated lead generation pipeline for web design agencies that finds local businesses without websites or with broken sites, builds demo HTML sites for them, sends personalized cold pitch emails, and tracks leads in leads.md.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michelle447](https://clawhub.ai/user/michelle447)

### License/Terms of Use:

MIT-0

## Use Case:

External web design agencies and operators use this skill to find local business prospects, generate demo websites, deploy previews, send personalized outreach, and track lead status through the sales pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically publish demo websites based on scraped business data.

Mitigation: Review each demo page before publication, use private or noindex previews, validate and escape scraped data, and remove unsupported claims.

Risk: The skill can send cold pitch emails from a Gmail account.

Mitigation: Confirm every recipient, sender identity, subject, message body, and demo URL before sending, and comply with applicable outreach and consent requirements.

Risk: Lead records may include business contact details and outreach status.

Mitigation: Keep clear deletion and retention controls for leads.md and deployed demos.

## Reference(s):

- [Lead Gen Pipeline Skill](https://clawhub.ai/michelle447/skills/mjw-lead-gen-pipeline)
- [Demo Site HTML Template](references/demo-site-template.md)
- [leads.md Schema](references/leads-schema.md)
- [Cold Pitch Email Template](references/pitch-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML, lead-tracking tables, deployment commands, and email copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce demo site files, lead records, deployment URLs, and cold outreach drafts or send instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
