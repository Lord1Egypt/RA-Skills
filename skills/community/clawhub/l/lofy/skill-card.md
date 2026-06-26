## Description: <br>
Personal AI chief of staff - a complete life management system for OpenClaw with proactive briefings, reviews, fitness tracking, career management, project tracking, smart home control, and brain-inspired memory architecture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrey401](https://clawhub.ai/user/harrey401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users use this skill to set up a personalized chief-of-staff style agent that manages goals, routines, memory, reminders, projects, fitness, career workflows, and optional home automation through natural conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The assistant template can receive standing access to sensitive personal files, calendar, email, messaging, memory, and workspace data. <br>
Mitigation: Use a dedicated workspace, avoid storing secrets in memory files, keep shared-chat memory loading disabled, and limit connected service credentials to the minimum needed scope. <br>
Risk: Scheduled heartbeat and cron workflows can create proactive monitoring or outreach that may surprise users if enabled without review. <br>
Mitigation: Review and narrow AGENTS.md and HEARTBEAT.md before enabling schedules, confirm every cron job, and require user confirmation before external messaging or smart-home actions. <br>
Risk: Memory files can accumulate sensitive personal facts and may be updated by the agent over time. <br>
Mitigation: Review MEMORY.md and daily logs regularly, keep the long-term memory concise, and remove outdated or sensitive entries. <br>


## Reference(s): <br>
- [Lofy ClawHub release page](https://clawhub.ai/harrey401/lofy) <br>
- [harrey401 publisher profile](https://clawhub.ai/user/harrey401) <br>
- [Memory System](references/memory-system.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown instructions with template files and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes workspace templates for agent identity, behavior, user profile, memory, scheduling, tools, goals, fitness, applications, projects, and home configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
