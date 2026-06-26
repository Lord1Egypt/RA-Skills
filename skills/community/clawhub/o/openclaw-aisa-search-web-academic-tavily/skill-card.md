## Description: <br>
Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIsaDocs](https://clawhub.ai/user/AIsaDocs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run web, academic, smart, full-text, and Tavily-backed searches, then compare retrieved sources with confidence scoring for research, market analysis, news aggregation, and competitive analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, URLs, and retrieved-result payloads are sent to AIsa/Tavily-backed external services. <br>
Mitigation: Use a dedicated revocable AISA_API_KEY and avoid submitting secrets, regulated data, internal-only URLs, or private content. <br>
Risk: Crawl and extraction operations can retrieve content from user-supplied URLs. <br>
Mitigation: Limit crawl and extraction requests to public targets the user intends to query. <br>


## Reference(s): <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API documentation](https://aisa.mintlify.app) <br>
- [AIsa API reference](https://aisa.mintlify.app/api-reference/introduction) <br>
- [AIsa Verity reference implementation](https://github.com/AIsa-team/verity) <br>
- [ClawHub skill page](https://clawhub.ai/AIsaDocs/openclaw-aisa-search-web-academic-tavily) <br>
- [Publisher profile](https://clawhub.ai/user/AIsaDocs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 or curl plus AISA_API_KEY; API responses may include usage cost and remaining credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
