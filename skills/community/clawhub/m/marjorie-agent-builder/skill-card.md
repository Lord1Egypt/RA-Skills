## Description: <br>
Build high-performing OpenClaw agents end-to-end. Use when you want to design a new agent (persona + operating rules) and generate the required OpenClaw workspace files (SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md + memory/YYYY-MM-DD.md). Also use to iterate on an existing agent's behavior, guardrails, autonomy model, heartbeat plan, and skill roster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and advanced OpenClaw users use this skill to design new agent workspaces, generate the core OpenClaw instruction files, and refine existing agent behavior, guardrails, autonomy, heartbeat behavior, and skill rosters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated agent workspace files may encode unsafe autonomy, outbound messaging, heartbeat, or memory behavior if accepted without review. <br>
Mitigation: Review generated files before use, especially MEMORY.md and HEARTBEAT.md, and only enable external APIs, outbound messaging, or high-autonomy behavior after explicit approval. <br>
Risk: Workspace files may accidentally include secrets, credentials, or sensitive session information. <br>
Mitigation: Keep secrets out of the workspace and avoid storing credentials, OAuth tokens, API keys, or session transcripts in generated files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/marjoriebroad/marjorie-agent-builder) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>
- [OpenClaw agent workspace](references/openclaw-workspace.md) <br>
- [OpenClaw agent file templates](references/templates.md) <br>
- [Agent Architecture Patterns](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown instructions and generated OpenClaw workspace file content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or generate SOUL.md, IDENTITY.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, daily memory notes, TOOLS.md, targeted diffs, and acceptance-test prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
