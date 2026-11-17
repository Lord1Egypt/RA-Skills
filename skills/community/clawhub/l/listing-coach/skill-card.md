## Description:

Query the configured real estate Listing Coach knowledge base and return the exact retrieval output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woowonjae1](https://clawhub.ai/user/woowonjae1)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retrieve real estate listing coaching language, including listing scripts, expired listing scripts, FSBO scripts, and objection scripts, from the configured knowledge base and return the retrieved text exactly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and retrieved results are sent through an external knowledge-base lookup, and the security guidance warns against using sensitive queries.

Mitigation: Use only non-sensitive prompts until the publisher documents the external data flow and the deployment has been reviewed.

Risk: The skill includes embedded credential defaults and uses a non-HTTPS endpoint by default.

Mitigation: Require publisher-supplied credential handling and HTTPS configuration before deployment.

Risk: Retrieved knowledge-base output is pasted back exactly and may contain unvetted or misleading content.

Mitigation: Treat retrieved output as external content and review it before relying on it for customer-facing advice.

Risk: Lookup results are written to temporary Markdown files.

Mitigation: Avoid sensitive query content and remove temporary result files after use.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown retrieval output, returned exactly as produced by the knowledge-base lookup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes search result headings, recall scores, source lines, elapsed time, token totals, and request ID when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
