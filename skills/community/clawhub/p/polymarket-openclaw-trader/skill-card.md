## Description: <br>
Reusable Polymarket and OpenClaw trading operations skill for setting up, running, tuning, monitoring, and deploying automated Polymarket trading projects with paper or live execution, environment configuration, risk controls, reporting, and dashboard operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[08820048](https://clawhub.ai/user/08820048) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and operate a Polymarket trading project, including paper or live execution, environment setup, process monitoring, runtime strategy settings, reporting, and deployment. It is intended for users who explicitly authorize trading operations and can comply with applicable trading-region restrictions. <br>

### Deployment Geography for Use: <br>
Global where Polymarket trading is legal and available; the skill instructs agents to stop trading attempts when geoblock or regional restrictions appear. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run live automated Polymarket trading with a wallet key as a persistent background process. <br>
Mitigation: Use paper mode first, inspect the separate bot code and dependencies, use a dedicated low-balance wallet, set strict order and loss limits, and require explicit approval before live trading, auto-restarts, production deployment, or committing persistent changes. <br>
Risk: Private keys or wallet secrets could be exposed if written into code, logs, or user-visible responses. <br>
Mitigation: Store sensitive values only in .env, never commit them, and report private-key status only as configured or not configured without echoing raw values. <br>
Risk: Trading may be blocked or unlawful in restricted regions. <br>
Mitigation: Stop trading attempts when geoblock or regional-restriction errors appear, tell the user there is a compliance limitation, and do not provide bypass instructions. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/08820048/polymarket-openclaw-trader) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational checklists, environment-variable guidance, process commands, deployment commands, and short code snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
