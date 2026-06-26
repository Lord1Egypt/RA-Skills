## Description: <br>
Jiajiaoy Morning coordinates Chinese-language morning and evening briefing workflows, including news, technology, finance, weather, wellness, language learning, and next-day fortune prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure scheduled Chinese-language daily briefings and generate prompts for morning modules and evening fortune updates. It is intended for personal notification workflows that save per-user settings and register scheduled OpenClaw jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes a real bundled user profile and defaults to that user ID in one script. <br>
Mitigation: Remove bundled user data before installation and require an explicit userId for each setup or execution. <br>
Risk: The skill registers persistent scheduled messages to personal communication channels. <br>
Mitigation: Confirm recipients, channels, schedule, timezone, and deletion process before registering cron jobs. <br>
Risk: The workflow depends on 11 other ClawHub skills that can affect the generated briefing content. <br>
Mitigation: Inspect and approve each dependency skill before enabling scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cosmofang/jiajiaoy-morning) <br>
- [Publisher profile](https://clawhub.ai/user/cosmofang) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON arrays, Markdown prompts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18 and 11 dependent ClawHub skills; scheduled outputs are sent to configured Telegram or Feishu recipients.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
