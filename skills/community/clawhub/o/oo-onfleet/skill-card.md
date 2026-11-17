## Description:

Use Onfleet through a connected OOMOL account to read and manage delivery tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use this skill to inspect delivery tasks and create, update, complete, clone, or delete tasks in their connected Onfleet account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback directs users to run a remote installer whose contents were unavailable for verification.

Mitigation: Review the CLI installation before enabling the skill and install a version you have verified yourself.

Risk: Creating, updating, completing, or deleting tasks can change or remove Onfleet data.

Mitigation: Keep the skill's explicit approval requirement for writes and deletions; confirm the exact action and target before execution.

## Reference(s):

- [Onfleet API documentation](https://docs.onfleet.com/reference/introduction)
- [Onfleet homepage](https://onfleet.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action responses and concise task-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write and destructive actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter; release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
