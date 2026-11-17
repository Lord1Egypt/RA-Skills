## Description:

Provides tools for debugging episodic memory systems including recall precision analysis, multi-modal encoding validation, indexing efficiency checks, and irrelevant recall detection for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose episodic-memory retrieval quality, encoding consistency, index coverage, irrelevant recall patterns, and memory drift in AI agent memory systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory records passed into the diagnostic functions may contain private or sensitive content.

Mitigation: Review and minimize memory data before analysis, and avoid passing unnecessary private content into the tool.

Risk: Recall, ranking, and health metrics can be misleading when ground truth labels, embeddings, or index statistics are incomplete or stale.

Mitigation: Validate labels and input statistics before using the generated recommendations to tune retrieval or indexing behavior.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [JavaScript diagnostic objects with metrics, issue lists, health scores, and recommendation text that can be summarized in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [All calculations are local and depend on caller-provided memories, queries, ground truth labels, embeddings, and index statistics.]

## Skill Version(s):

1.0.0 (source: evidence.json release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
