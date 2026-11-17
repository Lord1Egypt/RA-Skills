## Description:

Operate Smartsheet to read, create, update, and delete sheet data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and users use the skill to list and read Smartsheet sheets, and to add, update, or delete rows through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded code whose installers have not been reviewed.

Mitigation: Review CLI installation separately and use a pinned, verified distribution.

Risk: OOMOL may install or synchronize skills across connected agent tools, broadening changes beyond this Smartsheet task.

Mitigation: Decide whether to allow skill installation or synchronization, and disable it if unwanted.

Risk: Adding or updating rows changes Smartsheet data, and deleting rows removes data.

Mitigation: Confirm the exact payload and effect before writes; confirm the target and obtain explicit approval before deletions.

## Reference(s):

- [Smartsheet](https://www.smartsheet.com)
- [Smartsheet API documentation](https://developers.smartsheet.com/api/smartsheet/openapi)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Smartsheet skill release](https://clawhub.ai/oomol/skills/oo-smartsheet)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [JSON data with concise text summaries and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.4 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
