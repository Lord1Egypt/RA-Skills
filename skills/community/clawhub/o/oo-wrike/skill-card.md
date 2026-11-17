## Description:

Wrike (wrike.com). Use this skill for ANY Wrike request — reading, creating, and updating data. Whenever a task involves Wrike, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can search and read Wrike folders, tasks, and contacts, or create folders and tasks through their connected Wrike account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can run downloaded CLI installers, and the downloaded installers and hosted implementation were not verified.

Mitigation: Review and explicitly approve CLI installation; prefer a verified, fixed release before use.

Risk: Automatic skill deployment may introduce lasting changes beyond Wrike.

Mitigation: Review the deployment behavior and set OO_SKILLS_SYNC_DISABLED to disable startup synchronization when appropriate.

Risk: Folder and task creation actions change Wrike data.

Mitigation: Confirm the exact action payload and effect before running a write action.

## Reference(s):

- [Wrike API documentation](https://developers.wrike.com/docs/overview)
- [Wrike](https://www.wrike.com)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell command instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned data depends on the selected Wrike action.]

## Skill Version(s):

1.0.4 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
