## Description: <br>
Analyze any EVM smart contract by fetching or accepting its ABI, discovering usage patterns, decoding function calls through Dune, generating analytics, and returning structured results for Ethereum, Polygon, BSC, Arbitrum, Optimism, Base, and Avalanche. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ramitphi](https://clawhub.ai/user/Ramitphi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to inspect verified EVM smart contracts, understand function usage, caller behavior, and transaction patterns, and receive links to generated Dune queries or dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The hosted analysis service receives contract addresses, chain selections, and any manually supplied ABI. <br>
Mitigation: Use only public contract data or ABI content that is acceptable to share with the hosted Supabase and Dune-based service. <br>
Risk: Generated Dune queries, decoded tables, and dashboards may persist outside the user's local environment. <br>
Mitigation: Review generated dashboard and Dune links before sharing them, and avoid submitting private or proprietary ABI data. <br>
Risk: Analytics can be incomplete when contracts lack verified ABIs, have little activity, or when Dune query execution fails or times out. <br>
Mitigation: Ask for a manual ABI when needed, disclose failed or empty query results, and treat generated summaries as analysis aids rather than authoritative contract audits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ramitphi/on-chain-analyitcs) <br>
- [On-chain analysis API endpoint](https://esraarlhpxraucslsdle.supabase.co/functions/v1/onchain-analysis) <br>
- [Dune query example](https://dune.com/queries/12345) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries with structured JSON analysis results, dashboard links, Dune query links, and chart-oriented data tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return TLDR text, ABI summaries, top method statistics, raw Dune table metadata, query SQL, rows for stat, timeseries, bar, pie, or scatter results, and per-query errors.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
