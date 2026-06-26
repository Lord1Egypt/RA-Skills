## Description: <br>
Design and generate complete OpenClaw agent workspaces with personas, operating rules, memory files, heartbeat plans, guardrails, and acceptance-test prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill to design new agents, generate the core workspace files, and refine an existing agent's guardrails, autonomy model, heartbeat behavior, and skill roster. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated AGENTS.md, HEARTBEAT.md, and MEMORY.md files can influence future agent behavior. <br>
Mitigation: Review those files before use and confirm that guardrails, memory rules, and heartbeat behavior match the intended operating model. <br>
Risk: Secrets, credentials, or session transcripts may be exposed if a user places them in the generated workspace. <br>
Mitigation: Keep credentials, OAuth tokens, API keys, and session transcripts outside the workspace and out of generated memory files. <br>
Risk: High-autonomy and heartbeat behavior can increase operational risk if enabled before guardrails are checked. <br>
Mitigation: Use high autonomy or heartbeat tasks only after confirming ask-before-destructive and ask-before-outbound-message rules. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/godfery-agent-builder) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [OpenClaw agent workspace](references/openclaw-workspace.md) <br>
- [OpenClaw agent file templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated OpenClaw workspace file content, targeted diffs, checklists, and scenario prompts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate or revise SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, memory logs, and TOOLS.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
