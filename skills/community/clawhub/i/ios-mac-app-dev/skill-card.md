## Description:

Ios Mac App Dev helps agents guide full-lifecycle iOS and macOS app development, from requirements, PRDs, task breakdown, Swift TDD, code and UI guidance through localization, accessibility, performance, Apple Intelligence integration, and App Store release checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bbroot](https://clawhub.ai/user/bbroot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, implement, test, review, localize, optimize, and prepare iOS or macOS apps for release. It supports Swift, SwiftUI, UIKit, App Store readiness, Apple policy checklists, design quality checks, and architecture improvement workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may scan project files and suggest repository or issue-tracker changes.

Mitigation: Review proposed file, repository, and issue-tracker changes before applying them, and run helper scripts only on projects intended for review.

Risk: The policy monitor should be treated as a static checklist rather than current Apple policy verification.

Mitigation: Verify compliance-sensitive guidance against current Apple developer documentation before relying on it for release decisions.

Risk: Generated architecture HTML reports can load CDN scripts, which may expose report contents to external browser code.

Mitigation: Avoid opening generated reports with external CDN dependencies unless the report content can be shared with those external scripts, or remove those dependencies before viewing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bbroot/skills/ios-mac-app-dev)
- [Apple Developer News](https://developer.apple.com/news/)
- [Apple Developer News (China)](https://developer.apple.com/cn/news/)
- [Policy Compliance](references/00-policy-compliance.md)
- [Code Generation](references/01-code-generation.md)
- [UI Design System](references/02-ui-design.md)
- [Localization](references/03-localization.md)
- [Dark Mode](references/04-dark-mode.md)
- [Architecture Patterns](references/05-architecture.md)
- [Performance Optimization](references/06-performance.md)
- [Accessibility](references/07-accessibility.md)
- [Apple Intelligence Integration](references/08-ai-integration.md)
- [App Store Release Checklist](references/09-release-checklist.md)
- [Requirements Analysis](references/10-requirements-analysis.md)
- [PRD Generation](references/11-prd-generation.md)
- [Task Breakdown](references/12-task-breakdown.md)
- [Swift TDD](references/13-tdd-swift.md)
- [Bug Diagnosis](references/14-bug-diagnosis.md)
- [Architecture Improvement](references/15-architecture-improvement.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Swift or SwiftUI code snippets, shell commands, checklists, and optional helper-script reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper scripts may produce plain text or JSON reports and may scan local Swift project files when run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
