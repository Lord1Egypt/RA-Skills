## Description: <br>
Search the web using the Perplexity Agent API. Provides real-time information, news, and grounded answers with citations. Use when the user asks for: (1) Current events or news, (2) Information retrieval from the web, (3) Real-time data search, (4) In-depth research using web results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidsteelerose](https://clawhub.ai/user/davidsteelerose) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run real-time web searches through the Perplexity Agent API and return grounded answers for current events, news, information retrieval, and research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User search queries are sent to Perplexity under the configured API account. <br>
Mitigation: Use a dedicated PERPLEXITY_API_KEY where possible, monitor quota or billing, and avoid submitting secrets, private documents, or sensitive personal data unless that disclosure is acceptable. <br>


## Reference(s): <br>
- [Perplexity Agent API endpoint](https://api.perplexity.ai/v1/agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls] <br>
**Output Format:** [JSON object containing success, answer, and model fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PERPLEXITY_API_KEY and sends search queries to Perplexity under that API account.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
