## Description:

Helps agents design and operate a Harness-style control layer for OpenClaw setups by routing tasks, preflighting risky actions, defining verification checks, and promoting repeated incidents into playbooks or skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warren2008-2020-spec](https://clawhub.ai/user/warren2008-2020-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate OpenClaw work across skill routing, memory or context routing, safety preflight, execution checks, verification, and incident learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad routing skill can influence how an agent approaches sensitive operations.

Mitigation: Keep normal OpenClaw permissions and approvals in force, and require exact targets, blast radius, rollback or backup path, and verification checks before risky actions.

Risk: Incorrect routing or weak completion checks could leave work only partially verified.

Mitigation: Define objective verification before execution and state any remaining risk when verification cannot be completed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/warren2008-2020-spec/skills/harness-control-layer)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown and structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing recommendations, safety preflight criteria, verification checks, and incident-learning records for OpenClaw tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
