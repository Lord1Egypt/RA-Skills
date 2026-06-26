## Description: <br>
Generates Excel reports for Chinese government procurement opportunities and sends them by SMTP email for the govb workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpengle](https://clawhub.ai/user/zhangpengle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations teams tracking Chinese government procurement opportunities use this skill to fetch daily or date-specific bidding data, filter by keywords, generate an Excel workbook, and email the report to configured recipients. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends real procurement-report emails with attachments. <br>
Mitigation: Verify EMAIL_TO and EMAIL_CC before each production run and use the --to option for test delivery. <br>
Risk: SMTP credentials are required for email delivery. <br>
Mitigation: Use a dedicated SMTP account or app password and store the .env file only in trusted locations. <br>
Risk: A .env file in the current working directory can override the expected mail settings. <br>
Mitigation: Run the skill from a trusted directory and review the active .env values before sending reports. <br>
Risk: The full workflow depends on the separate govb-fetcher package. <br>
Mitigation: Review and install the govb-fetcher dependency before relying on generated reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpengle/goverment-bidding-email) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can trigger real SMTP email delivery with an Excel attachment when configured and executed.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
