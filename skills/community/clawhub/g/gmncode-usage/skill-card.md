## Description: <br>
GMNCODE Usage helps an agent query GMNCODE / gmncode.cn usage data through HTTP APIs, including dashboard summaries, daily trends, per-model token usage, and cost data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alex-shen1121](https://clawhub.ai/user/alex-shen1121) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to retrieve GMNCODE account quota, dashboard usage summaries, date-range trends, and per-model token and cost breakdowns without manually opening the web dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses GMNCODE account credentials and caches an access token locally. <br>
Mitigation: Use a dedicated or limited-scope account where possible, avoid pasting passwords into chat, keep ~/.openclaw/.env and the token cache private, and rotate credentials or revoke tokens if the environment is shared or compromised. <br>
Risk: The skill depends on a third-party service and sends authenticated requests to GMNCODE APIs. <br>
Mitigation: Install and run it only if you trust the service and publisher, and review the configured account and requested date ranges before execution. <br>


## Reference(s): <br>
- [GMNCODE Usage API Reference](references/api.md) <br>
- [GMNCODE service](https://gmncode.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown summaries, compact tables, JSON output when requested, and shell commands for the bundled CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GMNCODE_EMAIL and GMNCODE_PASSWORD from environment variables or ~/.openclaw/.env; caches access tokens locally at ~/.cache/openclaw/gmncode-usage/token.json.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
