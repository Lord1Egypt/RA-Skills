## Description: <br>
Security Check helps agents assess GitHub repositories, npm packages, PyPI libraries, and remote shell scripts before installation by surfacing advisory risk labels and recommended next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gawezepobi09-debug](https://clawhub.ai/user/gawezepobi09-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before cloning repositories, installing npm or PyPI packages, or executing remote shell scripts so an agent can summarize trust signals, known vulnerabilities, and whether user confirmation is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Risk labels are advisory and can be incomplete or outdated. <br>
Mitigation: Treat summaries as decision support, review flagged packages manually, and confirm important findings against authoritative vulnerability sources before installing. <br>
Risk: Checking private dependencies against external vulnerability services can disclose package names or dependency details. <br>
Mitigation: Avoid sending private dependency details to external services unless that disclosure is acceptable for the project. <br>
Risk: Remote scripts and package installs can execute untrusted code. <br>
Mitigation: Require explicit user confirmation before installing packages or running remote scripts, especially when the skill marks an item for review or as dangerous. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gawezepobi09-debug/pre-install-security-check) <br>
- [Skantek approach](references/skantek-approach.md) <br>
- [Vulnerability databases](references/vulnerability-databases.md) <br>
- [Snyk vulnerability database](https://security.snyk.io) <br>
- [GitHub Advisory Database](https://github.com/advisories) <br>
- [Safety DB](https://github.com/pyupio/safety-db) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Shell commands] <br>
**Output Format:** [Markdown with concise risk summaries and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports advisory safe, review, or dangerous labels and may recommend confirmation or safer package versions before proceeding.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
