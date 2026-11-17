## Description:

Python security standards checking skill based on CloudBase standards and Tencent security guidance, with optional LLM analysis disabled by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to scan Python projects for security, privacy, dependency, and code-quality issues and to generate review reports for local development or CI/CD workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional LLM analysis can transmit code snippets and scan results to a configured external endpoint.

Mitigation: Use the default local scanning mode for sensitive code, and enable LLM analysis only with a trusted endpoint and appropriate API token.

Risk: The included unsafe Flask example contains intentionally vulnerable code for testing scanner behavior.

Mitigation: Run the unsafe example only in an isolated test environment and do not deploy it as an application.

Risk: Security scan results can include false positives or incomplete findings.

Mitigation: Review generated findings before making code changes or using results for release decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-python-sec-check)
- [README](artifact/README.md)
- [Usage guide](artifact/docs/USAGE.md)
- [Security and privacy statement](artifact/SECURITY_AND_PRIVACY.md)
- [CloudBase Python development standards](https://docs.cloudbase.net/run/develop/standards/python)
- [Tencent security guide](https://github.com/Tencent/secguide)
- [Bandit documentation](https://bandit.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, optional HTML and JSON tool reports, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default local scanning can produce Markdown reports; optional Bandit and pip-audit integrations can produce HTML and JSON reports.]

## Skill Version(s):

0.0.2 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
