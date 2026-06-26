## Description: <br>
Pre-flight environment validator — checks that all required binaries, environment variables, and services are available before running other skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guifav](https://clawhub.ai/user/guifav) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to check required local binaries, environment variables, and optional service connectivity before running stack-specific automation. It reports what is ready, what is blocked, and concrete fixes for missing prerequisites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential validation can expose or save cloud token and private-key values in command output or preflight-report.json. <br>
Mitigation: Replace value-printing checks with set/unset tests, redact all report details, avoid production tokens when testing, and delete preflight-report.json after use. <br>
Risk: Optional connectivity checks contact external cloud services using local credentials. <br>
Mitigation: Require explicit user approval before network connectivity checks and run them only in an intended project or sandbox environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guifav/preflight-check) <br>
- [Publisher profile](https://clawhub.ai/user/guifav) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON diagnostic report and human-readable Markdown summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write preflight-report.json with check results and recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
