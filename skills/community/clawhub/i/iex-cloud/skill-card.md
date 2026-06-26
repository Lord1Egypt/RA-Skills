## Description: <br>
Use this skill when a task needs IEX Cloud market data through the REST API (quotes, charts, fundamentals, market lists, and batch calls), including secure token handling and scriptable CLI usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to choose and execute IEX Cloud REST API requests for quotes, charts, fundamentals, market lists, and batch market-data pulls with token-handling guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production IEX tokens can be exposed or misused if stored in plaintext, hardcoded, or printed in logs. <br>
Mitigation: Use OpenClaw secrets or environment variables with scoped or sandbox tokens where possible, and do not hardcode or log full token values. <br>
Risk: Raw API paths can send production-token requests to unintended IEX endpoints. <br>
Mitigation: Review raw API paths before execution, keep paths relative, and use only trusted IEX API base URLs. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/oscraters/iex-cloud-skill) <br>
- [IEX Cloud API Reference](https://iexcloud.io/docs/api/) <br>
- [IEX API Status](https://status.iexapis.com/) <br>
- [OpenClaw secrets](https://docs.openclaw.ai/gateway/secrets) <br>
- [Local API reference summary](references/api_docs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an IEX_TOKEN credential and curl; jq is optional for formatting JSON responses.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
