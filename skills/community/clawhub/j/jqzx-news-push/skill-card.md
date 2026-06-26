## Description: <br>
Automates daily technology news delivery by fetching the latest Machine Heart hot list, sending it to Feishu, and saving it to Get Note. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bqcldz](https://clawhub.ai/user/bqcldz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure an automated daily workflow that retrieves technology news, sends it to a Feishu recipient or group, and saves a copy in Get Note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles service credentials for Machine Heart, Get Note, and Feishu. <br>
Mitigation: Use masked or presence-only checks for credentials, avoid printing secrets in terminal output or logs, and store credentials only in the user's controlled environment. <br>
Risk: The skill can configure a recurring scheduled job that sends Feishu messages and creates Get Note entries. <br>
Mitigation: Before enabling cron, verify the script path, target recipient, log location, schedule, and removal process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bqcldz/jqzx-news-push) <br>
- [Machine Heart MCP/RSS service](https://mcp.applications.jiqizhixin.com/) <br>
- [Get Note OpenAPI](https://www.biji.com/openapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided service credentials and may configure a recurring cron job.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
