## Description: <br>
Find markets where Simmer's AI consensus diverges from the real market price, then trade on the mispriced side using Kelly sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to scan Simmer and Polymarket markets for AI-versus-market divergence, review opportunities, and optionally execute constrained trades with Kelly sizing and safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money trades and lose funds. <br>
Mitigation: Run dry-run scans first, use a dedicated wallet with limited funds, and set low trade and daily budget limits before enabling live execution. <br>
Risk: Documented spending limits do not fully match the managed configuration. <br>
Mitigation: Check the runtime configuration before live use and set explicit limits with the actual environment variable names used by the skill. <br>
Risk: The skill requires sensitive credentials for Simmer access and, for external-wallet trading, wallet signing. <br>
Mitigation: Store credentials only in environment variables or a secrets manager, avoid sharing them in prompts or logs, and prefer a wallet that holds only the intended trading funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-ai-divergence) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text with optional JSON output and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can execute live trades only when run with live mode and the required credentials.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
