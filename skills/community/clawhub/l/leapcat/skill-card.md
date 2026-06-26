## Description: <br>
Trade stocks, subscribe to IPOs, manage wallet, complete KYC, and access real-time market data via AI agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raymondxu813-finance](https://clawhub.ai/user/raymondxu813-finance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill set to operate Leapcat financial account workflows, including market research, authentication, KYC, portfolio review, IPO subscriptions, stock trading, and wallet activity through the Leapcat CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real financial actions, including trades, IPO subscriptions or cancellations, and withdrawals. <br>
Mitigation: Require explicit user approval before each action and verify symbols, sides, order types, quantities, prices, project IDs, withdrawal addresses, fees, and deadlines before execution. <br>
Risk: KYC workflows can upload identity documents, submit personal information, and accept legal agreements. <br>
Mitigation: Use only files and personal details explicitly provided by the user for the current task, confirm legal-agreement acceptance with the user, and avoid retaining identity data beyond the session need. <br>
Risk: Authenticated workflows use a local token file that can preserve account access between sessions. <br>
Mitigation: Protect ~/.config/leapcat/tokens.json, avoid exposing token contents, and run the documented logout command when account access is no longer needed. <br>


## Reference(s): <br>
- [Leapcat homepage](https://leapcat.ai) <br>
- [Leapcat ClawHub release page](https://clawhub.ai/raymondxu813-finance/leapcat) <br>
- [Leapcat npm package](https://www.npmjs.com/package/leapcat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown instructions with version-pinned CLI commands and JSON response expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses npx leapcat@0.1.1; authenticated operations may create or use the local token file at ~/.config/leapcat/tokens.json.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and version-pinned artifact commands) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
