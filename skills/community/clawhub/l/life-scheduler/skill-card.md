## Description: <br>
Life Scheduler helps an AI agent maintain fictional daily state by generating outfits, schedules, mood, and current-period context for persona, companion, roleplay, or virtual-idol use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[t-chen-cn](https://clawhub.ai/user/t-chen-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to give a persona or companion agent continuity across conversations by generating a daily fictional life state, writing it to HEARTBEAT.md, and optionally updating creative pools and schedule settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inject fictional daily state into future conversations, which may make roleplay continuity feel factual or persistent. <br>
Mitigation: Use it only for intended persona or companion agents, and review whether HEARTBEAT.md should be included in every conversation. <br>
Risk: Schedule generation may reference recent chats and retain life-history archives longer than desired. <br>
Mitigation: Review reference_recent_chats, archive settings, and memory/life-history retention before deployment. <br>
Risk: Automatic cron jobs can refresh agent state on a daily schedule and at period updates. <br>
Mitigation: Review the configured cron times and disable or adjust automatic generation where continuous state updates are not appropriate. <br>


## Reference(s): <br>
- [Life Scheduler ClawHub listing](https://clawhub.ai/t-chen-cn/life-scheduler) <br>
- [Configuration reference](references/CONFIGURATION.md) <br>
- [Persona configuration examples](references/EXAMPLES.md) <br>
- [AstrBot life scheduler inspiration](https://github.com/muyouzhi6/astrbot_plugin_life_scheduler) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown daily-state content with JSON configuration updates and natural-language guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update HEARTBEAT.md, config/life-scheduler.json, and memory/life-history archives; daily generation is documented at about 1500 tokens.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
