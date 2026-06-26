## Description: <br>
Provides MiniMax-backed web search, image understanding, and image generation tools for agents using a configured MINIMAX_API_KEY. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yongjie666888](https://clawhub.ai/user/yongjie666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to call MiniMax services for web search, image analysis, and image generation from an OpenClaw-compatible JavaScript tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes unsafe credential guidance with a token-like example. <br>
Mitigation: Do not copy or use the embedded token-like value; configure only your own credential through a secure secret path. <br>
Risk: Prompts, search queries, image URLs, and local image contents may be sent to MiniMax APIs. <br>
Mitigation: Submit only data you are authorized and comfortable sending to MiniMax, and avoid sensitive or regulated content unless approved for the use case. <br>
Risk: Documentation describes speech and video features that are not exposed by the current JavaScript tool interface. <br>
Mitigation: Expect this release to provide web search, image understanding, and image generation unless the artifact is updated and rescanned. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yongjie666888/minimax-coding-plan-tool-yongjie) <br>
- [Publisher profile](https://clawhub.ai/user/yongjie666888) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from JavaScript CLI tools with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and MINIMAX_API_KEY; image understanding can send local image contents or URLs to the MiniMax API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
