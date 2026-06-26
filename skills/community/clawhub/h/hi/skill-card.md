## Description: <br>
Tsz captures agent learnings, errors, and corrections, while the artifact also includes OpenClaw hook guidance and FreeRide/OpenRouter configuration utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roman181](https://clawhub.ai/user/roman181) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users can use this release to record corrections, command failures, feature requests, and reusable learning notes for coding agents. Because the package also contains configuration-changing OpenClaw and FreeRide assets, users should review the included files before enabling hooks or running scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package mixes several different skill purposes, including self-improvement logging, OpenClaw hooks, and FreeRide/OpenRouter configuration. <br>
Mitigation: Audit the artifact before installation and separate unrelated functionality before using it in a production agent workflow. <br>
Risk: Hook guidance can create broad or always-on agent reminders that users may not expect. <br>
Mitigation: Avoid global empty-matcher hooks unless explicitly intended, and enable hooks only in reviewed workspaces. <br>
Risk: Included scripts and guidance can change OpenClaw configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json and review the exact script or command before running it. <br>
Risk: FreeRide/OpenRouter behavior requires an API key and may affect model routing. <br>
Mitigation: Use a dedicated OPENROUTER_API_KEY and verify model and fallback settings before relying on the configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/roman181/hi) <br>
- [OpenClaw integration](references/openclaw-integration.md) <br>
- [Hooks setup](references/hooks-setup.md) <br>
- [Examples](references/examples.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, learning-log templates, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead users to create learning log files, enable hooks, or update OpenClaw configuration after review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
