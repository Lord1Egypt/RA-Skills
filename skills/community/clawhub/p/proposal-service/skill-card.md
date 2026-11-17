## Description:

Inspect and create real OpenClaw proposals in public.openclaw_proposals for the current closed-loop workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecosincronia](https://clawhub.ai/user/ecosincronia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect duplicate pending OpenClaw proposals and create trigger-driven stale-missions proposals in the current closed-loop workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create real pending proposals in the OpenClaw database.

Mitigation: Run the duplicate-check command first and require explicit approval before running create-stale-proposal.

Risk: The current database access uses a powerful postgres role through Docker.

Mitigation: Use a dedicated least-privilege database role before broader deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecosincronia/skills/proposal-service)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands and guidance for checking duplicate stale-missions proposals or creating a pending proposal.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
