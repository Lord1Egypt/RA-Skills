## Description: <br>
Use mmx to generate text, images, video, speech, and music via the MiniMax AI platform. Use when the user wants to create media content, chat with MiniMax models, perform web search, or manage MiniMax API resources from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minimax-ai-dev](https://clawhub.ai/user/minimax-ai-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate the MiniMax mmx CLI for multimodal generation, search, vision understanding, quota checks, and API resource workflows from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on installing and running the external mmx-cli npm package. <br>
Mitigation: Verify the mmx-cli package before installation and pin a trusted version when reproducibility or supply-chain control matters. <br>
Risk: MiniMax API keys can be exposed through command lines, shell history, or local credential files. <br>
Mitigation: Prefer environment variables or a secure secret manager, protect ~/.mmx/credentials.json, and rotate any exposed key. <br>
Risk: Some commands send prompts, files, or generated-media requests to the MiniMax service and may consume quota or affect account resources. <br>
Mitigation: Only send content approved for MiniMax processing, review costly or account-changing actions, and avoid --yes unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minimax-ai-dev/minimax-multimodal) <br>
- [MiniMax publisher profile](https://clawhub.ai/user/minimax-ai-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference generated media files, URLs, task IDs, and JSON tool schemas through mmx commands.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
