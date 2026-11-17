## Description:

Provides iOS-focused self-checks and rule proposals for Swift, Objective-C, UIKit, SwiftUI, App Store compliance, crash prevention, and Xcode workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelee09](https://clawhub.ai/user/joelee09)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to review iOS development answers and code for platform-specific risks, style issues, compatibility concerns, privacy configuration gaps, and App Store review considerations. It can also propose iOS rule drafts through its required developer-self-improve-core dependency for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The propose command runs the developer-self-improve-core shell script, so the effective behavior depends on that dependency.

Mitigation: Review and trust developer-self-improve-core before installation, and prefer a pinned or otherwise verified dependency version.

Risk: Security documentation describes the skill as read-only and no-code-execution, but that claim is incomplete for workflows that call the dependency script.

Mitigation: Treat rule-proposal workflows as dependency-executing workflows and review generated rule drafts before accepting any changes.

## Reference(s):

- [README](artifact/README.md)
- [Security Information](artifact/SECURITY.md)
- [Trust Model](artifact/TRUST_MODEL.md)
- [Dependency Explanation](artifact/DEPENDENCY_EXPLANATION.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and rule drafts require human review.]

## Skill Version(s):

1.1.0 (source: server release and SKILL.md frontmatter; .clawhub.json and SUBMISSION_NOTE.md still mention 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
