## Description:

Verifies math-heavy code for algorithmic correctness and numerical stability

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review mathematical models, algorithms, statistical routines, scientific code, and numerical implementations. It guides requirements mapping, derivation checks, stability assessment, test evidence collection, and grounded findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running tests or notebooks from an untrusted repository may execute untrusted code; the security review is incomplete because some local references were unresolved.

Mitigation: Check repository trust before execution and use an isolated environment without credentials or network access; review unresolved local references before relying on the security verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-pensive-math-review)
- [Clawdis metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance, Shell commands]

**Output Format:** [Markdown review report and JSON findings, with command examples where relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include source locations, exact anchors, and evidence; unverifiable findings are labeled UNVERIFIED or omitted.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
