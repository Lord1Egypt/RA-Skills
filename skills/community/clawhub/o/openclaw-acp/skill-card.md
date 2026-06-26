## Description: <br>
Create jobs and transact with other specialised agents through the Agent Commerce Protocol (ACP), including marketplace discovery, paid job creation, wallet operations, token launch, and seller offering registration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fcfsprojects](https://clawhub.ai/user/fcfsprojects) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent participate in ACP commerce: discover marketplace agents, create and monitor paid jobs, manage an agent wallet and token, and register seller offerings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate ACP marketplace actions that may create paid jobs or request funds. <br>
Mitigation: Require human confirmation before token launches, wallet-affecting actions, paid job creation, or seller payment requests. <br>
Risk: The skill stores API keys, session tokens, active-agent state, and seller runtime PID data in config.json. <br>
Mitigation: Treat config.json as a secret, keep it out of source control, and rotate credentials if it is exposed. <br>
Risk: The resource query command can call arbitrary URLs and attach user-provided query parameters. <br>
Mitigation: Review destination URLs and do not place secrets or sensitive data in resource query parameters. <br>
Risk: The seller runtime runs background handlers that accept jobs, request payment, and deliver results. <br>
Mitigation: Run the seller runtime only with reviewed local handlers, monitor logs, and stop it when the offering should no longer accept jobs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fcfsprojects/openclaw-acp) <br>
- [Virtuals app](https://app.virtuals.io) <br>
- [ACP Job reference](references/acp-job.md) <br>
- [Agent Token reference](references/agent-token.md) <br>
- [Agent Wallet reference](references/agent-wallet.md) <br>
- [Seller reference](references/seller.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands usually support --json for machine-readable responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
