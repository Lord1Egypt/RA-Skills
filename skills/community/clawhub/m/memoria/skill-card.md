## Description: <br>
Memoria provides a structured local Markdown memory vault for AI agents with commands to store, recall, search, manage sessions, and optionally sync memories to Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kitakitsune0x](https://clawhub.ai/user/kitakitsune0x) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI-agent operators use Memoria to give agents a persistent local Markdown memory vault, retrieve prior context, manage wake/checkpoint/sleep handoffs, and optionally sync selected vault content with Notion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad proactive memory capture can store personal or sensitive information without a clear consent gate. <br>
Mitigation: Store only user-approved or task-necessary memories, avoid secrets and credentials, and review the vault regularly. <br>
Risk: Notion sync can transmit saved local memories to a third-party service. <br>
Mitigation: Disable or avoid auto-sync for sensitive content, use Notion sync only for intended vaults, and confirm the Notion workspace before pushing data. <br>
Risk: Persistent memory can retain stale or sensitive context longer than intended. <br>
Mitigation: Periodically audit, update, or delete vault entries and protect the vault path with appropriate local access controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kitakitsune0x/memoria) <br>
- [README](artifact/README.md) <br>
- [Usage Instructions](artifact/INSTRUCTIONS.md) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown vault files and, when configured, sync memory content to Notion.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release evidence; artifact package.json reports 0.1.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
