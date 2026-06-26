## Description: <br>
Security pre-flight for AI coding agents that plans libraries, audits CVEs, certifies dependencies, and produces an ex-post report in autonomous mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use VibeSafe before adding third-party dependencies so AI coding agents plan intended libraries, run vulnerability and maintenance checks, enforce a secrets policy, and produce audit certificates or risk reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may run local audit commands, public vulnerability lookups, and optional package installs such as pip-audit. <br>
Mitigation: Review commands before execution, approve package installs according to environment policy, and inspect linked scripts before running them. <br>
Risk: Generated audit certificates and reports can become stale as vulnerabilities and dependency versions change. <br>
Mitigation: Treat certificates as time-limited evidence and re-run audits before deployment, after dependency changes, or when new vulnerability information is published. <br>
Risk: Autonomous mode can defer checks until after coding, leaving issues to be reviewed after implementation. <br>
Mitigation: Review the generated risk report before production use and redesign dependencies when the report identifies blocking issues. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nerua1/nerua1-vibe-safe) <br>
- [OSV.dev API](https://api.osv.dev/v1/query) <br>
- [npm audit documentation](https://docs.npmjs.com/cli/v10/commands/npm-audit) <br>
- [pip-audit](https://pypi.org/project/pip-audit/) <br>
- [deps.dev API](https://api.deps.dev/v3alpha/packages/npm/${PKGNAME}) <br>
- [Snyk State of Open Source Security 2023](https://snyk.io/reports/open-source-security/) <br>
- [Socket.dev Open Source Security Research](https://socket.dev/research) <br>
- [CISA Known Exploited Vulnerabilities Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create stay_safe.md or risk-report.md when the agent follows the workflow.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
