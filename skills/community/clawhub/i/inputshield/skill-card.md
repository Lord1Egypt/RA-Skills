## Description: <br>
Input validation and sanitization scanner that catches missing validation, unsafe deserialization, ReDoS, path traversal, command injection, and XSS patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suhteevah](https://clawhub.ai/user/suhteevah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use InputShield to scan local codebases for input validation, sanitization, deserialization, ReDoS, path traversal, command injection, and XSS risks before commit, CI, or security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads local project files and may print matched code snippets in scan results. <br>
Mitigation: Run scans only in repositories where local code inspection is acceptable, and review generated reports before sharing them outside the project team. <br>
Risk: Installing hooks changes repository behavior and can block commits or pushes. <br>
Mitigation: Inspect the bundled lefthook configuration before installation, keep a backup, and use the uninstall command when the hook should no longer apply. <br>
Risk: Passing license keys directly on command lines can expose them through shell history or process listings. <br>
Mitigation: Prefer the documented environment variable or OpenClaw configuration path for `INPUTSHIELD_LICENSE_KEY` instead of inline command arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suhteevah/inputshield) <br>
- [Publisher profile](https://clawhub.ai/user/suhteevah) <br>
- [InputShield website](https://inputshield.pages.dev) <br>
- [InputShield pricing](https://inputshield.pages.dev/#pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, markdown reports, JSON or HTML reports, and setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local scan output can include file paths, line numbers, check IDs, severities, scores, matched snippets, and remediation recommendations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
