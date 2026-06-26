## Description: <br>
Automatically selects Google for English or international web searches and Baidu for Chinese or China-related searches, then returns unified search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run web searches from Python or the CLI with automatic routing to Google for English or international queries and Baidu for Chinese or China-related queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Google or Baidu using configured provider credentials. <br>
Mitigation: Avoid searching for secrets or confidential data and inform users which provider receives each query. <br>
Risk: Provider API keys are loaded from environment variables or a local .env file. <br>
Mitigation: Use limited-scope or quota-limited keys and keep local .env files out of published artifacts and commits. <br>
Risk: Runtime behavior depends on external search APIs and Python dependencies. <br>
Mitigation: Pin or review dependencies and install the skill in an isolated environment for sensitive use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leohuang8688/google-baidu-search) <br>
- [Google Custom Search documentation](https://cloud.google.com/custom-search/docs) <br>
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/) <br>
- [Baidu AI documentation](https://ai.baidu.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Formatted text with Markdown-style result entries, Python list/dictionary result objects, and CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires at least one configured provider credential; Google results are capped at 10 per request by the provider API.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
