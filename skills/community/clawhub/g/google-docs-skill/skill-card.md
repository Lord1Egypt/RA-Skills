## Description:

Integrate with the Google Docs API to create, read, update, format, and manage documents using OAuth 2.0 authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zagran](https://clawhub.ai/user/zagran)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to work with Google Docs through the official API, including document creation, retrieval, text insertion, formatting, batch updates, and common content operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples can expose OAuth refresh or access tokens in terminals, logs, CI, or agent transcripts.

Mitigation: Avoid printing tokens, store credentials in a secret store, and revoke any token that may have been exposed.

Risk: The skill enables document-changing Google Docs API access.

Mitigation: Grant only the Google account and document access required for the task, review API requests before execution, and confirm that write operations target the intended document.

## Reference(s):

- [Google Docs API Documentation](https://developers.google.com/docs/api)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Document Structure](https://developers.google.com/docs/api/concepts/structure)
- [Request Types Reference](https://developers.google.com/docs/api/reference/rest/v1/documents/request)
- [Python Quickstart](https://developers.google.com/docs/api/quickstart/python)
- [ClawHub Skill Page](https://clawhub.ai/zagran/skills/google-docs-skill)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides OAuth setup guidance and Google Docs API request examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
