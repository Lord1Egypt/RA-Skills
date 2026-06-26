## Description: <br>
OpenClaw system health audit and auto-repair skill for monitoring prompt size, cron compliance, session cleanup, and token consumption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfmoon82](https://clawhub.ai/user/halfmoon82) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to generate health reports, review runtime cost risks, configure recurring checks, and apply user-approved fixes for cron and session issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently schedule agent work through a recurring cron job. <br>
Mitigation: Disable the recurring cron job during initial setup unless recurring checks are required, then review the generated cron configuration before enabling it. <br>
Risk: The skill can change cron and session state. <br>
Mitigation: Run reports in dry-run mode first, back up `~/.openclaw/cron/jobs.json` and `session_model_state.json`, and review listed fixes before using `health fix all`. <br>
Risk: Telegram or Discord report delivery may expose runtime health details outside the local machine. <br>
Mitigation: Treat report delivery as an external data flow and send reports only to approved channels. <br>


## Reference(s): <br>
- [OpenClaw Health Audit on ClawHub](https://clawhub.ai/halfmoon82/openclaw-health-audit) <br>
- [halfmoon82 publisher profile](https://clawhub.ai/user/halfmoon82) <br>
- [Layer Audit Guide](references/layer-audit-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local reports, configuration files, cron job templates, and user-reviewed repair commands.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
