## Description: <br>
Layered Memory manages large memory files with L0 summaries, L1 overviews, and L2 full content so agents can generate, search, and load memory with lower token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yingdadaa](https://clawhub.ai/user/yingdadaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain layered summaries of local memory files, search memory at lower token cost, and load full details only when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist conversation memory under the user's home directory, which may include sensitive content. <br>
Mitigation: Use it only in environments where local memory storage is acceptable, avoid saving secrets or credentials, and review retained memory files regularly. <br>
Risk: The bootstrap hook can inject reminders that steer the agent toward saving or loading memory. <br>
Mitigation: Review hook behavior before enabling it and prefer manual confirmation for memory-saving workflows until retention controls are tightened. <br>
Risk: The skill calls hardcoded ~/clawd/scripts paths through shell commands. <br>
Mitigation: Inspect the referenced scripts and use dry-run or manual commands before enabling automated generation, maintenance, or save workflows. <br>


## Reference(s): <br>
- [Layered Memory ClawHub release](https://clawhub.ai/yingdadaa/layered-memory) <br>
- [Integration Guide](INTEGRATION.md) <br>
- [Auto Trigger Guide](AUTO-TRIGGER.md) <br>
- [Anti-Duplicate Guide](ANTI-DUPLICATE.md) <br>
- [Auto Save Guide](AUTO-SAVE-GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory layer files under ~/clawd when commands are run.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata, package.json, changelog released 2026-03-13) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
