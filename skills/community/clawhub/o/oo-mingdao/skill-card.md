## Description:

Use Mingdao through a connected OOMOL account to read and manage workspace data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected Mingdao account can inspect application data and perform workspace tasks such as managing records, roles, views, and workflows. Changes to Mingdao data should be reviewed and approved before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run a downloaded installer without separate approval, and the installer may add or update skills in other agents.

Mitigation: Review and separately approve CLI installation, prefer a verified release, and confirm any changes it proposes to other agents.

Risk: The external installer and Mingdao connector behavior have not been verified.

Mitigation: Limit the connected Mingdao account's permissions and retain explicit approval for each write or destructive action.

## Reference(s):

- [Mingdao API documentation](https://help.mingdao.com/api/introduction/)
- [Mingdao](https://www.mingdao.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API responses, Guidance]

**Output Format:** [Shell commands with JSON payloads and JSON API responses; discussion results may also be formatted as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user approval.]

## Skill Version(s):

1.0.3 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
