## Description: <br>
Run automated liquidity provision strategies on concentrated liquidity (CLMM) DEXs using Hummingbot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengtality](https://clawhub.ai/user/fengtality) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and liquidity providers use this skill to deploy Hummingbot API and Gateway infrastructure, connect a Solana wallet, explore Meteora DLMM pools, run LP executor or rebalancer strategies, and analyze LP performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control live wallets and trading infrastructure. <br>
Mitigation: Use an isolated environment, a dedicated low-balance wallet, and review each wallet, stop, reset, Gateway, and trading action before execution. <br>
Risk: Default or weak API, configuration, and broker credentials may be present during setup. <br>
Mitigation: Change all API, configuration, and broker credentials before adding any wallet or running a strategy. <br>
Risk: Unsafe installation or reset behavior could affect a host or remove trading infrastructure state. <br>
Mitigation: Keep services bound to localhost, avoid running installers as root on a host, and review reset and database-repair actions before running them. <br>
Risk: Private keys may be exposed if passed through unsafe command-line workflows. <br>
Mitigation: Do not pass private keys on the command line; use the interactive wallet import flow and confirm shell history does not contain secrets. <br>


## Reference(s): <br>
- [LP Executor Guide](artifact/references/lp_executor_guide.md) <br>
- [LP Rebalancer Controller Guide](artifact/references/lp_rebalancer_guide.md) <br>
- [LP Agent Scripts README](artifact/scripts/README.md) <br>
- [Hummingbot API](https://github.com/hummingbot/hummingbot-api) <br>
- [ClawHub Skill Page](https://clawhub.ai/fengtality/lp-agent) <br>
- [Publisher Profile](https://clawhub.ai/user/fengtality) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and script-generated JSON, CSV, and HTML artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides infrastructure setup, wallet connection, pool exploration, LP strategy execution, and performance analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
