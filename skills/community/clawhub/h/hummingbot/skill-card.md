## Description: <br>
Agent skill that faithfully reproduces Hummingbot CLI commands (connect, balance, create, start, stop, status, history) via Hummingbot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading operators use this skill to manage Hummingbot API workflows, including connecting exchanges, checking balances, creating and starting V2 bots, monitoring status and history, and stopping bots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect live Hummingbot trading workflows and exchange-connected accounts. <br>
Mitigation: Use paper trading first and require explicit human approval before starting bots, stopping bots, placing orders, canceling orders, or using leveraged strategies. <br>
Risk: Weak Hummingbot API credentials or default credentials can expose trading controls. <br>
Mitigation: Set strong Hummingbot API credentials before use and avoid relying on default admin credentials. <br>
Risk: Exchange secrets may be exposed if passed directly on the command line. <br>
Mitigation: Prefer protected environment or configuration files for secrets and avoid command-line arguments for exchange API keys when possible. <br>
Risk: Exchange API keys with withdrawal permissions increase impact if credentials are misused. <br>
Mitigation: Disable withdrawal permissions on exchange API keys used with this skill. <br>


## Reference(s): <br>
- [PMM Mister Controller](artifact/references/pmm_mister.md) <br>
- [PMM V1 Controller](artifact/references/pmm_v1.md) <br>
- [ClawHub Hummingbot skill page](https://clawhub.ai/fengtality/hummingbot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Hummingbot API workflows that affect exchange credentials, bot lifecycle, orders, positions, and trading history.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
