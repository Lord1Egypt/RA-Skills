## Description: <br>
Manage Lemonade Servers natively. Use when checking system info, health status, listing available models, pulling or loading new models, completing LLM chats, or generating stable-diffusion images on a local or remote AI NPU/GPU cluster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-martinez](https://clawhub.ai/user/james-martinez) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect Lemonade server health, manage model lifecycle actions, and submit chat or image-generation requests to a selected local or remote Lemonade server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, model requests, and commands are sent to the configured Lemonade server URL. <br>
Mitigation: Use trusted server URLs, prefer HTTPS or a private network for remote hosts, and confirm the intended target before sending sensitive content. <br>
Risk: The optional LEMONADE_API_KEY can authenticate actions against a Lemonade server. <br>
Mitigation: Store the key in the environment, avoid exposing it in chat or logs, and rotate it if it may have been disclosed. <br>
Risk: Pulling, loading, or unloading large models can consume resources or disrupt active workloads. <br>
Mitigation: Check health and available VRAM first, and ask for confirmation before model download, load, or unload operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/james-martinez/lemonade-server-manager) <br>
- [Project homepage](https://github.com/james-martinez/lemonade-server-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl against a user-selected Lemonade server URL and optional LEMONADE_API_KEY authentication.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
