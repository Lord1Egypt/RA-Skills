## Description:

Google Forms API integration with managed OAuth for creating forms, adding questions, exporting responses to Excel, and summarizing response data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dfaaa](https://clawhub.ai/user/dfaaa)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage Google Forms through a third-party Forms for Google Drive service, including creating surveys, adding questions, listing forms, exporting responses, and summarizing response data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form content or response-derived data may be sent to the third-party gformsfree.com service.

Mitigation: Review the third-party service, OAuth setup, and data-handling expectations before using the skill with sensitive forms or responses.

Risk: The unauthorized setup flow suppresses normal agent guidance and forces a verbatim onboarding message.

Mitigation: Review the setup flow before installation and ensure users understand the third-party app, Google sign-in, and API-key requirements.

Risk: Authorized operations depend on the GFORMS_API_KEY environment variable.

Mitigation: Store the API key as a secret, do not expose it in agent messages or logs, and regenerate it if it is disclosed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dfaaa/skills/google-forms-app)
- [Forms for Google Drive App](https://gformsfree.com/app)
- [Google Forms API Reference](https://developers.google.com/workspace/forms/api/reference/rest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with shell commands, Python snippets, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and the GFORMS_API_KEY environment variable for authorized operations.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata version is 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
