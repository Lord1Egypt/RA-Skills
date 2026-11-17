## Description:

Search and read Drata company, control, personnel, vendor, and workspace data through a connected Drata account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers can retrieve Drata workspace data, including company details, controls, personnel, vendors, and workspaces. The skill uses a connected Drata account and returns the requested records for review or follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required CLI can make lasting changes to other agents’ installed skills, and the remote installers and live connector implementation remain unverified.

Mitigation: Review the CLI separately before installing, use a reviewed fixed release, and consider setting OO_SKILLS_SYNC_DISABLED=1 before invoking it.

Risk: Using Drata exposes sensitive workspace records to OOMOL handling.

Mitigation: Connect Drata with read-only access and ensure you accept OOMOL handling sensitive records.

## Reference(s):

- [Drata](https://drata.com)
- [Drata API reference](https://developers.drata.com/openapi/reference/v2/overview/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance, Shell commands]

**Output Format:** [JSON data and concise Markdown summaries, with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live data depends on the connected Drata account and its permissions.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
