## Description: <br>
Track crypto KOL and smart money wallets and get alerts when they buy or sell tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexbrc20](https://clawhub.ai/user/alexbrc20) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External crypto users and developers use this skill to inspect claimed KOL wallet activity, recent trades, and portfolio summaries. The bundled code displays preloaded wallets and simulated trade and portfolio output rather than verified live wallet data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may be mistaken for a real crypto intelligence tool even though the bundled code prints fixed simulated data. <br>
Mitigation: Treat outputs as demonstration data only and do not make trading or financial decisions from them unless the publisher supplies reviewed live wallet-monitoring code. <br>
Risk: The skill declares Telegram and Etherscan credentials despite lacking reviewed live integration behavior. <br>
Mitigation: Do not provide TELEGRAM_BOT_TOKEN or ETHERSCAN_API_KEY until the code is reviewed and the live data access scope is clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexbrc20/kol-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown instructions with shell-style command examples and console text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Declares python3 and curl requirements plus TELEGRAM_BOT_TOKEN and ETHERSCAN_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
