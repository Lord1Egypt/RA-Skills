## Description:

Makes this agent a Proposer in an MPAS multi-party approval workflow. Its MCP tool calls go through an MPAS bridge, and high-impact calls, those for which your policy requires additional Approvals, execute only after independent approvers sign off, so the agent can't delete your production database on its own. Changes agent behavior by design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oma3](https://clawhub.ai/user/oma3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to propose application actions through an MPAS bridge, coordinate independent approvals, and track each action through completion or cancellation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Action details are shared with maintainers during approval review.

Mitigation: Use trusted bridges and approved maintainer channels, and share the action details only with appropriate reviewers.

Risk: Persistent role setup changes future agent behavior, and cancellation cannot undo an operation already dispatched.

Mitigation: Install the role preamble only when requested, remove it when disabling the role, and check the target system if execution timing is uncertain.

## Reference(s):

- [MPAS project](https://www.oma3.org/mpas)
- [MPAS project repository](https://github.com/oma3dao/mpas)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Tool-call proposals, approval notifications, and progress or outcome messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action details are preserved for approval and tracking; the skill does not provide approvals itself.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
