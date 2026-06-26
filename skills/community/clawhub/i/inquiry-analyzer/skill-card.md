## Description: <br>
Analyzes Alibaba International inquiry data for a selected time window, extracts product category, customer, country, and status fields, and generates structured reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[likem90is-cmd](https://clawhub.ai/user/likem90is-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and business users use this skill to analyze Alibaba inquiries, run OKKI background checks for selected inquiries, and merge outputs into Markdown and CSV reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Alibaba browser session and can write sensitive customer, inquiry, chat, and background-check data to local report directories. <br>
Mitigation: Run it only with an authorized Alibaba account on a trusted machine, review generated outputs for sensitive data, and delete reports, chats, OKKI reports, and debug dumps when no longer needed. <br>
Risk: The skill can trigger OKKI background checks without strong scoping controls. <br>
Mitigation: Use explicit inquiry identifiers and time windows, confirm the intended account and scope before execution, and review generated OKKI outputs before use. <br>
Risk: External INQUIRY_ANALYZER_PATH overrides can redirect execution outside the self-contained skill directory. <br>
Mitigation: Prefer the bundled self-contained artifact path and use INQUIRY_ANALYZER_PATH only when the target directory is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/likem90is-cmd/inquiry-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CSV report files with supporting chat text outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and an authenticated OpenClaw browser session connected to Alibaba.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
