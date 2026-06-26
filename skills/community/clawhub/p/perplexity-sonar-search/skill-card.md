## Description: <br>
Perplexity Sonar search and answer generation through AIsa for citation-backed web answers, analytical reasoning, and long-form research reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill when they specifically need Perplexity Sonar, Sonar Pro, Sonar Reasoning Pro, or Sonar Deep Research responses through AIsa instead of structured scholar or web retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries and optional system instructions are sent to external AIsa/Perplexity-backed services. <br>
Mitigation: Avoid sending secrets, personal data, regulated content, or confidential business material unless external processing is permitted by policy. <br>
Risk: The AISA_API_KEY is required for API calls. <br>
Mitigation: Keep the key scoped, stored outside prompts and source text, and rotated according to normal credential management practice. <br>
Risk: Sonar Deep Research can be slower and may time out. <br>
Mitigation: Narrow the query, retry later, or use sonar-pro or sonar-reasoning-pro for faster responses. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aisadocs/perplexity-sonar-search) <br>
- [AIsa Profile](https://clawhub.ai/user/aisadocs) <br>
- [Sonar API Reference](https://docs.aisa.one/reference/post_perplexity-sonar) <br>
- [Sonar Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-pro) <br>
- [Sonar Reasoning Pro API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-reasoning-pro) <br>
- [Sonar Deep Research API Reference](https://docs.aisa.one/reference/post_perplexity-sonar-deep-research) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses from the bundled client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The deep research endpoint uses a longer timeout and retries; users may narrow prompts or choose a faster Sonar mode when responses time out.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
