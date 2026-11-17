## Description:

Audit a codebase or directory for deletion candidates: dead code, unused dependencies, single-use abstractions, config that never varies, and duplicated helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[divyeshjayswal](https://clawhub.ai/user/divyeshjayswal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to ask an agent for a conservative cleanup audit of a codebase or directory. It produces ranked deletion candidates with supporting evidence and risk labels so humans can decide what to remove.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deletion candidates may be incorrect or incomplete if references are generated dynamically or are outside the searched target.

Mitigation: Treat the audit as review guidance only; require human review and supporting evidence before deleting code or dependencies.

Risk: The skill asks the agent to inspect a target codebase, which may expose sensitive source content to the agent session.

Mitigation: Run it only in approved workspaces and avoid using it on repositories that the reviewing agent is not authorized to read.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown deletion audit with paths, estimated removable LOC, evidence, risk labels, and a summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks deletion candidates and highlights the top three lowest-risk deletions to start with.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
