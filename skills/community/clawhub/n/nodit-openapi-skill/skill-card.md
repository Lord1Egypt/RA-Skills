## Description: <br>
Operate Nodit Web3 Data API reads through UXC with a curated OpenAPI schema, API-key auth, and overlap-aware guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure UXC access to Nodit's read-only Web3 Data API and perform multichain entity, balance, transaction, token metadata, and token price lookups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Nodit API keys may expose quota or account access if reused broadly. <br>
Mitigation: Use a dedicated Nodit API key with quota limits and configure it through the NODIT_API_KEY secret environment variable. <br>
Risk: Blockchain identifiers supplied in lookups are sent to Nodit. <br>
Mitigation: Avoid querying sensitive identifiers unless external API disclosure is acceptable for the task. <br>
Risk: A mutable hosted OpenAPI schema can change behavior over time. <br>
Mitigation: Use the packaged schema or a pinned schema URL when reproducible behavior is required. <br>
Risk: Entity lookup can hit plan or tier rate limits. <br>
Mitigation: Back off on HTTP 429 responses and prefer chain-specific reads when the target chain is already known. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/nodit-web3.openapi.json) <br>
- [Nodit introduction](https://developer.nodit.io/en/guides/overview/introduction) <br>
- [Nodit entity lookup docs](https://developer.nodit.io/reference/multichain_lookupentities) <br>
- [Nodit Web3 Data docs](https://developer.nodit.io/reference/gettransactionsbyaccount) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API calls, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON-oriented API guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Nodit API operations through UXC; responses should stay on the JSON output envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI schema) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
