## Description:

Operate ERPNext through an existing OOMOL-connected account using the oo CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to read and manage ERPNext records through an existing OOMOL connection. It guides action schema checks and requires confirmation before writes or deletions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup workflow installs remote CLI software, and the downloaded installers and hosted runtime were not independently verified.

Mitigation: Review and explicitly approve CLI installation before setup; prefer a verified, version-pinned release and check whether it installs skills into other agents.

Risk: The OOMOL connection can access ERPNext business data, and writes or deletions can change or remove records.

Mitigation: Use narrowly scoped ERPNext credentials, consider OOMOL's access to business data, and retain confirmation of the exact effect before writes or deletions.

## Reference(s):

- [ERPNext](https://erpnext.com)
- [Frappe REST API documentation](https://docs.frappe.io/framework/user/en/api/rest)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ERPNext skill page](https://clawhub.ai/oomol/skills/oo-erpnext)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [oo CLI commands and JSON payloads; ERPNext action results returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available results depend on the ERPNext action. Writes and deletions require user confirmation.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
