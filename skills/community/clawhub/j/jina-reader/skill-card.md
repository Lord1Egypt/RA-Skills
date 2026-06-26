## Description: <br>
Jina Reader extracts clean web content through the Jina AI Reader API for URL-to-markdown reading, web search with full content, and fact-check grounding without exposing the host server IP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericsantos](https://clawhub.ai/user/ericsantos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch clean web content, run Jina-powered search, and fact-check statements while keeping the host server's IP out of direct target-site requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs, search queries, CSS selectors, and fact-check text are sent to Jina AI's external service. <br>
Mitigation: Avoid secrets, private intranet links, regulated data, personal data, credentials, and confidential business material unless that third-party processing is acceptable. <br>
Risk: The skill can use a JINA_API_KEY credential from the environment or local config. <br>
Mitigation: Store the API key securely and keep ~/.config/jina/api_key readable only by the local user. <br>


## Reference(s): <br>
- [Jina Reader](https://jina.ai/reader) <br>
- [ClawHub skill page](https://clawhub.ai/ericsantos/jina-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Shell output as Markdown, plain text, or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq. May use JINA_API_KEY from the environment or ~/.config/jina/api_key.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
