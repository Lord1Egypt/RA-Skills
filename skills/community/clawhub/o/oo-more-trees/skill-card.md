## Description:

More Trees (moretrees.eco). Use this skill for ANY More Trees request — reading, creating, and updating data. Whenever a task involves More Trees, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill through their connected OOMOL account to read More Trees account, forest, and project information, and to create or gift tree plantings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified CLI installer software that may affect installed agent skills.

Mitigation: Review and approve the CLI installation separately. Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup writes to agent skill directories.

Risk: Planting actions can use credits and create plantings or gifts for recipients.

Mitigation: Confirm the planting quantity, recipients, and credit cost before running a plant_trees action.

## Reference(s):

- [More Trees](https://www.moretrees.eco)
- [More Trees API documentation](https://www.moretrees.eco/learn/user-guides/api)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON service responses and concise natural-language guidance, issued through shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return account, forest, or project data; planting actions can create or gift trees.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
