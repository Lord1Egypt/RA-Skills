## Description: <br>
MoltRock provides commands for AI agents to interact with an autonomous on-chain hedge fund concept, including USDC contribution flows, vault-share status, governance actions, progress reporting, and MROCK token verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sloof13](https://clawhub.ai/user/Sloof13) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
AI agents and their operators use this skill to inspect MoltRock status, generate governance or promotional text, verify token addresses, and prepare contribution-style API calls for Base or Solana workflows. Because the skill concerns funds and token activity, users should independently verify contracts, endpoints, fees, and transaction details before allowing execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill asks agents to make contribution-style financial API calls before contract and endpoint trust details are adequately scoped. <br>
Mitigation: Do not allow an agent to contribute USDC, approve wallet spending, or submit transactions until the deployed vault contract, backend API, fees, project provenance, and exact transaction details have been independently verified. <br>
Risk: The artifact describes two assets named MROCK and identifies the vault share address as not yet deployed, creating token-confusion and scam risk. <br>
Mitigation: Use the skill's verification command and independent chain explorers before acting; treat any non-matching MROCK address as untrusted and do not treat the pump.fun token as vault ownership, voting power, or yield. <br>


## Reference(s): <br>
- [ClawHub MoltRock page](https://clawhub.ai/Sloof13/moltrock) <br>
- [Official pump.fun MROCK hype token](https://pump.fun/coin/7GWc8fiF7jYkigboNCoHuZPwAhk7zqmht2EWFDCipump) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Terminal text with optional JSON API responses and generated social-post text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command behavior depends on local shell tools, the MOLTROCK_API_URL environment variable, wallet addresses, chain selection, and external service availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
