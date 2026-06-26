## Description: <br>
Autonomous but risk-bounded options trading agent spec for the Perfect Storm strategy in paper-trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[essam9009](https://clawhub.ai/user/essam9009) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to configure, operate, or evaluate an OpenClaw-based paper options trader that scans an approved universe, scores PS+/PS- setups, selects liquid long call or put contracts, enforces risk limits, and journals decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow could be pointed at live brokerage credentials or a live trading endpoint. <br>
Mitigation: Use Alpaca paper credentials only, verify the base URL is the paper endpoint, and halt if any live endpoint or live credential signal appears. <br>
Risk: Options strategy outputs can be financially risky, incomplete, or unsuitable for real capital decisions. <br>
Mitigation: Use the skill for paper trading, enforce the provided risk limits, review every decision object, and treat no-trade outcomes as valid. <br>
Risk: Journals and decision records may contain sensitive account, order, or strategy information. <br>
Mitigation: Keep generated journals private and review storage or sharing practices before using them outside the paper-trading environment. <br>


## Reference(s): <br>
- [Skill specification](artifact/SKILL.md) <br>
- [Strategy rulebook](artifact/AGENTS.md) <br>
- [Risk configuration](artifact/risk_config_openclaw_best_practices.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with JSON decision objects and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paper-trading decisions include risk checks, blockers, confidence scores, and journal notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
