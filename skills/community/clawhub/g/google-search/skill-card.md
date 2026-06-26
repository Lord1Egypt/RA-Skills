## Description: <br>
Search the web using Google Custom Search Engine (PSE). Use this when you need live information, documentation, or to research topics and the built-in web_search is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mxfeinberg](https://clawhub.ai/user/mxfeinberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to run live web searches through Google Custom Search when built-in web search is unavailable. It supports research, documentation lookup, and retrieving current information after Google API credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries to Google's Custom Search API, which can expose sensitive query text to an external service. <br>
Mitigation: Avoid searching for confidential content and review queries before execution in sensitive environments. <br>
Risk: The skill requires a Google Custom Search API key and Programmable Search Engine ID. <br>
Mitigation: Use a restricted API key, keep .env files private, and ensure credential files are excluded from source control. <br>


## Reference(s): <br>
- [Google Programmable Search Engine](https://cse.google.com/cse/all) <br>
- [Google Custom Search JSON API](https://www.googleapis.com/customsearch/v1) <br>
- [ClawHub skill page](https://clawhub.ai/mxfeinberg/google-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON search results and concise setup or command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
