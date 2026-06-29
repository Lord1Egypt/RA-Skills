## Description: <br>
Monitors Polymarket World Cup winner odds, scans national-team markets, and alerts when odds move by more than 0.5%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External prediction-market traders and developers use this skill to monitor World Cup winner markets, compare odds against prior baselines, and receive Telegram alerts for short-term trading or arbitrage signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market alerts may be sent through Telegram, which shares alert content outside the local agent environment. <br>
Mitigation: Install only when Telegram delivery is acceptable, and configure bot tokens and chat IDs carefully. <br>
Risk: The skill depends on Polymarket API access and may require proxy use. <br>
Mitigation: Confirm API and proxy settings before running the skill, and review network access expectations with the deployment environment. <br>
Risk: The USDT subscription and contact flow are separate trust decisions about the third-party publisher. <br>
Mitigation: Evaluate the publisher profile and payment flow independently before purchasing or enabling paid access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/polymarket-worldcup-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration notes, and market-alert text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Alerts may be delivered through Telegram and depend on Polymarket API access, possibly through a proxy.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
