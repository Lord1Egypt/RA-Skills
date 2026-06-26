## Description: <br>
This skill helps an agent query a Chinese national laws and regulations knowledge base and format retrieved statutes, article numbers, article text, and relevance scores for legal-question workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eastern-law-firm](https://clawhub.ai/user/eastern-law-firm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Legal researchers, support teams, and agent builders can use this skill to retrieve relevant Chinese legal provisions, locate specific articles, and present search results for legal Q&A or preliminary research. Users should verify retrieved legal content against authoritative sources before relying on it. <br>

### Deployment Geography for Use: <br>
Global, with content focused on Chinese national laws and regulations <br>

## Known Risks and Mitigations: <br>
Risk: Legal questions may contain sensitive personal or case details that are sent to an external OrientLaw-hosted API. <br>
Mitigation: Avoid including names, confidential facts, or sensitive case details in queries unless the deployment owner has approved that data flow. <br>
Risk: The release includes a hardcoded bearer token for the external search API. <br>
Mitigation: Rotate the exposed credential and move API authentication into a managed secret or environment variable before broad distribution. <br>
Risk: Retrieved legal text may be incomplete, irrelevant, or outdated for a user's jurisdiction or matter. <br>
Mitigation: Treat results as retrieval assistance, preserve the skill's no-speculation behavior for empty results, and verify legal conclusions against authoritative sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eastern-law-firm/national-law-knowledge-search) <br>
- [API response format](references/api_response_format.md) <br>
- [Search script](scripts/search_knowledge.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON retrieval results formatted into legal text summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a query string and integer topk value; exact article queries should request one result, while broader legal questions request multiple results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
