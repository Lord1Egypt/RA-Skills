## Description: <br>
Helps agents support the full iOS/macOS app lifecycle, including requirements analysis, PRDs, task breakdown, Swift TDD, Swift/SwiftUI/UIKit guidance, UI design, localization, accessibility, performance, Apple Intelligence integration, compliance checks, and App Store release readiness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bbroot](https://clawhub.ai/user/bbroot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan, build, test, improve, and prepare iOS/macOS applications for release. It supports requirements clarification, PRD and task creation, Swift implementation guidance, quality checks, policy review, and App Store readiness work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some workflows can lead the agent to scan repositories, write files, generate reports, or publish to an Issue Tracker. <br>
Mitigation: Keep agent confirmations enabled for repository scans, file writes, generated reports, and Issue Tracker publishing, and review changes before applying them. <br>
Risk: Apple policy guidance may become stale because the included policy monitor is a static helper rather than an authoritative live policy source. <br>
Mitigation: Verify Apple-policy guidance against current Apple Developer documentation before relying on it for release or compliance decisions. <br>


## Reference(s): <br>
- [Policy Compliance and Dynamic Learning](references/00-policy-compliance.md) <br>
- [Code Generation](references/01-code-generation.md) <br>
- [UI Design System](references/02-ui-design.md) <br>
- [Localization and Internationalization](references/03-localization.md) <br>
- [Dark Mode Adaptation](references/04-dark-mode.md) <br>
- [Architecture Patterns](references/05-architecture.md) <br>
- [Performance Optimization](references/06-performance.md) <br>
- [Accessibility Support](references/07-accessibility.md) <br>
- [Apple Intelligence Integration](references/08-ai-integration.md) <br>
- [App Store Release Checklist](references/09-release-checklist.md) <br>
- [Requirements Analysis Workflow](references/10-requirements-analysis.md) <br>
- [PRD Generation Workflow](references/11-prd-generation.md) <br>
- [Task Breakdown Workflow](references/12-task-breakdown.md) <br>
- [Swift TDD Workflow](references/13-tdd-swift.md) <br>
- [Bug Diagnosis Workflow](references/14-bug-diagnosis.md) <br>
- [Architecture Improvement Workflow](references/15-architecture-improvement.md) <br>
- [Apple Developer News](https://developer.apple.com/news/) <br>
- [Apple Developer News China](https://developer.apple.com/cn/news/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Swift snippets, shell commands, checklists, and optional JSON or report output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose repository scans, file writes, generated reports, and Issue Tracker publishing when the host agent and user allow those actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
