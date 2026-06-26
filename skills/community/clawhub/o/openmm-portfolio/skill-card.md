## Description: <br>
Balance tracking, order overview, and market data across exchanges using OpenMM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to inspect exchange balances, open orders, market prices, order books, trades, and Cardano token prices through OpenMM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a crypto exchange CLI and exchange account credentials. <br>
Mitigation: Install only when exchange account queries are intended, use read-only API keys where possible, disable withdrawals and trading scopes unless explicitly needed, and restrict keys by IP when supported. <br>
Risk: OpenMM may expose trading-related operations beyond portfolio inspection. <br>
Mitigation: Require explicit user confirmation before any order creation, cancellation, or trading strategy command. <br>
Risk: Exchange API keys are handled through environment variables. <br>
Mitigation: Keep credentials local to the runtime environment and avoid sharing command output or logs that could expose account data. <br>


## Reference(s): <br>
- [Exchange Data Reference](references/exchange-data.md) <br>
- [OpenMM Portfolio on ClawHub](https://clawhub.ai/adacapo21/openmm-portfolio) <br>
- [@3rd-eye-labs/openmm npm package](https://www.npmjs.com/package/@3rd-eye-labs/openmm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON output from OpenMM commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the OpenMM CLI and at least one configured exchange credential set.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
