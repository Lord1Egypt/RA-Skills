## Description:

Analyze Kubernetes faults using only user-provided evidence by classifying the fault, ranking likely hypotheses, requesting the next highest-value checks, and keeping facts separate from guesses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghostwritten](https://clawhub.ai/user/ghostwritten)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and SREs use this skill to structure Kubernetes incident triage from evidence they provide, separating confirmed facts from hypotheses and identifying the next highest-value checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake advisory triage for live cluster inspection or remediation.

Mitigation: Treat the skill as advisory only; provide evidence explicitly and verify any recommended checks before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghostwritten/skills/kubernetes-triage-expert)
- [Ghostwritten publisher profile](https://clawhub.ai/user/ghostwritten)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured triage sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits active hypotheses and next checks to three each; preserves Kubernetes identifiers and exact error text.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
