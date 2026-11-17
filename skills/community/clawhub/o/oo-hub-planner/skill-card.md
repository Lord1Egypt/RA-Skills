## Description:

Resource Flow (Hub Planner) (milientsoftware.com). Use this skill for ANY Resource Flow (Hub Planner) request — reading, creating, and updating data. Whenever a task involves Resource Flow (Hub Planner), use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Hub Planner account can retrieve project and resource details or list records, and can create projects or resources through the oo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code, and the CLI's broader skill synchronization behavior is not explained in the bundled skill.

Mitigation: Review and verify the CLI before setup; the publisher documents OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes to agent skill directories.

Risk: Creating projects or resources changes Hub Planner data, and resource creation can send an invitation email.

Mitigation: Connect only the intended Hub Planner account and confirm each creation or invitation before running it.

Risk: Remote installers and hosted connector behavior remain unverified.

Mitigation: Verify installer and connector behavior before relying on them.

## Reference(s):

- [Resource Flow (Hub Planner) homepage](https://www.milientsoftware.com/hub-planner)
- [Hub Planner API documentation](https://api-docs.hubplanner.com/)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-hub-planner)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON action results with concise textual summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions retrieve data; project and resource creation change account state and require user confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
