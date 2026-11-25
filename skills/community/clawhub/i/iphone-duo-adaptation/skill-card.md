## Description:

Helps iOS developers audit, implement, and verify iPhone Duo layouts across SwiftUI, UIKit, and mixed interfaces, including fold transitions and localization or accessibility regressions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzw-object](https://clawhub.ai/user/hzw-object)

### License/Terms of Use:

MIT-0

## Use Case:

iOS developers and QA engineers use the skill to inspect and adapt apps for iPhone Duo's inner and outer displays, folding and resizing, navigation, reserved regions, localization, and accessibility. It provides implementation guidance, code examples, and project-specific verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A benign scan result does not guarantee zero risk in every project or runtime environment.

Mitigation: Review the guidance against the target app, use availability checks and fallbacks for newer APIs, and verify fold behavior on the intended runtime.

## Reference(s):

- [Source repository](https://github.com/hzw-object/iphone-duo-adaptation)
- [ClawHub release page](https://clawhub.ai/hzw-object/skills/iphone-duo-adaptation)
- [English engineering and QA handbook](references/guide.en.md)
- [Engineering examples](references/engineering.md)
- [Apple source index](references/sources.md)
- [Apple iPhone Duo preparation guide](https://developer.apple.com/iphone-duo/prepare/)
- [Apple reserved-region geometry API for SwiftUI](https://developer.apple.com/documentation/swiftui/geometryproxy/reservedregions(kind:options:layoutdirectionbehavior:))
- [Apple reserved-region API for UIKit](https://developer.apple.com/documentation/uikit/uiview/reservedregions(kind:options:))
- [Apple string catalogs and localization](https://developer.apple.com/documentation/xcode/localizing-and-varying-text-with-a-string-catalog)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance and reports with Swift examples, configuration advice, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
