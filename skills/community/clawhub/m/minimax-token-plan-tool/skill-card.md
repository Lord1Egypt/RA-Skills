## Description: <br>
A lightweight MiniMax Token Plan Tool skill that directly calls official MCP APIs using pure JavaScript, without external MCP servers or subprocess invocation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yorch233](https://clawhub.ai/user/yorch233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to access MiniMax Token Plan web search, image understanding, and token plan quota checks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries, prompts, quota requests, and selected images are sent to MiniMax APIs. <br>
Mitigation: Install only when this data sharing is acceptable, and avoid confidential, private, or regulated images. <br>
Risk: A misconfigured API host could send requests to an unsupported endpoint. <br>
Mitigation: Use only the documented MiniMax hosts: https://api.minimaxi.com or https://api.minimax.io. <br>
Risk: Local image inputs are converted and transmitted to MiniMax for analysis. <br>
Mitigation: Review image content before use and do not submit sensitive local files. <br>


## Reference(s): <br>
- [MiniMax Token Plan Tool on ClawHub](https://clawhub.ai/yorch233/minimax-token-plan-tool) <br>
- [MiniMax Token Plan Subscription - China Mainland](https://platform.minimaxi.com/subscribe/token-plan) <br>
- [MiniMax Token Plan Subscription - Global](https://platform.minimax.io/subscribe/token-plan) <br>
- [MiniMax Coding Plan MCP](https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP/) <br>
- [Minimax Multimodal Toolkit on ClawHub](https://clawhub.ai/minimax-ai-dev/minimax-multimodal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, MINIMAX_API_KEY, and a supported MINIMAX_API_HOST.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
