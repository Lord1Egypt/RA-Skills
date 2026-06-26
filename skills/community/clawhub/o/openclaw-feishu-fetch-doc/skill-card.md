## Description: <br>
Fetches user-provided Feishu/Lark cloud document content as Markdown and explains how to handle embedded images, files, and whiteboards with companion Feishu tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenfa188](https://clawhub.ai/user/chenfa188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to read Feishu/Lark document or wiki URLs they provide, retrieve Markdown content, and route media or non-document wiki objects to the appropriate Feishu tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose content from Feishu/Lark document tokens or URLs provided to the agent. <br>
Mitigation: Use a Feishu account with appropriate access limits and review requested document tokens or URLs before fetching. <br>
Risk: Embedded images, files, whiteboards, sheets, or bitables may trigger additional access or download actions through companion tools. <br>
Mitigation: Explicitly approve attachment or media downloads and any sheet or bitable operations before execution. <br>
Risk: Wiki links may resolve to object types other than cloud documents. <br>
Mitigation: Resolve the wiki node type first and call the matching Feishu tool only after confirming the returned object type. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenfa188/openclaw-feishu-fetch-doc) <br>
- [Publisher profile](https://clawhub.ai/user/chenfa188) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown document content with structured guidance for related Feishu tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Media objects are represented by tokens that require explicit companion-tool downloads when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
