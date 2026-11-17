## Description:

A mobile development toolkit covering Flutter, React Native, SwiftUI, mobile design, performance, release, device QA, and permission and dependency checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT

## Use Case:

Independent developers and small teams use this skill to choose and build mobile apps with Flutter, React Native, or SwiftUI, and to plan performance, release, and device QA work. It also provides permission and dependency checks with reusable configuration templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Profiling and hosted testing can expose test data or heap dumps.

Mitigation: Use test accounts, protect heap dumps, and delete them when no longer needed.

Risk: Permission templates and telemetry settings may not match an app's actual features or data practices.

Mitigation: Tailor permission declarations to the features in use and review telemetry before enabling monitoring.

Risk: Packages downloaded after the bundled files were reviewed are outside this security review.

Mitigation: Use reviewed, pinned versions where practical and review downloaded packages before use.

## Reference(s):

- [Cross-platform decision guide](references/decision-cross-platform.md)
- [Mobile performance and battery guide](references/mobile-performance.md)
- [Mobile release guide](references/mobile-release.md)
- [Mobile device QA guide](references/mobile-qa-devices.md)
- [Flutter architecture reference](https://skills.sh/flutter/skills/flutter-apply-architecture-best-practices)
- [React Native components reference](https://skills.sh/google-labs-code/stitch-skills/stitch::react-components)
- [SwiftUI layout reference](https://skills.sh/dpearson2699/swift-ios-skills/swiftui-layout-components)
- [Mobile design reference](https://skills.sh/sickn33/antigravity-awesome-skills/mobile-design)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with code examples and shell commands; reusable JSON, XML, and plist templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content varies with the mobile task and selected platform.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
