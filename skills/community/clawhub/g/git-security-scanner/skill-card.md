## Description: <br>
Unified security scanner that helps agents run gitleaks and shipguard scans for leaked secrets, credentials, and code vulnerabilities before changes reach a remote repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[celstnblacc](https://clawhub.ai/user/celstnblacc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and repository maintainers use this skill to ask an agent to scan working trees, staged changes, or full git history for secrets and common static-analysis findings. It also helps configure optional pre-commit checks and generate terminal, Markdown, JSON, or SARIF reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scan output and saved reports may contain real secrets, credentials, or sensitive vulnerability details. <br>
Mitigation: Treat terminal output and report files as confidential, restrict where reports are stored or shared, and rotate any exposed credentials before re-scanning. <br>
Risk: The skill depends on external scanning tools and a shell command wrapper. <br>
Mitigation: Install gitleaks and shipguard from trusted sources, keep them updated, and review generated commands before execution in sensitive repositories. <br>
Risk: The optional pre-commit hook can block commits when high-severity findings are detected. <br>
Mitigation: Enable the hook only in repositories where blocking high-severity findings is intended, and document the severity threshold for contributors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/celstnblacc/git-security-scanner) <br>
- [Publisher Profile](https://clawhub.ai/user/celstnblacc) <br>
- [Publisher Homepage](https://github.com/celstnblacc) <br>
- [gitleaks](https://github.com/gitleaks/gitleaks) <br>
- [gitleaks Releases](https://github.com/gitleaks/gitleaks/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and scan report formats including terminal text, Markdown, JSON, and SARIF.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or save sensitive scan reports that contain real secrets or vulnerability details; handle generated reports as confidential.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
