## Description: <br>
Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, or long-form research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baofeng-tech](https://clawhub.ai/user/baofeng-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call AIsa-hosted Perplexity Sonar endpoints for current web answers, cited synthesis, analytical reasoning, and longer research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional system instructions are sent to AIsa-hosted Perplexity endpoints. <br>
Mitigation: Use the skill only when sharing the submitted content with that external API is permitted. <br>
Risk: The skill requires a sensitive AISA_API_KEY credential. <br>
Mitigation: Store AISA_API_KEY in a secure environment or secret manager and avoid hardcoding it in files or prompts. <br>
Risk: Deep research requests can time out or take longer than standard search calls. <br>
Mitigation: Narrow the prompt, retry later, or use sonar-pro or sonar-reasoning-pro when a faster answer is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/baofeng-tech/perplexity-search-aisa) <br>
- [AIsa](https://aisa.one) <br>
- [Sonar API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar) <br>
- [Sonar Pro API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-pro) <br>
- [Sonar Reasoning Pro API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-reasoning-pro) <br>
- [Sonar Deep Research API Reference](https://aisa.one/docs/api-reference/perplexity/post_perplexity-sonar-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and sends user prompts to AIsa-hosted Perplexity endpoints.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
