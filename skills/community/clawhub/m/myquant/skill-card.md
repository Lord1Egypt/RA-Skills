## Description: <br>
MyQuant is a Python SDK reference skill for the GoldMiner event-driven quantitative trading platform, covering backtesting, simulated trading, and live trading workflows for Chinese equities, futures, options, ETFs, and convertible bonds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to draft and understand GoldMiner `gm.api` strategy code, authentication setup, market data queries, backtests, simulated trading, and live-trading order workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GM_TOKEN credentials are financially sensitive if exposed in prompts, files, logs, or generated code. <br>
Mitigation: Keep GM_TOKEN private, prefer environment variables or a secret manager, and avoid hard-coding real tokens in strategy examples. <br>
Risk: Live-trading, market-order, close-all, cancel-all, and margin examples can affect real brokerage accounts. <br>
Mitigation: Test in backtest or simulated mode first and require deliberate human confirmation before running live-trading or account-wide order operations. <br>
Risk: Unpinned dependencies can change trading SDK behavior across environments. <br>
Mitigation: Pin dependencies for production use and validate strategy behavior in a controlled environment before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coderwpf/myquant) <br>
- [GoldMiner Homepage](https://www.myquant.cn) <br>
- [GoldMiner Python Documentation](https://www.myquant.cn/docs/python/41) <br>
- [GoldMiner Python Overview](https://www.myquant.cn/docs/python/python_overview) <br>
- [GoldMiner Downloads](https://www.myquant.cn/docs/downloads/698) <br>
- [GoldMiner Financial Data Documentation](https://www.myquant.cn/docs/l3333/913) <br>
- [GoldMiner Community](https://www.myquant.cn/community) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples may require a GoldMiner account, a GM_TOKEN credential, and deliberate review before live-trading execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
