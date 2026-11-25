## Description:

Guide minimal code via a decision ladder with full safety, edge, and negative-case coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill before adding or changing code, choosing dependencies, or reviewing a diff. It guides them to prefer the simplest adequate implementation while retaining correctness, safety, performance, and edge-case handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because four local references could not be resolved, so the available scan evidence may not cover everything they contain.

Mitigation: Resolve and review the referenced files, then review and scan the skill before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-conserve-elegant-code)
- [Project homepage listed in ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conserve)

## Skill Output:

**Output Type(s):** [Code, Guidance, Analysis]

**Output Format:** [Natural-language guidance and code in the agent conversation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No fixed output schema; applies a decision ladder and preserves safety, correctness, performance, and edge-case requirements.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
