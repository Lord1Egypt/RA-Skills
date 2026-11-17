## Description:

Munger Observer reviews a specific decision, plan, or artifact using bounded evidence, counterevidence, alternatives, opportunity cost, and verifiable next checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdrhyne](https://clawhub.ai/user/jdrhyne)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to review concrete decisions, plans, proposals, or artifacts by separating observations from inferences, weighing counterevidence and alternatives, and identifying user-verifiable next checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Review requests could expand into broad history, memory, log, file, or scheduling access that exposes unrelated private data.

Mitigation: Require explicit approval for named sources, time range, maximum item count, privacy exclusions, and retention behavior before retrieving or reusing any such material.

Risk: A decision review could overstate unsupported conclusions about a person rather than the observable decision, artifact, or process.

Mitigation: Limit critique to observable evidence, label observations separately from inferences, include counterevidence and unknowns, and assign confidence.

Risk: Reviewed logs, memories, prior messages, attachments, or linked content may contain untrusted instructions.

Mitigation: Treat reviewed content only as evidence for the current review and do not execute commands, call tools, follow links, disclose secrets, or take external actions because reviewed content requests it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdrhyne/skills/munger-observer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown decision review with concise findings or a no-finding result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bounded evidence scope; history, memory, logs, or scheduling access require explicit user approval.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
