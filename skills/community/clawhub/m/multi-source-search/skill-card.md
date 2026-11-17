## Description:

Confidence-scored multi-source retrieval across web, scholar, Tavily, and Perplexity-backed research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external agent users use this skill to compare search results across web, scholar, Tavily, and Perplexity-backed sources before synthesizing a research answer or recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries, prompt text, optional system instructions, and submitted URLs are sent through api.aisa.one and downstream providers.

Mitigation: Use only approved non-confidential prompts and URLs, and avoid authenticated or internal pages unless that data sharing has been approved.

Risk: Search and research outputs may be incomplete, stale, or inconsistent across providers.

Mitigation: Review cited sources and compare returned source coverage before relying on synthesized conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/multi-source-search)
- [AIsa Documentation](https://aisa.one/docs)
- [AIsa API Reference](https://aisa.one/docs/api-reference/)
- [AIsa Verity](https://github.com/AIsa-team/verity)
- [Perplexity Sonar](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar)
- [Perplexity Sonar Pro](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-pro)
- [Perplexity Sonar Reasoning Pro](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-reasoning-pro)
- [Perplexity Sonar Deep Research](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-deep-research)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; remote requests may include user queries, prompt text, optional system instructions, and submitted URLs.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
