## Description:

Intelligent search for agents. Multi-source retrieval across web, scholar, Tavily, and Perplexity Sonar models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaimengphp](https://clawhub.ai/user/chaimengphp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to run structured web, academic, Tavily, and Perplexity Sonar searches, then generate citation-oriented answers or deep research reports. It supports fast lookup, scholar-backed research, multi-source retrieval, URL extraction, and confidence-scored result aggregation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, research prompts, and submitted URLs are sent to AIsa-backed third-party APIs.

Mitigation: Avoid private or internal URLs, secrets, regulated data, and confidential business context in queries, extraction requests, or Sonar prompts.

Risk: The skill requires an AISA_API_KEY for authenticated API calls.

Mitigation: Provide the key through the environment, rotate it if exposed, and do not paste it into prompts, docs, command history, or shared artifacts.

Risk: Long-form deep research requests may take longer or time out.

Mitigation: Use narrower prompts, retry later, or switch to Sonar Pro or Sonar Reasoning Pro for shorter answer-generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaimengphp/skills/openclaw-aisa-search)
- [OpenClaw homepage](https://openclaw.ai)
- [AIsa API documentation](https://docs.aisa.one)
- [AIsa API reference](https://docs.aisa.one/reference/)
- [AIsa Sonar endpoint](https://docs.aisa.one/reference/post_perplexity-sonar)
- [AIsa Sonar Pro endpoint](https://docs.aisa.one/reference/post_perplexity-sonar-pro)
- [AIsa Sonar Reasoning Pro endpoint](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro)
- [AIsa Sonar Deep Research endpoint](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research)
- [AIsa Verity reference implementation](https://github.com/AIsa-team/verity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON API responses, markdown/text answers, and inline shell or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AIsa-backed search, Tavily, and Perplexity Sonar endpoints.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
