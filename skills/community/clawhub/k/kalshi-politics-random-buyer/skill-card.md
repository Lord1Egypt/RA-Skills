## Description: <br>
Dry-run Kalshi skill that finds politics-related markets, picks a valid candidate at random, runs Simmer context checks, and proposes a trade plan without placing a real order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skybinjf](https://clawhub.ai/user/skybinjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-tool operators use this skill to create dry-run, manual-review trade plans for Kalshi politics markets. It can run on a managed schedule and requires a Simmer API key for market discovery, context checks, and sizing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is configured as a managed job that runs every 30 minutes while using a sensitive Simmer API key. <br>
Mitigation: Review before installing, keep the Simmer API key scoped and protected, and disable the cron or automaton configuration if only manual dry runs are intended. <br>
Risk: Generated logs and plans may expose bankroll, market-selection, and strategy details. <br>
Mitigation: Treat output as sensitive, limit log sharing, and review generated trade plans before any manual market action. <br>
Risk: The security verdict is suspicious because the instructions emphasize manual use while the configuration enables scheduled operation. <br>
Mitigation: Confirm the managed schedule is intentional and verify the simmer-sdk dependency before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skybinjf/kalshi-politics-random-buyer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with a pretty-printed JSON execution_plan object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The plan is marked manual_review_required and the script rejects live execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
