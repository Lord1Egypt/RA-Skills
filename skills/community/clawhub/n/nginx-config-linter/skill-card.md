## Description: <br>
Lint, validate, and audit nginx configuration files for syntax errors, security issues, and performance problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run local lint, security, performance, or full audits against nginx configuration files before deployment or in CI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The linter reads nginx configuration files or directories selected by the user, which may contain sensitive paths or operational details. <br>
Mitigation: Run it only on intended config paths and avoid broad recursive scans unless those files are appropriate for local inspection. <br>
Risk: `--strict` can fail CI when warnings are found. <br>
Mitigation: Use strict mode only when warning-level findings should block the pipeline. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/charlie-morrison/nginx-config-linter) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Status Summary](artifact/STATUS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, or Markdown lint reports with findings, severity, line numbers, and suggested fixes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports severity filtering, recursive directory scans, and strict exit behavior for CI.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
