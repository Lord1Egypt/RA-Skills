## Description: <br>
Enables AI agents with moods, intrusive thoughts, memory decay, trust learning, self-evolution, scheduled rituals, and a web dashboard for autonomous behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittleik](https://clawhub.ai/user/kittleik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to add mood-driven scheduling, prompt selection, memory, trust learning, and activity dashboards to an AI agent. It is suited for users who want configurable autonomous behavior while retaining review over prompts, schedules, integrations, and stored activity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad unattended agent authority can trigger code changes, tool installs, public posts, external messages, deletion, deployment, or system and network changes. <br>
Mitigation: Run the skill in a tightly constrained agent profile and require approval for file writes outside the skill data directory, code commits, package installs, public posts, external messages, deletion, deployment, and system or network changes. <br>
Risk: Scheduled autonomous activity may run before the user has reviewed prompts, presets, trust settings, and integrations. <br>
Mitigation: Do not enable cron jobs until thoughts.json, presets, trust settings, and integrations have been reviewed and adjusted. <br>
Risk: The web dashboard and local state can expose memory, journals, mood history, and activity logs. <br>
Mitigation: Bind the dashboard to localhost or add authentication, and treat stored memory, journals, mood history, and activity logs as private data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kittleik/intrusive-thoughts) <br>
- [Publisher profile](https://clawhub.ai/user/kittleik) <br>
- [GitHub homepage from skill metadata](https://github.com/kittleik/intrusive-thoughts) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [Public BBC News RSS feed](https://feeds.bbci.co.uk/news/world/rss.xml) <br>
- [Public Hacker News RSS feed](https://hnrss.org/frontpage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell command guidance for agent actions and local configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces user-editable prompts, local JSON state, scheduled-agent instructions, and dashboard guidance.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
