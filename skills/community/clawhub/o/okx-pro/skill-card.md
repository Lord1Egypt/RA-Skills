## Description: <br>
OKX Pro provides OKX exchange trading guidance and shell examples for spot trading, futures, leverage, take-profit and stop-loss orders, and position management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[IceNoodle](https://clawhub.ai/user/IceNoodle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to configure OKX API credentials, inspect account and market data, and draft OKX V5 API calls for spot and futures trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading examples can affect live funds or close the wrong position if copied with the wrong side, amount, market, or account mode. <br>
Mitigation: Start in OKX demo trading, verify side and amount before execution, and require confirmation for large or position-closing orders. <br>
Risk: Signing and authentication examples may fail or produce rejected API requests if they drift from OKX V5 requirements. <br>
Mitigation: Review the signing helper against the OKX API documentation before using it with real API keys. <br>
Risk: API credentials with broad trading permissions increase the impact of mistakes or misuse. <br>
Mitigation: Use API keys with the narrowest trading permissions available and avoid unnecessary withdrawal or administrative permissions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/IceNoodle/okx-pro) <br>
- [OKX API Documentation](https://www.okx.com/docs-v5/) <br>
- [OKX Demo Trading](https://www.okx.com/market/trade/demo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, openssl, and user-provided OKX API credentials.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
