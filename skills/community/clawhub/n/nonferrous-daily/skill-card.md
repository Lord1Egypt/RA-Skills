## Description: <br>
Daily non-ferrous metals briefing for AI agents that collects public market prices, news, inventory signals, futures structure, and sentiment for Cu, Zn, Ni, Co, Mg, and Bi, then produces a concise trading-style report that can be delivered through Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ramboxie](https://clawhub.ai/user/ramboxie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-monitoring agents use this skill to collect public non-ferrous metals data and generate a daily report with prices, trend signals, risk triggers, and execution-oriented commentary. It is intended as a research briefing workflow and not as a substitute for independent financial judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot credentials are required for live delivery and could expose the configured channel if mishandled. <br>
Mitigation: Use a dedicated bot and channel, keep tokens out of commits and logs, and test delivery with DRY_RUN before live sends. <br>
Risk: Market data and generated trend signals may be delayed, missing, revised, or unsuitable for financial decisions. <br>
Mitigation: Independently verify market data and treat reports as research briefings rather than investment advice. <br>
Risk: Running an unpinned clone could execute code that differs from the reviewed release. <br>
Mitigation: Pin the reviewed package, release, or commit before deployment. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Analysis Daily Template](references/ANALYSIS_DAILY_TEMPLATE.md) <br>
- [Analysis Playbook](references/ANALYSIS_PLAYBOOK.md) <br>
- [ClawHub skill page](https://clawhub.ai/ramboxie/nonferrous-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown report, with JSON data collection output and shell commands for setup or scheduled execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send generated report contents to a configured Telegram chat when credentials are provided.] <br>

## Skill Version(s): <br>
1.3.7 (source: package.json, server release evidence, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
