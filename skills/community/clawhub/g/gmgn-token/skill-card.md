## Description: <br>
Researches crypto or meme tokens by address using GMGN API data for price, liquidity, holders, traders, smart-money and KOL exposure, and security signals across Solana, BSC, Base, and Ethereum. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmgnai](https://clawhub.ai/user/gmgnai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, traders, and crypto researchers use this skill to run GMGN CLI token lookups and summarize due diligence before evaluating or trading a token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a GMGN API key in ~/.config/gmgn/.env. <br>
Mitigation: Treat the API key as a secret, keep the file private, and install the skill only when GMGN API access through gmgn-cli is intended. <br>
Risk: Token, wallet, holder, and trader outputs can expose sensitive or account-linked trading information. <br>
Mitigation: Avoid sharing raw wallet or account outputs publicly and review summaries before redistribution. <br>
Risk: The skill includes network troubleshooting commands for documented 401 or 403 connectivity issues. <br>
Mitigation: Run IPv6 troubleshooting only when debugging the documented GMGN CLI connectivity issue. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gmgnai/gmgn-token) <br>
- [GMGN API key setup](https://gmgn.ai/ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with gmgn-cli shell commands, summary cards, ranked tables, and optional raw JSON from the CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gmgn-cli and a locally configured GMGN_API_KEY. Token holder and trader outputs may include wallet-level data.] <br>

## Skill Version(s): <br>
1.4.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
