## Description:

Reviews Phoenix LiveView code for lifecycle patterns, assigns/streams usage, components, and security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Phoenix LiveView modules, HEEx templates, and LiveComponents for lifecycle, assigns, streams, component, and security issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill requires loading an unbundled sibling review-verification-protocol skill outside the reviewed package.

Mitigation: Install only after reviewing and trusting that adjacent protocol, or ask the publisher to bundle or pin it inside this package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/liveview-code-review)
- [Assigns and Streams](references/assigns-streams.md)
- [LiveView Components](references/components.md)
- [LiveView Lifecycle](references/lifecycle.md)
- [LiveView Security](references/security.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review findings with file and line anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are gated by explicit file evidence, verification protocol use, line anchors, and LiveView valid-pattern screening.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
