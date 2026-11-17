## Description:

Recommends and price-checks AI models and hosting providers using InferenceIndexer, including cost audits for existing model deployments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desmartin01](https://clawhub.ai/user/desmartin01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compare models and providers by price and suitability, check privacy or regional availability, and estimate savings at their expected token volume.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model-selection constraints, model IDs, and pricing questions are sent to InferenceIndexer; usage-log details may be sensitive.

Mitigation: Share only the information needed for a recommendation and inspect sensitive usage logs only with the user's explicit consent.

Risk: A cheaper provider may differ in reliability, latency, or suitability for production traffic.

Mitigation: Review provider differences and validate the recommendation before switching production traffic.

Risk: ZDR and EU-sovereignty flags are provider-stated rather than independently verified.

Mitigation: Confirm privacy and residency commitments with the provider before relying on them.

## Reference(s):

- [Inference Indexer on ClawHub](https://clawhub.ai/desmartin01/skills/inference-indexer)
- [InferenceIndexer MCP configuration](https://www.inferenceindexer.ai/.well-known/mcp-config.json)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance and plain-text cost comparisons]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations include prices, rationale, data freshness, and caveats; cost audits compare monthly and annual spend.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
