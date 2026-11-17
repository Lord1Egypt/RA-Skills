## Description:

CodeQL security scanning and LLM-assisted analysis tool that checks CodeQL availability, scans a target directory, generates vulnerability reports, supports LLM analysis, integrates with Jenkins, and outputs validation checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run CodeQL scans on authorized projects, review SARIF and Markdown findings, prioritize vulnerabilities with optional LLM assistance, and generate validation checklists. CI maintainers can use its Jenkins guidance to add security scanning to build workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can process source code, SARIF, vulnerability reports, and CI configuration that may contain sensitive project or security details.

Mitigation: Run it only on authorized code, keep reports in restricted locations, exclude sensitive directories, and avoid publishing SARIF or Markdown scan outputs.

Risk: LLM analysis and Jenkins workflows may move scan results outside the local environment despite local-only privacy claims.

Mitigation: Disable automatic LLM analysis unless approved, review what data is sent, use non-production Jenkins targets first, and keep CSRF protections enabled.

Risk: Example Jenkins credentials or tokens could be copied into real deployments.

Mitigation: Replace all sample credentials, use scoped secrets, and rotate any token that may have been exposed or reused.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-codeql-llm)
- [CodeQL CLI Binaries](https://github.com/github/codeql-cli-binaries)
- [CodeQL Documentation](https://codeql.github.com/docs/)
- [CodeQL Queries](https://github.com/github/codeql)
- [SARIF Format Reference](https://sarifweb.azurewebsites.net/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, SARIF scan output, Markdown reports, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the CodeQL CLI; outputs may include sensitive vulnerability details and should be stored with restricted access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
