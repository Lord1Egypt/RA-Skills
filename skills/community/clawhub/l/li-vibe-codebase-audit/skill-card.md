## Description:

Provides automated and AI-assisted security audits for AI-generated codebases, including checks for vulnerabilities, secrets, dependency risks, and configuration issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to audit AI-generated projects before publication, CI/CD promotion, or deployment. It can run local pattern scans and optional provider-backed AI review to produce findings, risk levels, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote or multi-provider audit modes may send project code to external AI providers.

Mitigation: Use local scanning for private repositories unless the user has reviewed and accepted what data will be sent.

Risk: The Ollama setup example uses a curl-to-shell installation command.

Mitigation: Review the installer source and prefer a trusted package manager or manual installation path before execution.

Risk: Enhanced caching stores scan results with pickle and may load cached files from the project cache directory.

Mitigation: Disable enhanced caching or run on trusted, narrow project paths until the cache format is replaced or otherwise secured.

Risk: Server security guidance reports a fail-open SAFE summary issue in the enhanced auditor.

Mitigation: Treat SAFE results from the enhanced auditor as advisory and verify with local findings or a second review before publication decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-vibe-codebase-audit)
- [Skill Documentation](artifact/SKILL.md)
- [English Usage Guide](artifact/README_en.md)
- [Tool Schema](artifact/tool_schema_v2.json)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON, Markdown, console text, or HTML reports with findings, risk scores, recommendations, and example commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured findings, severity counts, dependency and configuration scan summaries, model consensus results, and fix suggestions.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
