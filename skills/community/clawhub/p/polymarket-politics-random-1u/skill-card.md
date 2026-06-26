## Description: <br>
Build and run a Polymarket politics-market trading skill with the AION SDK that searches active political markets on Polymarket, randomly chooses one market, and places a 1 USD trade through Aionmarket when live execution is enabled. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as an AION SDK template for searching active Polymarket politics markets, selecting one candidate at random, and preparing a 1 USD YES or NO trade. It defaults to dry-run mode and requires explicit live execution before submitting a real-money trade. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place repeated real-money random trades if live mode is enabled, especially when scheduled automation is active. <br>
Mitigation: Keep dry-run mode enabled by default, avoid setting RUN_LIVE in scheduled environments, disable the cron unless automation is intentional, and set strict spending limits before live runs. <br>
Risk: The skill requires sensitive AION and optional wallet credentials for live trading. <br>
Mitigation: Use tightly controlled credentials and never write API keys or private keys into repository files. <br>
Risk: Random market selection is not a production trading strategy. <br>
Mitigation: Review market context warnings, customize the market filter and risk checks, and require operator approval before live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fivegive249-ship-it/polymarket-politics-random-1u) <br>
- [Publisher profile](https://clawhub.ai/user/fivegive249-ship-it) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, API calls, JSON-like run summaries] <br>
**Output Format:** [Markdown instructions and Python script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AION_API_KEY for market reads and trade execution; optional live trading uses wallet-related environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
