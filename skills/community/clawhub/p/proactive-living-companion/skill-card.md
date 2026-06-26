## Description: <br>
Proaktiv monitors user interests and daily patterns to send timely Telegram briefings, reminders, and topic pings through OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wewillsee86](https://clawhub.ai/user/wewillsee86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users install this companion to schedule proactive Telegram updates, learn interest preferences, and follow up on goals, commitments, and daily briefings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can make persistent OpenClaw changes, including a 30-minute cron job, routing rules in SOUL.md, and tools.profile configuration. <br>
Mitigation: Back up SOUL.md, review the installer before running it, and confirm that the cron schedule and tools.profile setting are acceptable. <br>
Risk: Telegram pings depend on the configured chat ID and may send autonomous messages to that destination. <br>
Mitigation: Verify OPENCLAW_TELEGRAM_NR before activation and inspect or remove the PROAKTIV cron entry if recurring pings are not wanted. <br>
Risk: The skill stores personal preferences, goals, commitments, and social facts in local state files, including silently collected social context. <br>
Mitigation: Review, edit, or disable the social-memory behavior and periodically inspect or delete proaktiv_state.json, interest_graph.json, interests.yaml, and social_knowledge.json. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wewillsee86/proactive-living-companion) <br>
- [Artifact README](artifact/README.md) <br>
- [Dispatcher Skill Definition](artifact/SKILL.md) <br>
- [Topic Templates](artifact/TOPIC_TEMPLATES.md) <br>
- [Social Knowledge Rules](artifact/SOCIAL.md) <br>
- [ClawHub Manifest](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Telegram-ready plain text and Markdown with occasional shell commands and JSON or YAML configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs through scheduled OpenClaw triggers and can update local JSON or YAML state files.] <br>

## Skill Version(s): <br>
1.0.52 (source: server release evidence and root SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
