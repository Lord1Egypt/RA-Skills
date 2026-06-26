## Description: <br>
Researches and analyzes cryptocurrency tokens on supported blockchains using the LiberFi CLI, including token search, token details, security checks, liquidity pools, holders, traders, and candlestick data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bombmod](https://clawhub.ai/user/bombmod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to research specific cryptocurrency tokens, compare on-chain market data, review security flags, inspect holder concentration, and summarize chart data before taking further action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global LiberFi CLI automatically and to retry npm installation against the public registry. <br>
Mitigation: Review or install the CLI manually with an explicit version before enabling the skill, and avoid unattended global installs in restricted environments. <br>
Risk: Token security checks and token-analysis outputs are informational and may not prove that a token is safe. <br>
Mitigation: Treat security findings as due-diligence inputs, verify high-risk flags independently, and avoid representing a clean result as a safety guarantee. <br>


## Reference(s): <br>
- [LiberFi homepage](https://liberfi.io) <br>
- [ClawHub skill page](https://clawhub.ai/bombmod/liberfi-token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with inline shell commands and JSON-backed token data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the LiberFi CLI with --json for structured command output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
