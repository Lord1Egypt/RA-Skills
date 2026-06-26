## Description: <br>
OpenServ Client guides developers through using @openserv-labs/client to manage OpenServ agents, workflows, triggers, tasks, authentication, x402 payments, ERC-8004 identity, and the Platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[issa-me-sush](https://clawhub.ai/user/issa-me-sush) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to provision OpenServ agents, configure workflows and triggers, manage platform credentials, and integrate payment or on-chain identity flows for deployed agent services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys, auth tokens, wallet private keys, and public webhook URLs that could expose accounts or agent endpoints if copied into logs or source control. <br>
Mitigation: Use a test account or wallet first, keep .env and .openserv.json out of source control, avoid logging secrets or full webhook URLs, and rotate credentials if they are exposed. <br>
Risk: Provisioning, ERC-8004 registration, cleanup, and wallet deletion examples can affect real OpenServ resources, wallet material, or on-chain identity records. <br>
Mitigation: Back up wallet material before registration, confirm the target agent and workflow IDs before cleanup, and run destructive commands only after verifying the intended resources. <br>


## Reference(s): <br>
- [OpenServ Client API Reference](reference.md) <br>
- [OpenServ Client Troubleshooting](troubleshooting.md) <br>
- [Example Environment File](examples/env.example.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and environment configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, provisioning, API usage, troubleshooting, and cleanup guidance for OpenServ client workflows.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
