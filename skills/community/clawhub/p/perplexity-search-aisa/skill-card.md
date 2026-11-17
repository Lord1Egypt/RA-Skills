## Description:

Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call AIsa-hosted Perplexity Sonar endpoints for citation-backed web answers, comparison and synthesis, analytical reasoning, and long-form research reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search prompts and optional system instructions are sent to an external AIsa/Perplexity API.

Mitigation: Do not submit secrets, private code, or sensitive personal data unless that data is approved for the external service.

Risk: The skill requires an AISA_API_KEY to call the external API.

Mitigation: Store the API key in the environment, restrict access to it, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/skills/perplexity-search-aisa)
- [AIsa](https://aisa.one)
- [Sonar API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar)
- [Sonar Pro API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-pro)
- [Sonar Reasoning Pro API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-reasoning-pro)
- [Sonar Deep Research API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-deep-research)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and AISA_API_KEY; Sonar Deep Research uses longer timeouts and retries.]

## Skill Version(s):

1.0.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
