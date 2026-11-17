## Description:

OpenStatus (openstatus.dev). Use this skill for ANY OpenStatus request — reading, creating, updating, and deleting data. Whenever a task involves OpenStatus, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and service operators use the skill to inspect OpenStatus monitors, statuses, response logs, and metrics, and to create, update, trigger, or delete monitors through their connected account. The skill requires confirmation before state-changing actions and explicit approval before deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CLI setup may execute unverified code or install persistent agent skills beyond the requested task.

Mitigation: Review the CLI installer and its additional skill-installation behavior before setup, and use the publisher's documented startup synchronization controls.

Risk: Monitor changes and deletions affect the connected OpenStatus workspace.

Mitigation: Confirm the exact effect before write actions and obtain explicit approval for deletions, as the skill's safety guidance requires.

## Reference(s):

- [OpenStatus](https://www.openstatus.dev)
- [OpenStatus API documentation](https://www.openstatus.dev/tooling/api)
- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)

## Skill Output:

**Output Type(s):** [JSON data, Guidance]

**Output Format:** [JSON connector responses with natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live monitor and check data; state-changing operations require confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
