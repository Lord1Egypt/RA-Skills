## Description: <br>
Li Python Sec Check scans Python projects for security, privacy, data-security, dependency, and code-quality issues, with optional LLM analysis disabled by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to run local Python security checks, generate reports, and review remediation guidance before release or CI/CD integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads the target project and writes reports locally. <br>
Mitigation: Run it only against intended workspaces and review generated reports before relying on them. <br>
Risk: The included unsafe example application is intentionally vulnerable. <br>
Mitigation: Do not run examples/unsafe-example/app.py as a service or expose it on a network. <br>
Risk: Enabling LLM analysis can send code snippets or scan results to the configured API endpoint. <br>
Mitigation: Keep LLM analysis disabled for private code unless approved, and use environment variables or a secret manager for API credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-python-sec-check) <br>
- [Usage guide](docs/USAGE.md) <br>
- [Security and privacy statement](SECURITY_AND_PRIVACY.md) <br>
- [CloudBase Python standards](https://docs.cloudbase.net/run/develop/standards/python) <br>
- [Tencent Python security guide](https://github.com/Tencent/secguide/blob/main/Python%20%E5%AE%89%E5%85%A8%E6%8C%87%E5%8D%97.md) <br>
- [Bandit documentation](https://bandit.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, HTML, Guidance] <br>
**Output Format:** [Markdown reports, JSON reports, HTML security reports, and terminal summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports to a local reports directory; optional LLM analysis can add remediation guidance when explicitly enabled.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata, target metadata, frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
