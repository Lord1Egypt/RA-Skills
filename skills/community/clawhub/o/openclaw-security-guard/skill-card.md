## Description: <br>
Security audit CLI + live dashboard for OpenClaw. Scans for secrets, config issues, prompt injections, vulnerable dependencies, and unverified MCP servers. Zero telemetry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miloudbelarebia](https://clawhub.ai/user/miloudbelarebia) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to audit OpenClaw installations for exposed secrets, unsafe configuration, prompt-injection patterns, vulnerable dependencies, and unverified MCP servers. It can also provide hardening guidance, report generation, dashboard monitoring, and optional local fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool can read OpenClaw or workspace files and may modify OpenClaw configuration or Git hooks when fix commands are used. <br>
Mitigation: Run audit and dry-run modes first, keep backups enabled, and manually review diffs before accepting changes. <br>
Risk: The dashboard uses third-party CDN scripts even though the release claims zero network activity. <br>
Mitigation: Use the dashboard only where loading those external scripts is acceptable, or rely on CLI audit/report workflows in restricted environments. <br>
Risk: The bundled dependency scanner should not be treated as a complete CVE audit. <br>
Mitigation: Run npm audit or an approved software composition analysis tool before relying on dependency risk results. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/miloudbelarebia/openclaw-security-guard) <br>
- [Publisher profile](https://clawhub.ai/user/miloudbelarebia) <br>
- [Project homepage](https://github.com/2pidata/openclaw-security-guard) <br>
- [npm package](https://www.npmjs.com/package/openclaw-security-guard) <br>
- [CLI reference](docs/api/cli.md) <br>
- [Programmatic API reference](docs/api/programmatic.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal output with optional JSON, HTML, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read local OpenClaw and workspace files; fix modes can modify local configuration or Git hooks when explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
