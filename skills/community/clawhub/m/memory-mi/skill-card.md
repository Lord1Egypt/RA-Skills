## Description: <br>
memory-mi provides an agent memory framework for automatically retrieving and saving user conversation history, preferences, and continuity context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nikol-coder](https://clawhub.ai/user/Nikol-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent, user-scoped memory retrieval and asynchronous memory saving to OpenClaw conversations. It is intended for agents that need continuity across turns and sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically capture and save user-linked conversation content. <br>
Mitigation: Make memory capture opt-in, avoid saving full raw transcripts by default, and provide retention and deletion controls. <br>
Risk: Memory search and save scripts send user-linked content to an external API destination. <br>
Mitigation: Verify the API destination and token handling before use, and only run the skill where that data sharing is acceptable. <br>
Risk: The background daemon stores queued conversation data in persistent plaintext files and logs. <br>
Mitigation: Run the daemon only in trusted environments and review queue and log storage permissions, retention, and cleanup. <br>
Risk: The installer can replace workspace-level AGENTS.md, SOUL.md, and start.sh files. <br>
Mitigation: Review changes before installation, keep backups, and remove or narrow global instruction replacement when not required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nikol-coder/memory-mi) <br>
- [Publisher profile](https://clawhub.ai/user/Nikol-coder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory retrieval results, queue status messages, daemon status output, and installation or configuration instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
