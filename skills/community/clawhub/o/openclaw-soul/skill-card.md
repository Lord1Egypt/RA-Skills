## Description: <br>
Openclaw Soul helps an OpenClaw agent bootstrap a self-evolving workspace with constitution, identity, heartbeat, memory, goals, optional governance skills, and guided personality setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kianzzz](https://clawhub.ai/user/kianzzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize an agent workspace with persistent memory, identity files, heartbeat behavior, goal tracking, and optional self-improvement and governance modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can set up persistent memory, scheduled work, OpenClaw configuration, and repository state changes. <br>
Mitigation: Review cron entries, systemPrompt files, OpenClaw config changes, transcript processing, and git auto-commit behavior before enabling the skill in a valuable workspace. <br>
Risk: Conversation-derived memory and transcript processing may retain sensitive user context. <br>
Mitigation: Use the skill only in a workspace where persistent memory is desired, and review or prune generated memory files regularly. <br>
Risk: API tokens or credentials pasted during setup may be stored in shell profiles or configuration files. <br>
Mitigation: Use scoped tokens, avoid pasting raw secrets unless needed, and remove any stored credentials that are not required. <br>
Risk: Optional integrations and visualizer behavior can broaden the runtime surface area. <br>
Mitigation: Disable the writable visualizer server and social or API integrations unless they are required for the deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kianzzz/openclaw-soul) <br>
- [README](artifact/README.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Bootstrap Guide](artifact/references/bootstrap-guide.md) <br>
- [Heartbeat Template](artifact/references/heartbeat-template.md) <br>
- [Memory Architecture Template](artifact/references/memory-architecture-template.md) <br>
- [EvoClaw Source API Reference](artifact/fallback/evoclaw/references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, workspace file templates, configuration snippets, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update OpenClaw workspace files, memory directories, scheduled heartbeat tasks, git commits, and local configuration when executed by an agent.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
