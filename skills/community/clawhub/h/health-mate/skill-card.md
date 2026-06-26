## Description: <br>
Executable OpenClaw health-report skill with Chinese, English, and Japanese report flows. It reads Markdown logs only from an explicitly configured MEMORY_DIR, writes reports and logs locally, can create a commented project-local config/.env template during setup, sanitizes local-LLM stdout before AI commentary is embedded into reports, separates monthly disease mode from balanced/fat-loss lifestyle mode, and only performs Tavily, webhook, or font-download network activity when the corresponding runtime options are configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tankeito](https://clawhub.ai/user/tankeito) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use Health Mate to turn structured local health logs into localized daily, weekly, and monthly PDF health reports with scoring, trend charts, reminders, and optional delivery integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted report text can become local Python code in scheduled shell-runner delivery flows. <br>
Mitigation: Avoid scheduled shell-runner delivery until the heredoc interpolation issue is fixed, and review generated report text before enabling automated delivery. <br>
Risk: Sensitive health data may be read from MEMORY_DIR and written into local reports, logs, web-published directories, or external webhook messages. <br>
Mitigation: Keep MEMORY_DIR narrowly scoped, keep config/.env private, and leave web publishing and webhook settings unset unless those flows are intentional. <br>
Risk: Optional external services can transmit health-report content when configured. <br>
Mitigation: Set Tavily, webhook, REPORT_WEB_DIR, REPORT_BASE_URL, and runtime font-download settings only after reviewing the intended data flow. <br>


## Reference(s): <br>
- [ClawHub Health Mate listing](https://clawhub.ai/tankeito/health-mate) <br>
- [Project homepage](https://github.com/tankeito/Health-Mate) <br>
- [User configuration example](artifact/config/user_config.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and executable local report files, including PDF reports and optional delivery messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads configured local Markdown health logs, writes reports and logs locally, and uses optional network integrations only when configured.] <br>

## Skill Version(s): <br>
1.5.4 (source: server evidence, SKILL.md frontmatter, artifact metadata, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
