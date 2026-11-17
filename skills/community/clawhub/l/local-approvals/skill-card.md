## Description:

Local Approvals is a local human-in-the-loop approval system for managing agent permissions, approval history, and auto-approved categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaiss](https://clawhub.ai/user/shaiss)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to review, approve, deny, and optionally auto-learn local agent permission requests while retaining local JSON state for pending requests and decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The approval workflow is a weak boundary if requesting agents can invoke the approval CLI or edit state files directly.

Mitigation: Use it as a convenience workflow only and restrict agent access to the CLI and local state files before installation.

Risk: Learned broad categories can cause future operations to be auto-approved too widely.

Mitigation: Avoid learning broad categories and regularly inspect or reset auto-approved categories.

Risk: Local approval state may drift from intended policy over time.

Mitigation: Review approval history and reset agent categories when approval patterns look incorrect or stale.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shaiss/skills/local-approvals)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown guidance, and local JSON state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains pending request and approval state in local JSON files.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
