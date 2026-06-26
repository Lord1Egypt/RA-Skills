## Description: <br>
Build a multi-bot arbitrage coordination framework with marketplace discovery, escrow protection, trust verification, cross-exchange opportunity detection, execution verification, profit splitting, MEV protection, and audit trails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-system builders use this skill as a guide for coordinating arbitrage bots across exchanges with trust checks, escrow workflows, execution verification, and audit trails. The examples are non-executable skill content but include code and API-call patterns that require careful review before use with funds or credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy-paste examples can affect funds, trading privacy, or execution signals if pointed at real systems. <br>
Mitigation: Run experiments only in sandbox or paper-trading environments, verify endpoints before running snippets, and require explicit human approval, limits, and compliance review before connecting wallets, exchange accounts, or funds. <br>
Risk: Signing-key handling and shared event-bus examples can expose sensitive credentials or trade details. <br>
Mitigation: Use isolated least-privilege signing keys, keep AGENT_SIGNING_KEY out of shared logs, and do not publish trade details or execution signals to shared infrastructure. <br>
Risk: The security summary notes that some safety claims conflict with the shown code. <br>
Mitigation: Review each snippet before use and treat the guide as advisory until the implementation is tested against the intended sandbox and compliance requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mirni/greenhelix-bot-arbitrage-framework) <br>
- [Publisher profile](https://clawhub.ai/user/mirni) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix API reference](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References AGENT_SIGNING_KEY for request signing examples.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
