## Description:

通过 AISA 在网页、学术、Tavily 与综合分析层做多源证据搜索，并输出置信度。触发条件：当用户需要由多个搜索来源支撑的综合结论，而不是一次单点搜索时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to run AISA-backed web, academic, Tavily, sonar, and multi-source searches when they need synthesized evidence and confidence levels across multiple sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, supplied URLs, and synthesis payloads are sent to AISA using AISA_API_KEY.

Mitigation: Use a dedicated low-privilege API key if available, and avoid confidential prompts, sensitive research topics, private URLs, or signed URLs.

Risk: The bundled script exposes URL extraction and sonar commands beyond the main multi-source search workflow.

Mitigation: Review the selected command before execution and restrict use to the needed search mode when extract or sonar capabilities are not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/multi-search-zh)
- [AISA service](https://aisa.one)
- [AISA API base endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text summaries with result snippets, citations, confidence scores, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends search queries, URLs, and synthesis payloads to AISA-hosted endpoints.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
