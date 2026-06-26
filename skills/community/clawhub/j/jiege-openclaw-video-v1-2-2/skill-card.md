## Description: <br>
Generate high-quality Veo videos from natural language prompts with automatic task handling and browser preview. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangshenghzj888-stack](https://clawhub.ai/user/liangshenghzj888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users can trigger Veo video generation from a natural language chat prompt. The skill submits the prompt to a third-party video service in the background and opens the returned result link in a browser. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts a local background Python process that sends the user prompt and an OpenClaw API key to a third-party service. <br>
Mitigation: Use a dedicated low-privilege API key and avoid entering sensitive prompts. <br>
Risk: The skill automatically opens returned links in the system browser. <br>
Mitigation: Review or disable the auto-open behavior before deployment where untrusted links are not acceptable. <br>
Risk: Background task and lock-file behavior can leave generation blocked after an interrupted run. <br>
Mitigation: Review the local log and lock file state during troubleshooting before retrying generation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liangshenghzj888-stack/jiege-openclaw-video-v1-2-2) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill description](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and short chat replies with background process behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts are submitted to a third-party Veo-compatible API; successful results are opened as browser links.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata; artifact manifest reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
