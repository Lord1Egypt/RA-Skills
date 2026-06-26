## Description: <br>
Operate mempool.space public Bitcoin and Lightning explorer APIs through UXC with a curated OpenAPI schema, no-auth setup, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to query public mempool.space Bitcoin and Lightning explorer data for fees, mempool state, block height, address and transaction status, and Lightning node or channel reads without authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried Bitcoin addresses, transaction IDs, Lightning public keys, and search terms are sent to mempool.space. <br>
Mitigation: Use the skill only for data that is appropriate to query through a public explorer service. <br>
Risk: The setup references an OpenAPI schema from a GitHub main-branch URL. <br>
Mitigation: For automated or sensitive workflows, verify or pin the schema before use. <br>
Risk: Mempool state and Lightning rankings can change quickly. <br>
Mitigation: Re-query current values instead of relying on cached results for time-sensitive decisions. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/mempool-space-public.openapi.json) <br>
- [OpenAPI schema URL](https://raw.githubusercontent.com/holon-run/uxc/main/skills/mempool-space-openapi-skill/references/mempool-space-public.openapi.json) <br>
- [Official mempool repository](https://github.com/mempool/mempool) <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/mempool-space-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on read-only public API queries and stable JSON envelope parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
