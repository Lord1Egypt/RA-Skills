## Description:

Reviews Phoenix code for controller patterns, context boundaries, routing, and plugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Phoenix applications for controller structure, bounded context boundaries, routing conventions, plug composition, authentication, authorization, and JSON API patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an unbundled review-verification-protocol sibling skill, so a missing or changed dependency can influence review findings.

Mitigation: Use only with a controlled, reviewed, and pinned copy of review-verification-protocol, or require the publisher to vendor that protocol inside the package.

## Reference(s):

- [Phoenix Contexts](references/contexts.md)
- [Phoenix Controllers](references/controllers.md)
- [Phoenix Routing](references/routing.md)
- [Phoenix Plugs](references/plugs.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review findings with anchored file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to use the [FILE:LINE] ISSUE_TITLE pattern after evidence and verification gates pass.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
