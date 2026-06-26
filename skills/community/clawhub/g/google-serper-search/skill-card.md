## Description: <br>
This skill enables an agent to search the web and find images using the Serper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twodogegg](https://clawhub.ai/user/twodogegg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve current web or image search results, including news, organic results, related questions, and image metadata, through Serper-backed Google search endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, parameters, and related context are sent to Serper.dev using the user's API key. <br>
Mitigation: Use a dedicated API key and avoid searching for secrets, sensitive personal data, or confidential internal information. <br>
Risk: Persisting the Serper API key in shell startup files can expose the key to other local processes or account compromise. <br>
Mitigation: Store the key only where appropriate for the deployment environment and review shell configuration before making the setting permanent. <br>


## Reference(s): <br>
- [Serper API](https://serper.dev) <br>
- [API response reference](references/api_response.md) <br>
- [ClawHub release page](https://clawhub.ai/twodogegg/google-serper-search) <br>
- [Publisher profile](https://clawhub.ai/user/twodogegg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON search results from the Serper API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SERPER_API_KEY environment variable and sends search queries and parameters to Serper.dev.] <br>

## Skill Version(s): <br>
0.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
