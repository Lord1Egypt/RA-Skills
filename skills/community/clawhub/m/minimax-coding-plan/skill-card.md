## Description: <br>
MiniMax Coding Plan provides native web search and image understanding for OpenClaw when a user specifically wants MiniMax-native search or vision analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YJLi-new](https://clawhub.ai/user/YJLi-new) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to route web search and image-understanding requests through MiniMax when MiniMax-native processing is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search queries, prompts, images, URLs, and derived image data to the external MiniMax API. <br>
Mitigation: Use it only when external MiniMax processing is acceptable, and avoid sending private screenshots, documents, internal URLs, or confidential images. <br>
Risk: The wrapper relies on MiniMax credentials from environment variables or an OpenClaw OAuth profile. <br>
Mitigation: Verify that MINIMAX_API_KEY, MINIMAX_API_HOST, and the selected minimax-portal OAuth profile are intentional before running the skill. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/YJLi-new/minimax-coding-plan) <br>
- [MiniMax API host](https://api.minimaxi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [JSON responses and text guidance from MiniMax web search or image-understanding calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MiniMax API key or configured minimax-portal OAuth profile; image inputs may be local files, URLs, or data URLs.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
