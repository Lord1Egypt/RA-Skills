## Description: <br>
Adds cheap OpenRouter model aliases to an OpenClaw setup, advises when to switch models by task complexity, and estimates cost savings without changing the default model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffjhunter](https://clawhub.ai/user/jeffjhunter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to add OpenRouter model aliases, pick cost-focused presets, receive model-switching guidance, and estimate or track savings for agent work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add or remove OpenClaw model aliases and restart the OpenClaw gateway. <br>
Mitigation: Review each approval prompt, confirm the selected preset or alias before execution, and remove aliases that are no longer wanted. <br>
Risk: The skill uses the user's OpenRouter account and requires OpenRouter credentials through OpenClaw. <br>
Mitigation: Use OpenClaw's auth wizard instead of pasting API keys into chat, and monitor OpenRouter usage or billing after enabling aliases. <br>
Risk: The cost tracker keeps a local task and savings log under ~/.openclaw. <br>
Mitigation: Reset or delete the tracker if local task history should not be retained. <br>


## Reference(s): <br>
- [OpenClaw Cost Optimizer on ClawHub](https://clawhub.ai/jeffjhunter/openclaw-cost-optimizer) <br>
- [Publisher profile: jeffjhunter](https://clawhub.ai/user/jeffjhunter) <br>
- [Model reference](MODEL-REFERENCE.md) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [Jeff J Hunter](https://jeffjhunter.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and chat commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw, OPENROUTER_API_KEY, and user approval for OpenClaw alias, auth, and gateway commands; may write a local savings log under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
