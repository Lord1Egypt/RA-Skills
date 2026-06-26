## Description: <br>
Optimizer Openclaw Token helps OpenClaw users reduce token usage and API cost with context recommendations, model-routing guidance, heartbeat optimization, and local budget tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloud-dark](https://clawhub.ai/user/cloud-dark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using OpenClaw use this skill to reduce token and API costs by selecting smaller context bundles, routing prompts to lower-cost models, optimizing heartbeat checks, and tracking daily usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence ongoing agent behavior through model selection, heartbeat behavior, and generated workspace guidance. <br>
Mitigation: Review generated AGENTS.md and HEARTBEAT.md content before adopting it. <br>
Risk: Heartbeat setup may overwrite an existing OpenClaw workspace HEARTBEAT.md file. <br>
Mitigation: Back up the existing HEARTBEAT.md before installing the template. <br>
Risk: The RTK companion documentation includes a curl-to-shell installer path. <br>
Mitigation: Avoid that installer unless it has been separately verified; prefer a reviewed package-manager or source install path. <br>
Risk: Token budget tracking is advisory and may not enforce real spending limits without additional integration. <br>
Mitigation: Do not rely on token_tracker.py as hard budget enforcement. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cloud-dark/oot) <br>
- [Publisher profile](https://clawhub.ai/user/cloud-dark) <br>
- [Project homepage from Claw metadata](https://github.com/Cloud-Dark/oot) <br>
- [Provider strategy reference](references/PROVIDERS.md) <br>
- [RTK companion workflow reference](references/RTK.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local guidance files such as optimized AGENTS.md or HEARTBEAT.md drafts for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
