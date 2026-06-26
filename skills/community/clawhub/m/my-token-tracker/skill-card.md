## Description: <br>
Tracks token usage and estimated model costs, with daily or weekly reports and threshold alerts for OpenClaw sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mr-Lucky](https://clawhub.ai/user/Mr-Lucky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect current token consumption, estimate model costs, generate periodic usage reports, and receive threshold alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional hook may persist more session context than is needed for token accounting. <br>
Mitigation: Review the hook before enabling it and remove or disable the full context log in hooks/token-logger/handler.js. <br>
Risk: Scheduled Telegram reports and threshold alerts may expose ongoing local usage history. <br>
Mitigation: Enable scheduled reports only when the configured delivery channel is acceptable for usage and cost information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mr-Lucky/my-token-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/Mr-Lucky) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON usage records and report token totals, estimated cost, and threshold status.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
