## Description:

Reviews iOS animation code for correctness, performance, accessibility, and Apple API best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift and iOS animation code for grounded findings about correctness, performance, accessibility, and Apple animation API usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce inaccurate code-review findings if animation claims are not anchored to the current Swift file or applicable reference material.

Mitigation: Follow the hard gates: inventory files in scope, re-read cited regions, cross-check framework-specific claims against bundled references, and downgrade unsupported issues to questions.

Risk: The skill asks the agent to inspect Swift files selected by the user, which can include proprietary application code.

Mitigation: Review only intended files in an approved workspace and avoid including unrelated source in prompts or reports.

## Reference(s):

- [SwiftUI Animation Patterns](artifact/references/swiftui-animation-patterns.md)
- [Animation Performance](artifact/references/performance.md)
- [Animation Accessibility](artifact/references/accessibility.md)
- [Transition Review Patterns](artifact/references/transitions.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings with file and line headers, rationale, and code suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to be anchored to reviewed files and cross-checked against bundled reference notes when framework-specific.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
