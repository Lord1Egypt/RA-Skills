## Description: <br>
Intelligent search for agents with multi-source retrieval across web, scholar, Tavily, and Perplexity Sonar models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run web, academic, Tavily, and Perplexity Sonar searches, then collect structured search results, citation-rich answers, deep research responses, or confidence-scored multi-source retrieval output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, prompts, optional system instructions, URLs, and the AIsa API key are sent to an external API and upstream providers. <br>
Mitigation: Use a dedicated revocable API key, avoid secrets or confidential internal URLs, and review prompts before submitting them. <br>
Risk: Tavily crawl/map and Sonar Deep Research can process broader or more detailed content than a single search query. <br>
Mitigation: Limit crawl targets and deep research prompts to content that is approved for external processing. <br>


## Reference(s): <br>
- [Skill Page](https://clawhub.ai/chaimengphp/openclaw-aisa-search) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa Documentation](https://docs.aisa.one) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [Perplexity Sonar](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [Perplexity Sonar Pro](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [Perplexity Sonar Reasoning Pro](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [Perplexity Sonar Deep Research](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>
- [AIsa Verity Reference Implementation](https://github.com/AIsa-team/verity) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and network access to AIsa API endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
