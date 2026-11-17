## Description:

Newsletter Automation provides four n8n workflows for double opt-in subscriber signup, welcome drip email sequencing, broadcast sends, and subscriber analytics with Google Sheets storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Developers, operators, and content teams use this skill to deploy a self-hosted newsletter pipeline for subscriber capture, confirmation, onboarding emails, broadcasts, and daily list analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A misconfigured public broadcast endpoint could send email to every confirmed subscriber.

Mitigation: Review before installing, set NEWSLETTER_SECRET to a strong random value, remove the public fallback secret, and protect broadcast webhooks with authentication or rate limiting before activation.

Risk: Subscriber-supplied fields or broadcast content could be rendered into email messages without enough validation.

Mitigation: Sanitize subscriber fields and email content before rendering or sending messages.

Risk: Signup abuse, privacy, or sheet-access gaps could expose subscriber data or create unwanted mail volume.

Mitigation: Add signup abuse controls, publish a privacy and consent notice, and restrict access to the subscriber Google Sheet.

Risk: Welcome drip state issues could cause onboarding emails to be sent more than once.

Mitigation: Fix and verify drip state tracking so each welcome email is sent only once per subscriber.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mhmalvi/skills/newsletter-automation)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with n8n workflow JSON and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires n8n, Google Sheets OAuth2, SMTP credentials, and NEWSLETTER_ADMIN_EMAIL, NEWSLETTER_BASE_URL, and NEWSLETTER_SECRET environment variables.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact metadata reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
