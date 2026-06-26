## Description: <br>
Fade sharp in-play price shocks on Polymarket soccer markets with a laddered limit-buy strategy that consumes pre-sized Simmer Pro signals, places recovery ladder orders, and manages exits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External trading operators use this skill to run a dry-run-first or explicitly live Polymarket shock-fade workflow for in-play soccer markets. It is intended for users who understand automated trading, wallet exposure, Pro signal access, and the limits of unvalidated strategy parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real Polymarket orders and expose wallet funds to irreversible trading losses. <br>
Mitigation: Start in dry-run, avoid setting WALLET_PRIVATE_KEY until ready, use a limited wallet, and keep the per-shock stake small. <br>
Risk: The strategy parameters and defaults are disclosed as a framework and are not validated as a guaranteed profitable edge. <br>
Mitigation: Review dry-run ladders against real shocks, understand spreads and latency, and only widen filters or increase size after observing performance. <br>
Risk: The skill requires Simmer Pro shock signals and Polymarket order-book mechanics; the sim venue is only a plumbing smoke test. <br>
Mitigation: Confirm Pro access and use the Polymarket venue for actual ladder behavior; do not treat sim output as strategy validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-soccer-shock-ladder) <br>
- [RohOnChain framework credit](https://x.com/RohOnChain) <br>
- [Simmer shock ladder configuration endpoint](https://api.simmer.markets/api/sdk/shock-ladder/config) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python execution entrypoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dry-run logs by default; live mode can place Polymarket orders only when explicitly enabled.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
