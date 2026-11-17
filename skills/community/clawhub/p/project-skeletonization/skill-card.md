## Description:

Collaborative workflow for converting a complete business project into a reusable base skeleton while requiring inventory, keep/remove proposals, uncertain-item review, and user confirmation before changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agilebuilder](https://clawhub.ai/user/agilebuilder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn an existing business application into a reusable starter project by preserving common framework capabilities, removing business-specific modules, and adding minimal placeholders for verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to inspect and modify a project while removing business-specific functionality.

Mitigation: Review the proposed inventory, keep list, remove list, uncertain items, and key options before approving any transformation.

Risk: Database migrations, authentication, scheduled jobs, file storage, audit logs, or deployment configuration may be common infrastructure or business-specific behavior.

Mitigation: Treat those areas as explicit review points and verify build, tests, startup, and placeholder behavior after changes.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/agilebuilder/agilebuilder-skills/tree/master/skills/project-skeletonization)
- [ClawHub skill page](https://clawhub.ai/agilebuilder/skills/project-skeletonization)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with proposed file changes and command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before destructive transformations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
