## Description: <br>
Scans and compares USDC yield farming opportunities on Base and Arbitrum with APY rankings, vault migration breakeven analysis, historical trends, and protocol risk summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaoolucas](https://clawhub.ai/user/joaoolucas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and DeFi analysts use this skill to compare USDC yield opportunities, review protocol risk context, inspect APY history, and estimate whether moving between vaults is worthwhile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Yield, TVL, protocol risk, and APY history are informational estimates that can change quickly. <br>
Mitigation: Run the tool for current data, treat APYs as point-in-time snapshots, and verify values independently before making allocation decisions. <br>
Risk: The bundled Python script makes HTTPS requests to DeFiLlama and writes a temporary local cache. <br>
Mitigation: Install only when this network access and short-lived cache behavior are acceptable in the target environment. <br>
Risk: Breakeven calculations use approximate gas and bridge cost assumptions. <br>
Mitigation: Check current transaction, bridge, and protocol costs before acting on a migration verdict. <br>


## Reference(s): <br>
- [Protocol Reference](references/protocols.md) <br>
- [DeFiLlama Yields Pools API](https://yields.llama.fi/pools) <br>
- [DeFiLlama Yields Chart API](https://yields.llama.fi/chart/{pool_id}) <br>
- [n0ir](https://n0ir.ai) <br>
- [ClawHub Release Page](https://clawhub.ai/joaoolucas/n0ir-defi-yield-scout) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown tables and narrative guidance, with optional JSON from the CLI tool.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on live DeFiLlama data, cached locally for 15 minutes by the bundled script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
