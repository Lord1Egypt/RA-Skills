## Description:

Google Search with intelligent caching, rate limiting, and cost optimization. Uses OpenClaw tools + free APIs. 10x faster, 99% cheaper than v1.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gloriaolk](https://clawhub.ai/user/gloriaolk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to run cached, rate-limited web searches and batch query workflows while prioritizing lower-cost search methods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises real search integrations but may return mock or fabricated results.

Mitigation: Review the search implementation before use and do not rely on live-search outputs until mock oxylabs paths are removed or clearly disabled.

Risk: Search queries and results may be stored in a local plaintext SQLite cache.

Mitigation: Avoid sensitive queries unless caching is disabled, the cache path is protected, or cache retention is configured appropriately.

Risk: Batch inputs and search queries may be sent to external search providers.

Mitigation: Do not include secrets or sensitive data in queries, and review provider terms and credentials before batch use.

Risk: Dependencies are declared with minimum versions rather than pinned versions.

Mitigation: Install in an isolated environment and pin reviewed dependency versions for controlled deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gloriaolk/skills/google-search-unlimited-v2)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown usage guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries can be cached locally; batch mode can write structured result files.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
