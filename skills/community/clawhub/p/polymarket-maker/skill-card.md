## Description: <br>
Continuous Static Market Making execution skill for Polymarket. Sells BOTH sides of 5-minute binary markets at $0.52. Features multi-asset support and an automated 8% Stop-Loss. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thony32](https://clawhub.ai/user/thony32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who intentionally operate Polymarket 5-minute crypto market-making use this skill to start a continuous trading loop and choose the initial asset and share allocation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an autonomous real-money Polymarket trading process. <br>
Mitigation: Use a dedicated low-balance wallet and keep LIVE_TRADING unset unless deliberately testing live orders. <br>
Risk: The suggested background process can continue running unattended. <br>
Mitigation: Define maximum runtime and exposure limits before launch, and know how to find and stop the node process. <br>
Risk: The security scan notes weak user controls and an overclaimed stop-loss. <br>
Mitigation: Monitor balances and open orders independently, and do not rely on the built-in stop-loss as the only loss control. <br>
Risk: Runtime dependencies and remote market APIs affect execution behavior. <br>
Mitigation: Inspect and pin dependencies before use, then run with the minimum wallet balance needed for the intended test. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thony32/polymarket-maker) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may start a long-running background Node.js trading process and write logs to bot_log.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
