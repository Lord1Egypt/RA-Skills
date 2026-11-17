## Description:

Use an OOMOL-connected account to search and read Dialpad WFM schedules, activity metrics, and agent metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Workforce operations teams use this skill to retrieve Dialpad WFM schedules, activity metrics, and agent metrics through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI installation path can execute remote code, and the remote installer and backend were not fully verified; the security review did not establish malicious behavior.

Mitigation: Review the CLI installation before enabling the skill, explicitly approve host changes, and decide whether automatic installation of other agent skills is acceptable.

Risk: The Dialpad connection and workforce data are handled through OOMOL.

Mitigation: Review OOMOL's connection and data handling for the intended workforce queries before connecting an account.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [Dialpad WFM API documentation](https://help.dialpad.com/docs/wfm-apis)
- [Dialpad workforce management](https://www.dialpad.com/features/workforce-management-software/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON data returned from Dialpad WFM actions, with shell command examples and setup guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only schedule and workforce metrics retrieved for a requested time interval; results may be paginated.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
