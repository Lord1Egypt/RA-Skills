## Description: <br>
Provides a crypto paper-trading framework that guides an agent through multi-indicator technical analysis, regime filtering, position sizing, stop-loss management, trade journaling, and observation logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent builders use this skill to simulate crypto trading workflows, backtest trading logic, monitor paper portfolio performance, and capture lessons from simulated trades. It is intended for paper trading and strategy development, not direct real-money execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or update local paper-trading state and lesson files. <br>
Mitigation: Run it in a sandboxed or version-controlled workspace and review generated portfolio, journal, and observation files before relying on them. <br>
Risk: Trading analysis and simulated strategy guidance may be incorrect or misleading. <br>
Mitigation: Treat outputs as paper-trading or backtesting support, review results independently, and avoid using them as financial advice. <br>
Risk: The release evidence does not show credential use or real-money trading, but adding an implementation could change that risk profile. <br>
Mitigation: Keep the skill isolated from real exchange credentials and live trading APIs unless any added implementation is separately audited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/hft-paper-trader-pro) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional code snippets and local JSON or Markdown trading state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local paper-trading files such as portfolio.json, journal.json, and observations.md.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and SKILL.md frontmatter; artifact _meta.json lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
