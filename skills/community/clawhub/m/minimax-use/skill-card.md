## Description: <br>
MiniMax AI tools for web search, image analysis, LLM chat, and language translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnlangzi](https://clawhub.ai/user/cnlangzi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to call MiniMax services for web search, image understanding, chat, streaming chat, translation, and model listing from CLI commands or Python functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, chat history, translation text, and image contents can be sent to MiniMax or the endpoint configured in MINIMAX_API_HOST. <br>
Mitigation: Avoid sensitive or regulated data unless approved for that endpoint, and review inputs before sending them to the service. <br>
Risk: A custom MINIMAX_API_HOST can redirect requests and API-key-authenticated traffic to another service. <br>
Mitigation: Use only MiniMax or a trusted endpoint you control, and prefer a dedicated API key with spending limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnlangzi/minimax-use) <br>
- [MiniMax API reference](references/API.md) <br>
- [Available MiniMax models](assets/models.json) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>
- [MiniMax API key setup](https://platform.minimaxi.com/subscribe/coding-plan) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, configuration] <br>
**Output Format:** [JSON responses with text results, plus Markdown guidance with CLI and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY; optionally uses MINIMAX_API_HOST; streaming chat can return response chunks.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
