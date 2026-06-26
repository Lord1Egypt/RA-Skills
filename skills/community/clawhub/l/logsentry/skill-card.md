## Description: <br>
Logging quality & observability analyzer -- detects missing structured logging, sensitive data in logs, inconsistent log levels, and log injection vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use LogSentry to scan codebases for logging quality issues, sensitive data exposure in logs, missing structured context, inconsistent levels, and log injection risks before committing or shipping code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A crafted license key can trigger local code execution during license handling. <br>
Mitigation: Install only if the publisher is trusted, avoid untrusted license keys, and prefer environment variables or locked-down configuration over CLI flags. <br>
Risk: Optional git hook installation modifies the repository and can persist scans on future commits or pushes. <br>
Mitigation: Enable hooks only as an explicit opt-in, review the lefthook configuration before installation, and remove hooks when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub LogSentry release page](https://clawhub.ai/suhteevah/logsentry) <br>
- [LogSentry homepage](https://logsentry.pages.dev) <br>
- [LogSentry hooks documentation](https://logsentry.pages.dev/docs/hooks) <br>
- [Lefthook project](https://github.com/evilmartians/lefthook) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, HTML, Shell commands, Configuration] <br>
**Output Format:** [Console text, JSON, self-contained HTML, and markdown-style reports with actionable findings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against files or directories; optional license keys unlock higher pattern tiers; optional lefthook integration can run scans on future commits or pushes.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
