## Description: <br>
Coordinates five specialized agents to develop, backtest, deploy, package, and iterate OKX OnchainOS on-chain trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SynthThoughts](https://clawhub.ai/user/SynthThoughts) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to coordinate an agent team that turns trading ideas into on-chain strategy code, backtest artifacts, deployment steps, packaged skills, and post-live iteration reports. It is intended for OKX OnchainOS strategy workflows with explicit gates before live deployment and optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward live wallet, token approval, swap, transfer, contract-call, VPS deployment, and GitHub release actions. <br>
Mitigation: Require explicit user approval before any production deployment, release publication, token approval, swap, transfer, or contract-call action; start with dry-runs or test funds. <br>
Risk: Trading credentials and wallet access may be exposed or over-scoped if handled casually. <br>
Mitigation: Keep credentials in scoped environment variables or a secret manager, prefer read-only or limited keys where possible, and avoid logging secrets. <br>
Risk: Automated strategy changes can cause financial loss if backtests, risk limits, or user approvals are bypassed. <br>
Mitigation: Enforce the documented backtest, risk-profile, dry-run, rollback, and user-confirmation gates before live execution or iteration. <br>


## Reference(s): <br>
- [onchainos CLI interface reference](artifact/references/api-interfaces.md) <br>
- [Risk profile schema](artifact/references/risk-schema.json) <br>
- [Strategy lessons reference](artifact/references/strategy-lessons.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with generated code, JSON configuration, shell commands, reports, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create strategy workspaces, backtest outputs, deployment state, and packaged skill files.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release evidence; artifact metadata reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
