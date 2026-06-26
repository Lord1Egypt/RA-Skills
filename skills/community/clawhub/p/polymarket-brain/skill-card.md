## Description: <br>
Automates geopolitical and macroeconomic news analysis, matches expert insights to Polymarket odds, and posts actionable trade recommendations to Discord. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimaschand29](https://clawhub.ai/user/dimaschand29) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to automate news-driven Polymarket research: fetch CNBC geopolitics and macroeconomic articles, route them through analyst logic, compare expert probabilities with monitored markets, and deliver Discord summaries. Outputs are decision-support analysis, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Embedded Discord webhook credentials can post to destinations the installer does not control. <br>
Mitigation: Remove and rotate embedded webhooks before use, and configure destination webhooks through secrets or environment variables. <br>
Risk: Market odds may be hardcoded or stale, which can make trading recommendations misleading. <br>
Mitigation: Verify whether odds are live before relying on output, and treat recommendations as decision-support analysis rather than financial advice. <br>
Risk: Local memory, snapshots, and workflow state can persist article history and posting configuration across restarts. <br>
Mitigation: Disable, clear, or review persisted files when retention is not desired, especially before copying the skill directory to another environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dimaschand29/polymarket-brain) <br>
- [Workflow reference](artifact/references/workflow.md) <br>
- [Configuration reference](artifact/references/config.md) <br>
- [Discord output format](artifact/references/discord-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown Discord messages, JSON analysis artifacts, Python code, shell commands, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Discord messages are sent one by one with rate limiting; the workflow may persist local output, memory, and snapshot files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
