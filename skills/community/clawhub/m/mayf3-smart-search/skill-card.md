## Description:

Smart Search helps agents run multi-engine web, news, image, video, and book searches with automatic language detection, backend fallback, structured results, and optional page extraction through a DDGS-based script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to gather public web information, compare search results across engines, retrieve current news or vertical search results, and extract page content for downstream research or fact checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External searches and page extraction can disclose confidential queries, private URLs, internal hostnames, or customer data to third-party services.

Mitigation: Use only public, non-sensitive queries and URLs unless the runtime has approved network egress controls.

Risk: Batch search and arbitrary URL extraction can create broad or hard-to-review network activity.

Mitigation: Review batch files and extraction targets before use, restrict network access where possible, and keep result volumes scoped to the task.

Risk: Long-running searches or extraction attempts can stall an agent workflow.

Mitigation: Set reasonable timeout values and prefer the documented fallback mode for normal use.

Risk: Search results may be incomplete, stale, or misleading across engines.

Mitigation: Cross-check important claims with multiple sources and apply the skill's credibility assessment guidance before using results.

## Reference(s):

- [Smart Search skill documentation](artifact/SKILL.md)
- [Advanced search syntax](artifact/references/advanced-syntax.md)
- [Credibility assessment](artifact/references/credibility-assessment.md)
- [Search API upgrade paths](artifact/references/search-apis.md)
- [Vertical search routing](artifact/references/vertical-search.md)
- [ClawHub release page](https://clawhub.ai/mayf3/skills/mayf3-smart-search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with command examples and optional JSON or URL-only search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return structured search results, extracted page markdown, and batch-search outputs depending on command flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
