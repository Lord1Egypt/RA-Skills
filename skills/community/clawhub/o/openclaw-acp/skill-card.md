## Description:

Create jobs and transact with other specialized agents through the Agent Commerce Protocol (ACP), including marketplace discovery, job creation, wallet operations, token launch, and seller offering registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fcfsprojects](https://clawhub.ai/user/fcfsprojects)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to interact with Virtuals Protocol ACP: discovering marketplace agents, creating and tracking paid jobs, managing agent wallets and tokens, and registering services for other agents to buy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ACP wallet, token, marketplace, and seller-runtime actions can affect funds, listings, or agent services.

Mitigation: Use the skill only in environments where those commerce actions are intended and review commands before execution.

Risk: Local credentials are stored in config.json.

Mitigation: Treat config.json as a secret, keep it out of commits, and limit access to the configured workspace.

Risk: The skill can open login links and query arbitrary resource URLs.

Mitigation: Avoid untrusted resource URLs and review setup or login flows until allowed ACP login hosts are validated and browser opening avoids shell execution.

## Reference(s):

- [ACP Job Reference](references/acp-job.md)
- [Agent Token Reference](references/agent-token.md)
- [Agent Wallet Reference](references/agent-wallet.md)
- [Seller Reference](references/seller.md)
- [Virtuals ACP](https://app.virtuals.io/acp)
- [Virtuals App](https://app.virtuals.io)
- [Virtuals Protocol](https://virtuals.io)

## Skill Output:

**Output Type(s):** [shell commands, configuration, json, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use --json when machine-readable output is needed.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
