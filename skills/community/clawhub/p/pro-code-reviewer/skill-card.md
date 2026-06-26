## Description: <br>
Review code changes against platform-specific rules for Android and iOS plus shared general rules, supporting uncommitted changes, staged changes, specific commits, commit ranges, branch diffs, and optional styled HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timeaground](https://clawhub.ai/user/timeaground) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review repository changes before committing or merging. It focuses on production-impacting findings, with Android, iOS, general, quick, and security-focused review modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill inspects git diffs and nearby source code during review, which may expose proprietary or sensitive code to the active agent session. <br>
Mitigation: Use it only in trusted agent sessions and avoid reviewing sensitive changes unless that access is authorized. <br>
Risk: Optional HTML report generation creates local .code-reviews/ files inside the repository. <br>
Mitigation: Request HTML reports only when needed and add .code-reviews/ to .gitignore before committing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timeaground/pro-code-reviewer) <br>
- [README](README.md) <br>
- [General review rules](references/review-general.md) <br>
- [Android review rules](references/review-android.md) <br>
- [iOS review rules](references/review-ios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review findings by severity, with optional JSON-backed HTML reports when explicitly requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings include severity, file location, problem explanation, original code, and fix guidance; optional reports are written under .code-reviews/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
