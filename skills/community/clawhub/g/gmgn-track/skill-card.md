## Description: <br>
Gets real-time crypto buy/sell activity from Smart Money wallets, KOL influencer wallets, and personally followed wallets through the GMGN API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gmgnai](https://clawhub.ai/user/gmgnai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query GMGN tracking feeds for followed-token lists, followed-wallet trades, KOL trades, and smart-money activity across Solana, BSC, Base, and Ethereum, then summarize cluster signals and trading context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires local GMGN credentials and may store a GMGN signing private key for followed-wallet queries. <br>
Mitigation: Keep ~/.config/gmgn/.env private, restrict file permissions, and rotate the GMGN key if the machine is shared or compromised. <br>
Risk: Follow-wallet output can reveal the user's GMGN followed-wallet list. <br>
Mitigation: Avoid sharing follow-wallet results in public channels; prefer KOL or smart-money feeds when public sharing is needed. <br>
Risk: The workflow depends on the separately installed gmgn-cli package. <br>
Mitigation: Review npm package trust and installation source before use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/gmgnai/gmgn-track) <br>
- [GMGN API key setup](https://gmgn.ai/ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown trade summaries with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include summarized GMGN trade feed results, convergence-signal analysis, retry timing for rate limits, and credential setup steps.] <br>

## Skill Version(s): <br>
1.4.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
