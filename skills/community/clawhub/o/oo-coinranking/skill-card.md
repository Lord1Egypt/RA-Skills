## Description: <br>
Coinranking (coinranking.com). Use this skill for ANY Coinranking request: searching and reading data through an OOMOL-connected account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Coinranking cryptocurrency market data through the OOMOL oo CLI, including coin details, price history, global statistics, reference currencies, coin lists, and search suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an authenticated OOMOL connection to Coinranking and may depend on sensitive credentials managed outside the agent. <br>
Mitigation: Use the existing OOMOL connection flow and avoid exposing raw API tokens in prompts, files, or command output. <br>
Risk: Coinranking market data can be time-sensitive and may be incomplete or stale for financial decisions. <br>
Mitigation: Treat returned cryptocurrency data as informational and verify critical market decisions against authoritative sources before acting. <br>
Risk: The skill executes oo CLI shell commands against a connected external service. <br>
Mitigation: Inspect the live action schema before building payloads and review commands before execution. <br>


## Reference(s): <br>
- [Coinranking homepage](https://coinranking.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [Skill page](https://clawhub.ai/oomol/oo-coinranking) <br>
- [Publisher profile](https://clawhub.ai/user/oomol) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to inspect each live action schema before constructing payloads and returns Coinranking connector responses as JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
