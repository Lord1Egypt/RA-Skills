## Description: <br>
Agentic trading and market-data workflows for Futu OpenD (MooMoo/Futu OpenAPI), including OpenClaw-compatible secret-ref credential loading, account discovery, position queries, and simulated or live order placement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oscraters](https://clawhub.ai/user/oscraters) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-automation operators use this skill to query local OpenD market data, inspect accounts and positions, and place simulated or explicitly requested live MooMoo/Futu orders through structured CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel live brokerage orders and has limited built-in trading safeguards. <br>
Mitigation: Keep SIMULATE as the default and require a separate human approval process before enabling REAL trading. <br>
Risk: The skill handles MooMoo/Futu trading credentials. <br>
Mitigation: Prefer OpenClaw-managed secret refs and avoid keyring or local encrypted config storage on shared or hosted machines. <br>
Risk: OPEND_SDK_PATH can alter which Python SDK code is imported. <br>
Mitigation: Set OPEND_SDK_PATH only to trusted directories. <br>


## Reference(s): <br>
- [Futu OpenAPI Portal](https://www.futunn.com/OpenAPI) <br>
- [Futu OpenAPI Docs](https://openapi.futunn.com/futu-api-doc/en/) <br>
- [Get Market Snapshot API](https://openapi.futunn.com/futu-api-doc/en/quote/get-market-snapshot.html) <br>
- [Trade API Overview](https://openapi.futunn.com/futu-api-doc/en/trade/overview.html) <br>
- [OpenD Skill API References](references/api_docs.md) <br>
- [OpenD Registry Metadata](references/registry_metadata.md) <br>
- [OpenD Release Checklist](references/release_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or text emitted by CLI commands, with Markdown guidance and shell command examples for agent workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to structured JSON output and simulated trading unless live trading is explicitly selected.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
