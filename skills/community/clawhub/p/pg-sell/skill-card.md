## Description: <br>
Guides agents through selling API capacity on ProxyGate, including creating and managing listings, exposing local services through tunnels, rotating keys, uploading docs, managing headers, and viewing earnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to publish, price, and maintain ProxyGate API listings, expose local services through dev or production tunnels, and monitor seller balances and settlements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands can expose local services and change live ProxyGate listings, prices, headers, or credentials. <br>
Mitigation: Confirm the intended listing ID, exposed port, price, headers, credentials, and tunnel mode before running commands; validate in dev mode before starting a production tunnel. <br>
Risk: Wallet and settlement workflows can move funds or affect seller earnings. <br>
Mitigation: Use dry-run or preview modes where available, verify amounts and destination details, and require explicit confirmation before deposits, withdrawals, deletes, or credential rotations. <br>
Risk: Examples include API keys and credential rotation patterns that could leak secrets if copied into shared prompts or shell history. <br>
Mitigation: Keep real secrets in local configuration or a secret manager, avoid pasting them into shared contexts, and rotate credentials only after confirming the target listing. <br>
Risk: Broad activation language could cause seller operations to be suggested when the user only needs general ProxyGate information. <br>
Mitigation: Use the skill for ProxyGate seller workflows and ask for confirmation before destructive, financial, credential, or production tunnel actions. <br>


## Reference(s): <br>
- [ProxyGate CLI Command Reference](references/commands.md) <br>
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with bash, YAML, and TypeScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands for ProxyGate CLI listing management, tunneling, credentials, documentation, balances, and settlements.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
