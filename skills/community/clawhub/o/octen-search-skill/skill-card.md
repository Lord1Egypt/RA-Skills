## Description: <br>
Real-time web search for AI agents powered by Octen, with date filtering and LLM-ready results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[octenai](https://clawhub.ai/user/octenai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve current web results, monitor news, and gather time-filtered information through Octen search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the OCTEN_API_KEY are sent to Octen's HTTPS search API. <br>
Mitigation: Confirm Octen is trusted for the intended queries, keep OCTEN_API_KEY stored securely and scoped appropriately, rotate it if exposed, and avoid sensitive private queries unless Octen's privacy and retention practices meet the use case. <br>


## Reference(s): <br>
- [Octen homepage](https://octen.ai) <br>
- [Octen Search API endpoint](https://api.octen.ai/search) <br>
- [ClawHub skill listing](https://clawhub.ai/octenai/octen-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown-style terminal output listing search result titles, URLs, publish times, and highlights] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and OCTEN_API_KEY; result count is clamped from 1 to 20 and optional ISO 8601 start/end time filters are supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
