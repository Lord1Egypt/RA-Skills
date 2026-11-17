## Description:

Google Workspace admin and investigation tool via service account and domain-wide delegation for Vault, Gmail, Directory, Reports, Drive, Calendar, Sheets, Docs, and People read workflows across a Google Workspace domain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmac122](https://clawhub.ai/user/jmac122)

### License/Terms of Use:

MIT-0

## Use Case:

Google Workspace administrators, security teams, and investigators use this skill to query user mailboxes, Vault search results, audit logs, directory records, files, calendars, spreadsheets, documents, and contacts during authorized domain investigations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad domain-wide delegation can expose email, files, calendars, contacts, Vault data, and directory information across users.

Mitigation: Deploy only in a tightly controlled admin environment after legal and security approval, using a dedicated least-privilege service account.

Risk: Service account JSON keys and delegated tokens are sensitive credentials.

Mitigation: Store keys outside repositories with restricted file permissions, restrict invocation access, rotate keys, and avoid logging or echoing credentials.

Risk: Full email bodies or Vault exports may reveal highly sensitive personal or business data.

Mitigation: Require documented case IDs and target users for each query, summarize results by default, and perform full content retrieval or exports only when explicitly approved.

Risk: Unpinned dependencies can change behavior over time.

Mitigation: Pin and review Google API Python dependencies before installation in production environments.

## Reference(s):

- [GWS Skill setup checklist](references/setup-checklist.md)
- [ClawHub skill page](https://clawhub.ai/jmac122/skills/gws-dwd)
- [Metadata homepage](https://github.com/jmac122/gws-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts return JSON or text from Google Workspace API reads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, Google API Python dependencies, and GWS_SERVICE_ACCOUNT_PATH, GWS_ADMIN_EMAIL, and GWS_DOMAIN environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
