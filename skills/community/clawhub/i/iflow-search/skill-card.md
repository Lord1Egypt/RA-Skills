## Description: <br>
Provides web search, image search, and webpage content fetch through the iFlow Search API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflow-ai](https://clawhub.ai/user/iflow-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search the web, search images, and fetch cleaned webpage content for current-information research and summarization workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, image queries, fetched URLs, and API-key-backed requests are sent to the external iFlow service. <br>
Mitigation: Avoid submitting secrets, private document links, localhost URLs, or internal-only URLs. <br>
Risk: The skill requires IFLOW_API_KEY, which can be exposed if stored or shared carelessly. <br>
Mitigation: Store IFLOW_API_KEY in a secret manager or temporary shell environment and do not commit it to files. <br>


## Reference(s): <br>
- [iFlow Search Skill Homepage](https://github.com/iflow-ai/iflow-skills/tree/main/skills/iflow-search) <br>
- [iFlow API Key Setup](https://platform.iflow.cn/profile?tab=apiKey) <br>
- [iFlow Platform](https://platform.iflow.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON responses from the iFlow Search API scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IFLOW_API_KEY and network access to the iFlow platform.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
