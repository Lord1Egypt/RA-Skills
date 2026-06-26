## Description: <br>
Meta-agent skill for orchestrating complex tasks through autonomous sub-agents by decomposing tasks, creating sub-agent workspaces, coordinating file-based handoffs, and consolidating results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to split complex work into coordinated sub-agent tasks, define sub-agent roles, monitor progress through status files, and merge completed deliverables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sub-agents may send prompts, files, scraped content, or datasets to an external AI API when SkillBoss-backed capabilities are used. <br>
Mitigation: Use the skill in a dedicated workspace, avoid regulated or secret data, set SKILLBOSS_API_KEY only for sessions that need it, and review any generated sub-agent instructions before external API use. <br>
Risk: Generated sub-agent instructions and merged outputs may introduce incorrect, conflicting, or misleading results. <br>
Mitigation: Review generated sub-agent SKILL.md files, validate outbox deliverables against success criteria, and require human approval before relying on consolidated results. <br>


## Reference(s): <br>
- [File-Based Communication Protocol](references/communication-protocol.md) <br>
- [Sub-Agent Templates](references/sub-agent-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with bash, Python, JSON, and file-layout examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create sub-agent SKILL.md files, inbox/outbox directories, status.json files, and consolidated summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
