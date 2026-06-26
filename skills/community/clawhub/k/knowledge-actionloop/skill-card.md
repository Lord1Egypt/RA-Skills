## Description: <br>
基于《实践论》的自我迭代系统，当需要自动整理记忆、反思改进、或创建新技能时使用，包含 Heartbeat 检查清单、Cron 定时任务配置和技能创建工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongchenga](https://clawhub.ai/user/kongchenga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to configure an agent workflow for persistent memory review, scheduled reflection, and repeated-pattern skill creation. It is intended for agents that should maintain and reorganize conversation-derived notes over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to persist and reorganize conversation-derived memory, which can retain sensitive information without enough user control. <br>
Mitigation: Before enabling it, define where memory files live, what information must never be saved, and how users can review, edit, or disable memory updates. <br>
Risk: Scheduled cleanup can delete or rewrite memory files automatically. <br>
Mitigation: Require reviewable change logs or backups for memory cleanup jobs, and keep destructive cron behavior disabled until the operator approves the policy. <br>


## Reference(s): <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub release page](https://clawhub.ai/kongchenga/knowledge-actionloop) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and checklist templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory-maintenance checklists, cron setup commands, and skill-creation workflow guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
