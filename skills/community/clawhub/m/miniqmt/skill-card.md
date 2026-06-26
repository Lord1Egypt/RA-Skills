## Description: <br>
miniQMT is a lightweight quantitative trading terminal skill that helps agents use the xtquant SDK for market data access and programmatic trading from external Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system operators use this skill to understand miniQMT setup, connect Python code to xtquant market-data and trading APIs, and draft examples for brokerage-enabled quantitative workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward live brokerage trading, automated strategies, account-data export, and bank-linked account actions. <br>
Mitigation: Use paper or test accounts first and require explicit human approval for every live order, automated strategy, transfer, or account-data export. <br>
Risk: Examples and generated code may handle brokerage, bank, fund, or account credentials unsafely if copied into a live workflow. <br>
Mitigation: Never hardcode bank, fund, or brokerage passwords; store secrets outside generated examples and review code before execution. <br>
Risk: Trading examples may write account or market data to local paths that expose sensitive information. <br>
Mitigation: Restrict export paths, avoid shared directories, and review any generated file output before running it with real account data. <br>


## Reference(s): <br>
- [ClawHub miniQMT skill page](https://clawhub.ai/coderwpf/miniqmt) <br>
- [xtquant native API start guide](http://dict.thinktrader.net/nativeApi/start_now.html) <br>
- [xtdata usage guide](http://dict.thinktrader.net/nativeApi/xtdata.html) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact quick reference](artifact/QUICK_REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include examples for live trading, account queries, data export, and local miniQMT or xtquant setup.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
