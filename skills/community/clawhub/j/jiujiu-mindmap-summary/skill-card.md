## Description: <br>
思维导图总结生成技能。根据传入的文本，生成json格式的思维导图； <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cx17030204-dotcom](https://clawhub.ai/user/cx17030204-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn input text into a simple_mind_map-compatible JSON mind-map summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release publishes a shared trial API key. <br>
Mitigation: Use a private scoped key instead of the published default key. <br>
Risk: The skill sends user text and an API key to an undocumented local backend. <br>
Mitigation: Install only when you control and trust the localhost:8000 backend, and avoid sensitive or regulated text until the backend owner, retention policy, and security model are clear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cx17030204-dotcom/jiujiu-mindmap-summary) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cx17030204-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown heading followed by pretty-printed JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and JIUJIUMINDMAP_API_KEY; posts input text to the configured local generation endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
