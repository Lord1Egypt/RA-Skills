## Description: <br>
Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renning22](https://clawhub.ai/user/renning22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when they specifically need Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research through AIsa for web-grounded answers, synthesis, reasoning, or research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and optional system messages are sent to the external AIsa API using the user's AISA API key. <br>
Mitigation: Use a dedicated key where possible, monitor quota and billing, and avoid sending secrets, regulated data, or proprietary internal material unless external processing by api.aisa.one is acceptable. <br>
Risk: Long-form deep research requests can be slower and may time out. <br>
Mitigation: Narrow the query, retry later, or use sonar-pro or sonar-reasoning-pro when a faster response is needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/renning22/my-perplexity-search) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [AIsa Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [AIsa Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [AIsa Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [AIsa Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the bundled Python client.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, curl for examples, and AISA_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
