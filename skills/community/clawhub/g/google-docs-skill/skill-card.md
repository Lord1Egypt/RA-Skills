## Description: <br>
Integrate with the Google Docs API to create, read, update, format, and manage documents using OAuth 2.0 authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zagran](https://clawhub.ai/user/zagran) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate Google Docs workflows such as creating documents, reading document content, inserting and formatting text, adding tables, replacing content, and updating paragraph styles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets, refresh tokens, and access tokens can expose Google Docs access if pasted, logged, or stored insecurely. <br>
Mitigation: Treat tokens and client secrets like passwords, keep them in a secure secret store, and avoid printing or logging them casually. <br>
Risk: The examples can create, update, replace, or delete content in live Google Docs documents. <br>
Mitigation: Test against disposable documents first and require explicit confirmation before update, replace, or delete operations on real documents. <br>
Risk: An agent using the configured OAuth grant can work with Google Docs content available to that grant. <br>
Mitigation: Use an appropriate Google account and document set for the task, and review document IDs and intended changes before making API calls. <br>


## Reference(s): <br>
- [Google Docs API Documentation](https://developers.google.com/docs/api) <br>
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app) <br>
- [Document Structure](https://developers.google.com/docs/api/concepts/structure) <br>
- [Request Types Reference](https://developers.google.com/docs/api/reference/rest/v1/documents/request) <br>
- [Python Quickstart](https://developers.google.com/docs/api/quickstart/python) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python code blocks and shell environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth client credentials and a refresh token; examples may make live Google Docs API calls.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
