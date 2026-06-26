## Description: <br>
Helps configure model routing, fallback chains, routing strategy, and usage statistics for OpenClaw model providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zsdadad](https://clawhub.ai/user/Zsdadad) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure OpenClaw model chains, choose cost, speed, or quality routing strategies, and inspect local routing statistics. It is intended for teams managing multiple external model providers and fallback behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised automatic failover, cost monitoring, and API integration behavior may not match a user's OpenClaw setup without local validation. <br>
Mitigation: Test routing paths, failure cases, and cost reporting in the target environment before relying on the skill for production routing decisions. <br>
Risk: Multi-provider routing can send prompts or files to the selected external model provider. <br>
Mitigation: Review configured providers and data handling requirements before routing sensitive content. <br>
Risk: Configuration and reset commands can change local OpenClaw model router settings. <br>
Mitigation: Back up and review ~/.openclaw/model-router.json before and after using configuration or reset commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Zsdadad/model-router-manager) <br>
- [Project homepage from artifact metadata](https://github.com/myboxstorage/model-router-manager) <br>
- [Moltbook agent skills page](https://www.moltbook.com/m/agentskills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local OpenClaw configuration files and model provider names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
