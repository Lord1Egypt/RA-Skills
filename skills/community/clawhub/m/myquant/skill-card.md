## Description:

MyQuant is a Python SDK guide for the GoldMiner event-driven quantitative platform, covering market data, backtesting, simulated trading, and live trading for A-shares, futures, options, ETFs, and convertible bonds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coderwpf](https://clawhub.ai/user/coderwpf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill to build, test, and operate MyQuant strategies that access market data, run backtests, and interact with simulated or live brokerage workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live brokerage orders and bulk portfolio changes.

Mitigation: Start in backtest or paper/simulation mode and require explicit human confirmation before live orders, rebalances, margin operations, cancel-all, or close-all actions.

Risk: GM_TOKEN credentials may be exposed if copied into source files or chat transcripts.

Mitigation: Keep GM_TOKEN in a protected environment variable or secret store and avoid placing it in source code, logs, or prompts.

Risk: Unpinned dependencies may change behavior before connecting to live credentials.

Mitigation: Pin and review dependency versions in a dedicated low-privilege environment before any authenticated or live trading workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/coderwpf/skills/myquant)
- [MyQuant homepage](https://www.myquant.cn)
- [MyQuant Python documentation](https://www.myquant.cn/docs/python/41)
- [MyQuant downloads](https://www.myquant.cn/docs/downloads/698)
- [MyQuant financial data documentation](https://www.myquant.cn/docs/l3333/913)
- [README](artifact/README.md)
- [Quick Reference](artifact/QUICK_REFERENCE.md)
- [Demo project](artifact/demo_project/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a GM_TOKEN for authenticated MyQuant use; live trading actions should remain gated by explicit human confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
