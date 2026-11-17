## Description:

Use HRMOS Kintai through a connected OOMOL account to read and manage attendance, employee, business partner, and related HR records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and HR administrators use this skill to look up attendance, leave, employee, workplace, and business partner information in a connected HRMOS Kintai account. It can also create, update, or delete supported records and export declaration data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified installers and introduce broader agent changes without clear user approval.

Mitigation: Review and approve a pinned, verified CLI installation separately, check its skill synchronization settings before first use, limit connected HRMOS permissions, and retain write and delete confirmations.

## Reference(s):

- [HRMOS Kintai](https://www.ieyasu.co/)
- [HRMOS Kintai API documentation](https://ieyasu.co/docs/api.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-hrmos-kintai)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, CSV files, Shell commands, Guidance]

**Output Format:** [JSON responses, downloadable CSV exports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected HRMOS Kintai account; actions that change or delete records require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
