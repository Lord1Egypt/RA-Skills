## Description:

Manage Miro through the REST API using OAuth 2.0, saved token files, or direct access tokens for board inspection, content changes, webhooks, exports, and raw API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to a Miro workspace, inspect boards, manage board items and webhooks, export board data, and preview or execute Miro REST API requests in a local workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth tokens and direct bearer tokens can expose the user's Miro workspace if they are logged, shared, or stored carelessly.

Mitigation: Use a least-privilege Miro app, avoid direct bearer-token entry in shared shells, store token files outside shared or synced folders, and rotate any token that appears in logs.

Risk: Write, delete, webhook, and raw API commands can alter live Miro boards or integrations.

Mitigation: Confirm board and item IDs, review the endpoint and request body before changes, and use preview-write for non-obvious writes before sending a live request.

Risk: Large board exports or raw API responses can expose workspace content in chat or files.

Mitigation: Prefer writing exports to local files, inspect results before sharing, and avoid dumping unnecessary board payloads into conversation logs.

## Reference(s):

- [Miro OAuth notes](artifact/references/miro-oauth-notes.md)
- [Miro request examples](artifact/references/miro-request-examples.md)
- [Miro REST API base](https://api.miro.com/v2)
- [Miro OAuth authorization endpoint](https://miro.com/oauth/authorize)
- [Miro OAuth token endpoint](https://api.miro.com/v1/oauth/token)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON API responses, and optional markdown, CSV, or JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live Miro API reads or writes when the user supplies credentials and confirms actions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
