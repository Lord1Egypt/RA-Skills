## Description: <br>
Discovers trending and newly listed tokens across supported blockchains using the LiberFi CLI, with filters for chain, time window, launchpad platform, keywords, and ranking fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan public token-market rankings, discover newly launched tokens, and prepare follow-up token research before any trading workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs an agent to install the LiberFi CLI globally from npm without asking first. <br>
Mitigation: Require explicit user approval before installing or retrying CLI installation, and prefer a user-verified local installation. <br>
Risk: Token rankings and newly listed token data can be mistaken for investment advice or a safety endorsement. <br>
Mitigation: Present rankings as informational only and recommend independent token security review before any follow-up trading or wallet action. <br>
Risk: Market-ranking workflows may lead users toward wallet credentials, signing, or transaction approval in adjacent skills. <br>
Mitigation: Do not request wallet credentials or approve transactions while using this market-ranking skill; route trading actions to separate workflows with explicit confirmation. <br>


## Reference(s): <br>
- [LiberFi homepage](https://liberfi.io) <br>
- [Liberfi Market ClawHub listing](https://clawhub.ai/bombmod/liberfi-market) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and tables with LiberFi CLI commands and JSON-backed results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market data; ranking output should include token name, symbol, price, and 24-hour change when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
