## Description: <br>
Structured memory system for AI agents using Notion. Use when setting up agent memory, discussing memory persistence, or helping agents remember context across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vladchatware](https://clawhub.ai/user/vladchatware) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up file-based and optional Notion-backed memory workflows so agents can preserve working context, decisions, lessons, and handoff notes across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent memory files or Notion pages could capture raw passwords, API keys, tokens, recovery codes, or session details. <br>
Mitigation: Store only references to a password manager or secret vault, and review memory templates before deployment. <br>
Risk: A Notion integration with broad access could expose more workspace data than the agent needs. <br>
Mitigation: Use a dedicated low-privilege Notion integration shared only with the specific pages or databases required. <br>
Risk: Heartbeat, email/calendar checks, and cron-style monitoring can create ongoing background behavior without clear user expectations. <br>
Mitigation: Treat those features as opt-in, define explicit scope, review schedules, and document how to disable them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vladchatware/notion-agent-memory) <br>
- [Continuity Cycle](references/continuity-cycle.md) <br>
- [Notion Integration Guide](references/notion-integration.md) <br>
- [ACT Framework](references/act-framework.md) <br>
- [Notion integrations](https://www.notion.so/my-integrations) <br>
- [Shop Vlad Chat](https://shop.vlad.chat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands] <br>
**Output Format:** [Markdown guidance with template files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces memory templates, setup steps, Notion API examples, and operating routines for agents.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
