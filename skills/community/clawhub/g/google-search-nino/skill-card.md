## Description: <br>
Searches the web with Google Programmable Search Engine so agents can retrieve live information, documentation, or research material when built-in web search is unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ninonano64](https://clawhub.ai/user/ninonano64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add Google Custom Search queries to an OpenClaw workflow, returning live web search results from a configured Programmable Search Engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Google API key and search engine ID for outbound Google Custom Search requests. <br>
Mitigation: Keep credentials out of version control and prefer platform-managed secrets or user-level environment variables over a workspace .env file. <br>


## Reference(s): <br>
- [Google Programmable Search Engine setup](https://cse.google.com/cse/all) <br>
- [Google Custom Search JSON API endpoint](https://www.googleapis.com/customsearch/v1) <br>
- [ClawHub skill page](https://clawhub.ai/ninonano64/google-search-nino) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables; defaults to five search results unless a result count is supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
