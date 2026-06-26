## Description: <br>
Uses the MiniMax Coding Plan API to help agents search the web for current information and analyze image content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[L1-M1ng](https://clawhub.ai/user/L1-M1ng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when they need current web search results, research support, or image descriptions through MiniMax. It is intended for cases where sending the query or image content to MiniMax is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries, URLs, and image contents may be sent to MiniMax for processing. <br>
Mitigation: Use the skill only with content that is appropriate to share with MiniMax; avoid private screenshots, documents, photos, and sensitive URLs. <br>
Risk: The skill depends on a local MiniMax API key stored in a shell-readable configuration file. <br>
Mitigation: Use a dedicated API key where possible, store it outside the skill artifact, keep the file permission restricted, and avoid printing the key in logs or command output. <br>
Risk: Search and VLM API usage may be rate-limited or incur external service costs. <br>
Mitigation: Avoid bulk or repeated calls unless the user has confirmed the intended usage and account limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/L1-M1ng/minimax-search-vlm) <br>
- [MiniMax developer platform](https://platform.minimaxi.com) <br>
- [MiniMax Coding Plan search endpoint](https://api.minimaxi.com/v1/coding_plan/search) <br>
- [MiniMax Coding Plan VLM endpoint](https://api.minimaxi.com/v1/coding_plan/vlm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and a user-provided MINIMAX_API_KEY; image analysis supports JPEG, PNG, GIF, and WebP files up to 20MB according to the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
