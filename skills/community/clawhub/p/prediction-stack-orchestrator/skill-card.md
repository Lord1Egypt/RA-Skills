## Description: <br>
Three-agent pipeline orchestrator (Kalshalyst, Eval, Executor) for automated Kalshi prediction market trading with validation loops and retry logic. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingmadellc](https://clawhub.ai/user/kingmadellc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and prediction-market operators use this skill to coordinate an automated Kalshi trading pipeline that filters markets, routes estimates, validates reasoning, applies retry logic, sizes positions, executes trades, and reports portfolio metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an automated prediction-market trading orchestrator that may execute live trades. <br>
Mitigation: Use paper-trading or manual approval gates before live use, and set hard spend and loss limits. <br>
Risk: The bundled monitor exposes local trading-stack status, configs, logs, and process details over an unauthenticated network service. <br>
Mitigation: Run the monitor only on localhost or behind authentication, and redact secrets and sensitive logs before sharing output. <br>
Risk: Local prompts and configuration can directly influence trading behavior. <br>
Mitigation: Review all local prompt and configuration files before enabling automated execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kingmadellc/prediction-stack-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON logs and Markdown status reports, with operational guidance and configuration details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces market intake, validation, retry, sizing, execution, and dashboard status records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
