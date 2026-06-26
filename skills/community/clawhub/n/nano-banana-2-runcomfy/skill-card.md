## Description: <br>
Nano Banana 2 on RunComfy helps agents prepare and run text-to-image generation requests through the RunComfy CLI for drafts, batch variants, typography-focused images, and optional web-grounded prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate still images with RunComfy's hosted Nano Banana 2 text-to-image endpoint. It is suited for marketing drafts, social thumbnails, batch ideation, reproducible variants, quoted in-image text, and prompts that optionally need web-grounded context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunComfy credentials are required for normal use. <br>
Mitigation: Keep RUNCOMFY_TOKEN and ~/.config/runcomfy credentials private, rotate exposed tokens, and avoid logging token values. <br>
Risk: Prompts and web-grounded context may be sent to RunComfy. <br>
Mitigation: Do not include private, regulated, or sensitive content in prompts unless the user has approved sending that material to RunComfy. <br>
Risk: Web-grounded generation can add latency and cost. <br>
Mitigation: Enable web search only when the prompt requires current events or real-entity context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/nano-banana-2-runcomfy) <br>
- [Kalvin ClawHub profile](https://clawhub.ai/user/kalvinrv) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy) <br>
- [Nano Banana 2 model page](https://www.runcomfy.com/models/google/nano-banana-2?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=nano-banana-2-runcomfy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The agent produces RunComfy command guidance and configuration steps; RunComfy produces image files outside the skill card context.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
