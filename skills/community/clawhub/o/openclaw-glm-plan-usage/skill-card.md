## Description: <br>
Query GLM coding plan usage statistics, including quota, model usage, and MCP tool usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OrientLuna](https://clawhub.ai/user/OrientLuna) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to check GLM Coding Plan quotas, 24-hour model usage, and 24-hour MCP tool usage from their local OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local OpenClaw configuration that contains the GLM API key. <br>
Mitigation: Protect ~/.openclaw/openclaw.json and avoid commands or logs that print full API keys. <br>
Risk: The release includes a shell script that performs local checks and remote usage queries. <br>
Mitigation: Review scripts/query-usage.sh before running it and install only from a trusted source. <br>
Risk: Installation guidance includes cleanup commands that remove skill directories. <br>
Mitigation: Verify rm -rf paths before cleanup so unrelated local files are not removed. <br>
Risk: Scheduled checks can repeatedly query usage data. <br>
Mitigation: Add a cron job only when scheduled local usage checks are intended. <br>


## Reference(s): <br>
- [GLM Coding Plan API Endpoints Reference](references/api-endpoints.md) <br>
- [Installation Guide](docs/INSTALLATION.md) <br>
- [OpenClaw Documentation](https://openclaw.dev) <br>
- [GLM Coding Plan](https://open.bigmodel.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Terminal text output and Markdown documentation with shell and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English output; reads local OpenClaw provider configuration and queries GLM monitoring endpoints with curl and jq.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
