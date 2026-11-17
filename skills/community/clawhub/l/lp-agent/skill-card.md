## Description:

Run automated liquidity provision strategies on concentrated liquidity (CLMM) DEXs using Hummingbot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengtality](https://clawhub.ai/user/fengtality)

### License/Terms of Use:


## Use Case:

External developers and liquidity providers use this skill to deploy Hummingbot trading infrastructure, configure Solana Gateway access, add a wallet, explore Meteora DLMM pools, run LP Executor or Rebalancer strategies, and analyze position performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control local Hummingbot trading infrastructure and wallet import workflows.

Mitigation: Use a dedicated low-value wallet and install only in an environment where that trading control is acceptable.

Risk: Unsafe default credentials and reachable API or Gateway endpoints could expose trading controls.

Mitigation: Change default credentials before exposing any service and keep API/Gateway endpoints on localhost or trusted HTTPS only.

Risk: Deployment scripts can make broad local changes to Docker-based trading infrastructure.

Mitigation: Review the deployment script before running it with elevated privileges and avoid default non-interactive setup for real funds.

Risk: Generated reports may auto-open local HTML from trading data.

Mitigation: Use the no-open option for generated reports when the source data is untrusted.

## Reference(s):

- [LP Executor Guide](references/lp_executor_guide.md)
- [LP Rebalancer Controller Guide](references/lp_rebalancer_guide.md)
- [LP Agent Scripts](scripts/README.md)
- [Hummingbot API](https://github.com/hummingbot/hummingbot-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown with inline shell commands, configuration parameters, and generated CSV or HTML analysis file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local scripts that query APIs, deploy Docker-based services, manage wallets, create strategy configurations, and export or visualize LP position data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
