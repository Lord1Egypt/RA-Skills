## Description: <br>
CodeQL security scanning and LLM-assisted analysis tool that checks CodeQL availability, scans target directories, generates vulnerability reports, supports LLM analysis, integrates with Jenkins, and outputs validation checklists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security engineers, and DevOps teams use this skill to run CodeQL scans on authorized codebases, summarize findings, generate Markdown and SARIF outputs, and prepare remediation or validation checklists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes Jenkins administration paths and credential examples that could affect CI systems if copied directly. <br>
Mitigation: Run only against Jenkins instances you control, keep Script Console access out of automation accounts, and replace or rotate any copied credentials or similar tokens. <br>
Risk: LLM analysis or Jenkins upload can move SARIF, file paths, vulnerability details, and code-derived snippets outside the local machine. <br>
Mitigation: Keep LLM analysis and uploads disabled unless that data sharing is approved, and review or redact scan outputs before sending them to external services. <br>
Risk: Exploit-style validation output may be misused or expose sensitive vulnerability details. <br>
Mitigation: Use the generated validation checklists only for authorized systems and store reports in restricted locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-codeql-llm) <br>
- [Publisher profile](https://clawhub.ai/user/43622283) <br>
- [CodeQL CLI binaries](https://github.com/github/codeql-cli-binaries) <br>
- [CodeQL documentation](https://codeql.github.com/docs/) <br>
- [CodeQL queries](https://github.com/github/codeql) <br>
- [SARIF format reference](https://sarifweb.azurewebsites.net/) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, generated reports, SARIF files, and validation checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local scan artifacts such as CODEQL_SECURITY_REPORT.md, vulnerability checklists, CodeQL databases, and SARIF results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
