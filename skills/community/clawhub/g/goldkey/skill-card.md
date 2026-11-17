## Description:

Preflight proposed agent actions with GoldKey Action Gate for deterministic ALLOW, REVIEW, or BLOCK receipts, and guide feature-gated GoldKey Guard beta workflows for MCP, HTTPS, AgentCash, and supported Base/EVM calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-ing](https://clawhub.ai/user/noah-ing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to screen proposed agent actions, configure paid GoldKey checks, evaluate utility-pass usage, and operate Guard beta flows where a local enforcer controls access to real connectors or wallet signers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GoldKey Action Gate, component utilities, and Guard beta can trigger real nonrefundable USDC payments.

Mitigation: Require explicit current authorization for the exact endpoint, serialized request body, chain, amount, and payment path; reconcile ambiguous results before any retry.

Risk: Wallet-adjacent tokens, one-use signatures, and signer access may be exposed if passed through prompts, command arguments, logs, or shell history.

Mitigation: Use the agent secret store or stdin for sensitive values, keep low-balance segregated wallets where possible, and never place private keys, tokens, or signatures in command arguments.

Risk: Guard beta is advisory if the guarded agent can bypass the local enforcer and reach the connector, AgentCash wallet, upstream credential, or execution signer directly.

Mitigation: Make the local enforcer the exclusive execution path, remove direct routes to protected credentials and signers, and fail closed on any possible bypass.

Risk: Runtime package workflows can download or install executable artifacts.

Mitigation: Obtain authorization before package download or cache changes, verify the documented Guard enforcer integrity values, and install only the verified artifact with lifecycle scripts disabled where directed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/noah-ing/skills/goldkey)
- [GoldKey Repository](https://github.com/noah-ing/goldkey)
- [GoldKey Guard Beta](references/guard-beta.md)
- [GoldKey Utility Pass and Scoped Keys](references/pass-and-keys.md)
- [x402scan GoldKey Server](https://www.x402scan.com/server/8447beac-d24b-434a-bd01-5abfdab53f84)
- [Poncho Action Gate Listing](https://tryponcho.com/tool/url_aHR0cHM6Ly9nb2xka2V5LWVkZ2Utc3RvcmVmcm9udC5ub2FoLWluZy53b3JrZXJzLmRldi92MS9hY3Rpb24tZ2F0ZQ)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes paid-action receipts, reason codes, check details, and fail-closed stop conditions when applicable.]

## Skill Version(s):

1.0.10 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
