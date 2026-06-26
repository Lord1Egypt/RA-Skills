## Description: <br>
Meta-agent skill for decomposing complex tasks, coordinating autonomous sub-agents, and consolidating their outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to break large work into sub-agent tasks, define file-based handoffs, monitor completion, and merge deliverables. It is most useful for complex research, coding, analysis, writing, review, and integration workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and manage local agent workspaces that may contain task inputs, intermediate files, and generated outputs. <br>
Mitigation: Run it in a dedicated workspace, review generated files before cleanup or archive, and avoid placing sensitive local data in agent inboxes unless the task requires it. <br>
Risk: Sub-agents may send task content, scraped pages, or local data to SkillBoss using SKILLBOSS_API_KEY. <br>
Mitigation: Require explicit approval before external API calls, scope the API key for the intended use, and avoid sending confidential inputs to third-party services. <br>
Risk: The security scan verdict is suspicious because user-facing consent and scoping for third-party API use are not clear. <br>
Mitigation: Treat API-backed steps as opt-in, document what data will be sent, and review the orchestration plan before dispatching sub-agents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-agent-orchestrator) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>
- [File-Based Communication Protocol](artifact/references/communication-protocol.md) <br>
- [Sub-Agent Templates](artifact/references/sub-agent-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, JSON examples, and generated skill templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce task instructions, generated SKILL.md files, workspace layouts, status files, summaries, and API call examples.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
