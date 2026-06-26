## Description: <br>
Build and operate a metered public API endpoint for OpenClaw skills and agents with API-key auth, per-request usage logging and pricing, prepaid balances, and BTC/ETH top-ups through payment-processor webhooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arshingleton](https://clawhub.ai/user/arshingleton) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to package an OpenClaw capability as a paid public API with signed API keys, prepaid usage metering, rate limits, balance tracking, and crypto payment top-ups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment webhooks can mutate prepaid balances. <br>
Mitigation: Use strong provider-specific webhook secrets, verify signatures, enforce idempotency, and fail closed when any required secret is missing. <br>
Risk: Administrative endpoints can create keys and inspect usage data. <br>
Mitigation: Restrict admin endpoints with strong tokens, network controls, and operational access review before deployment. <br>
Risk: The service stores usage, payment, and balance metadata. <br>
Mitigation: Protect the Postgres database and document what metadata is stored, retained, and exposed to operators. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [Billing and Ledger Notes](references/billing_ledger.md) <br>
- [Agent Integration Prompt](references/integration_prompt.md) <br>
- [Payment Provider Adapters](references/providers.md) <br>
- [Next.js Starter Deployment](scripts/nextjs-starter/README_DEPLOY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command snippets and bundled JavaScript implementation files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes reference server and serverless starter assets for signed API access, metered usage, balance management, and payment webhook integration.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
