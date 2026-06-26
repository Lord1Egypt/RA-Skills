## Description: <br>
Reviews iOS animation code for correctness, performance, accessibility, and Apple API best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code reviewers use this skill to review SwiftUI, UIKit, and Core Animation code for animation correctness, performance, accessibility, and Apple API best practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review output may include stale or weakly anchored animation findings if code locations or framework-specific claims are not rechecked. <br>
Mitigation: Use the documented hard gates: inventory animation APIs, re-anchor each FILE:LINE citation, and cross-check framework-specific claims against the bundled references before reporting. <br>
Risk: Security evidence advises caution before using ClawHub workflows with real credentials or mutating commands. <br>
Mitigation: Review the relevant auth, publishing, telemetry, moderation, and production-deploy documentation before providing real credentials or running mutating commands. <br>


## Reference(s): <br>
- [Animation Accessibility](references/accessibility.md) <br>
- [Animation Performance](references/performance.md) <br>
- [SwiftUI Animation Patterns](references/swiftui-animation-patterns.md) <br>
- [Transition Review Patterns](references/transitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown review findings with file and line anchors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are expected to include concise rationale, code suggestions, and reference-backed review details.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
