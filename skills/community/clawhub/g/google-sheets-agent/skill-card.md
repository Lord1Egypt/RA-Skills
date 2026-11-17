## Description:

Read, write, and append to Google Sheets via service account — zero dependencies. Use when an agent needs to access Google Sheets data, export spreadsheet contents, write rows, or list available sheets. Supports 1Password, env var, or file-based SA key loading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theagentwire](https://clawhub.ai/user/theagentwire)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to list, inspect, read, append, and overwrite Google Sheets through service account authentication in headless workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands described as read-only may request write-capable Google Sheets authorization.

Mitigation: Use a dedicated least-privilege service account, share sheets with Viewer access unless writes are needed, and confirm the script uses read-only scopes before relying on it for sensitive sheets.

## Reference(s):

- [Google Sheets Agent on ClawHub](https://clawhub.ai/theagentwire/skills/google-sheets-agent)
- [The Agent Wire](https://theagentwire.ai?utm_source=clawhub&utm_medium=skill&utm_campaign=google-sheets-agent)
- [The Agent Wire on X](https://x.com/TheAgentWire)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Google Sheets operations return JSON to stdout; setup guidance covers service account key loading through environment variables, file path, or 1Password.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
