## Description: <br>
Health Report helps an agent configure personal health profiles, guide health data entry, generate scored health reports and PDFs, and optionally send reports through configured messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal health assistants use this skill to collect daily weight, diet, water, exercise, and symptom records, then produce health summaries, scoring details, PDFs, and follow-up guidance. It is intended for configured personal wellness reporting rather than clinical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive health records may be read from MEMORY_DIR and used in AI prompts, reports, logs, or generated PDFs. <br>
Mitigation: Use a dedicated MEMORY_DIR, keep report and log locations private, and review generated reports and logs for sensitive content. <br>
Risk: Configured Tavily, OpenClaw agent, DingTalk, Feishu, or Telegram paths may send health-related content to external services. <br>
Mitigation: Configure only the outbound channels that are required, verify recipients before use, and rotate webhook, bot, and API credentials regularly. <br>
Risk: Generated PDF URLs can expose private health reports if REPORT_BASE_URL or REPORT_WEB_DIR points to a public location. <br>
Mitigation: Avoid public report hosting for private PDFs and restrict access to any directory used for generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tankeito/openclaw-skill-health-report) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [user_config.example.json](artifact/config/user_config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, PDF files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text health report, generated PDF report, and command/configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local report files and optionally publish report links or messages through configured outbound channels.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
