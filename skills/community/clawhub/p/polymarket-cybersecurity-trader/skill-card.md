## Description: <br>
Trades Polymarket prediction markets on major cyberattacks, ransomware incidents, data breaches, zero-day exploits, and national cybersecurity legislation using cybersecurity-specific timing and tractability signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diagnostikon](https://clawhub.ai/user/diagnostikon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to discover cybersecurity-related Polymarket markets, generate conviction-based YES/NO trade decisions, and execute them through Simmer in paper mode by default or live mode when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Simmer trading credential. <br>
Mitigation: Install only when the credential can be protected, scoped, and rotated according to the user's normal credential handling practices. <br>
Risk: Live mode can place real Polymarket trades with USDC. <br>
Mitigation: Run in the default paper mode first, enable live trading only with the explicit live flag, and keep live position limits low. <br>
Risk: The documented minimum-volume filter does not appear to be enforced by the code. <br>
Mitigation: Review market liquidity before live execution and do not rely on the documented minimum-volume setting as a trading safeguard. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/polymarket-cybersecurity-trader) <br>
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/) <br>
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces trading decisions, execution logs, tunable configuration guidance, and safety notes for paper or live Polymarket execution.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
