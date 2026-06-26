## Description: <br>
iOS self-improvement skill for Swift and Objective-C standards, App Store review readiness, crash prevention, automated self-checks, Xcode, UIKit, and SwiftUI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joelee09](https://clawhub.ai/user/joelee09) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to review iOS code and guidance for platform-specific risks such as crash patterns, privacy permission text, navigation behavior, AutoLayout, SwiftUI lifecycle issues, concurrency, sandboxing, and App Store review concerns. It also helps generate user-reviewed iOS rule proposals through its declared developer-self-improve-core dependency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on developer-self-improve-core for rule generation. <br>
Mitigation: Review that dependency before installation and confirm it is acceptable for the intended workspace. <br>
Risk: Generated rule proposals or self-check findings could be inaccurate or too broad for a specific iOS project. <br>
Mitigation: Keep the documented human-review step in place before accepting any proposed rule or memory change. <br>
Risk: The iOS checks are only appropriate when the workspace is configured for iOS or multi-platform iOS work. <br>
Mitigation: Confirm the platform configuration before relying on the skill's self-check output. <br>


## Reference(s): <br>
- [README](artifact/README.md) <br>
- [Security Information](artifact/SECURITY.md) <br>
- [Trust Model](artifact/TRUST_MODEL.md) <br>
- [Dependency Explanation](artifact/DEPENDENCY_EXPLANATION.md) <br>
- [Built-in iOS Rules](artifact/rules/builtin_rules.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/joelee09/ios-self-improve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with inline code, shell command examples, configuration notes, and rule-draft snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for user review before any rule or memory change is accepted.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
