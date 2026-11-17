## Description:

Read or write a user's Google Sheets, Docs, Drive, or Calendar from code via a Google service account - headless, no OAuth browser flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amiller](https://clawhub.ai/user/amiller)

### License/Terms of Use:

MIT

## Use Case:

Developers, engineers, and agent operators use this skill to set up or use Google service-account credentials for headless access to explicitly shared Sheets, Docs, Drive files, and Calendars. It helps an agent explain setup, choose scopes, troubleshoot sharing errors, and produce runnable Python or shell examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful Google service-account credentials that can access shared Google resources.

Mitigation: Keep credentials.json out of shared folders and source control, prefer secret injection such as CREDS_JSON, and rotate keys if they leak.

Risk: Examples can write to live Google Docs and Sheets.

Mitigation: Run write examples first on test documents, read a document before editing it, and use read-only scopes when write access is not needed.

Risk: Over-broad sharing or scopes can give an agent more access than intended.

Mitigation: Share only the specific files or calendars needed, use Viewer plus read-only scopes for read-only tasks, and use one service account per job.

## Reference(s):

- [Google Cloud SDK install](https://cloud.google.com/sdk/docs/install)
- [gspread authentication](https://docs.gspread.org/en/latest/oauth2.html)
- [Google Workspace create access credentials](https://developers.google.com/workspace/guides/create-credentials)
- [Google IAM service accounts overview](https://cloud.google.com/iam/docs/service-account-overview)
- [OAuth 2.0 service accounts](https://developers.google.com/identity/protocols/oauth2/service-account)
- [OAuth 2.0 scopes for Google APIs](https://developers.google.com/identity/protocols/oauth2/scopes)
- [Best practices for service accounts](https://cloud.google.com/iam/docs/best-practices-service-accounts)
- [google-auth service_account reference](https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html)
- [ClawHub skill page](https://clawhub.ai/amiller/skills/google-service-accounts)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands, Python snippets, scope choices, and troubleshooting steps for Google service-account access.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
