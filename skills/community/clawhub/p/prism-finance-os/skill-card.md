## Description: <br>
PRISM OS SDK gives AI agents access to PRISM financial APIs for market data, prices, fundamentals, analytics, and finance workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StrykrAgent](https://clawhub.ai/user/StrykrAgent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to add PRISM financial data and analytics calls to AI finance agents, trading assistants, research tools, and portfolio workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SDK may expose trading, order, wallet, webhook, and API-key administration capabilities beyond the read-only positioning in the public skill text. <br>
Mitigation: Scope PRISM_API_KEY permissions narrowly and do not expose execution, wallet, webhook, or key-management methods to autonomous agents without explicit human approval gates, limits, and separate credentials. <br>
Risk: Financial API outputs may influence trading or portfolio decisions. <br>
Mitigation: Treat returned data and generated recommendations as decision support, verify material actions independently, and require review before any transaction or account-management action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/StrykrAgent/prism-finance-os) <br>
- [PRISM API Documentation](https://api.prismapi.ai/docs) <br>
- [PRISM API Homepage](https://api.prismapi.ai) <br>
- [npm Package](https://www.npmjs.com/package/prism-finance-os) <br>
- [Architecture and Build Roadmap](docs/ARCHITECTURE.md) <br>
- [Real API Coverage](docs/REAL_API_COVERAGE.md) <br>
- [Universal SDK Reference](docs/UNIVERSAL_SDK.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples and shell commands; SDK calls return JSON from the PRISM API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRISM_API_KEY for authenticated API access.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release metadata; package.json lists 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
