## Description: <br>
Automatically creates and maintains OpenClaw MEMORY.md long-term memory files with rule-based filtering, optional LLM analysis, and sensitive-data detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx0018](https://clawhub.ai/user/zx0018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to initialize a MEMORY.md file and optionally maintain it from daily session logs. It supports cron-driven updates that filter notable events, call a configured LLM provider when available, and flag possible sensitive content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Session logs may contain secrets or sensitive personal data that are retained in MEMORY.md or sent to the configured LLM provider. <br>
Mitigation: Use local rule mode by leaving provider API keys unset when privacy matters, review MEMORY.md and daily logs for sensitive content, and keep restrictive file permissions. <br>
Risk: Recurring cron updates can create ongoing retention beyond the user's expectations. <br>
Mitigation: Enable the cron job only after confirming the desired retention behavior, and audit or disable the OpenClaw cron job when automatic updates are no longer needed. <br>
Risk: API keys are read from environment variables and partial key values may be printed in command output. <br>
Mitigation: Avoid running the updater in shared terminals or log collectors, use provider-scoped credentials, and rotate credentials if exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zx0018/memory-manager-secure) <br>
- [Publisher Profile](https://clawhub.ai/user/zx0018) <br>
- [OpenClaw Cron Documentation](https://docs.openclaw.ai/cron) <br>
- [OpenClaw Sessions Documentation](https://docs.openclaw.ai/sessions) <br>
- [OpenClaw Memory Best Practices](https://docs.openclaw.ai/best-practices/memory) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, shell scripts, and inline command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update MEMORY.md and OpenClaw cron configuration when installed or run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
