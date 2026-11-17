## Description:

Lead Guardian provides AI-powered real estate lead response and qualification through SMS, email, or CRM webhook integrations to engage, qualify, and route buyer and seller leads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonbarnato](https://clawhub.ai/user/jonbarnato)

### License/Terms of Use:

MIT-0

## Use Case:

Real estate agents use this skill to automate initial lead engagement, collect qualification details, identify hot leads, and route ready buyers or sellers for direct follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private lead data and admin actions may be exposed without authentication.

Mitigation: Add authentication and authorization for the dashboard and APIs before installing or deploying.

Risk: Incoming SMS webhooks may be spoofed or tampered with if Twilio signatures are not validated.

Mitigation: Validate Twilio request signatures and reject untrusted webhook requests.

Risk: The app runs an externally reachable Flask debug server in the artifact.

Mitigation: Disable debug mode, bind safely, and deploy behind a production WSGI server or equivalent controlled runtime.

Risk: Lead conversations can include personal data processed through third-party services.

Mitigation: Document privacy, consent, retention, and third-party processing controls for lead conversations.

Risk: Dashboard-rendered conversation content may expose users to unsafe or unsanitized display behavior.

Mitigation: Sanitize dashboard rendering before deployment.

## Reference(s):

- [Lead Guardian ClawHub Skill Page](https://clawhub.ai/jonbarnato/skills/lead-guardian)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documentation and Python application code, with SMS text responses and JSON API responses when the app runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Twilio, OpenRouter, and optional agent phone configuration; stores lead conversations in SQLite when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
