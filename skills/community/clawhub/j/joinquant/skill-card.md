## Description: <br>
JoinQuant helps agents use the JoinQuant quantitative trading platform for A-share, futures, and fund data queries, event-driven strategy backtesting, online research, and simulated trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coderwpf](https://clawhub.ai/user/coderwpf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and quantitative-trading agents use this skill to look up JoinQuant APIs, configure local JQData access, and draft Python examples for market data research, backtesting, simulated trading, and strategy workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: JoinQuant credentials may be exposed if real usernames or passwords are pasted into prompts, source files, or shared examples. <br>
Mitigation: Use environment variables or a local secret manager, keep credentials out of prompts and repositories, and rotate any credentials that were exposed. <br>
Risk: Order-related examples can affect trading or simulated-trading accounts if run in the wrong account mode. <br>
Mitigation: Verify the account mode, strategy target, and order parameters before running order snippets, and prefer paper or simulated accounts for testing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/coderwpf/joinquant) <br>
- [JoinQuant Homepage](https://www.joinquant.com) <br>
- [JoinQuant API Documentation](https://www.joinquant.com/help/api/help) <br>
- [JoinQuant Community](https://www.joinquant.com/community) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JoinQuant credentials for live JQData access.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
