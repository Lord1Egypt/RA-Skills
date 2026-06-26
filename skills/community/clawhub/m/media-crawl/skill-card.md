## Description: <br>
Connects an agent to a user-run local media-agent-crawler HTTP service to collect and inspect Bilibili, Douyin, YouTube, and Zhihu content without requiring MCP client setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sansan-mei](https://clawhub.ai/user/sansan-mei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users with the local media-agent-crawler service running use this skill to start platform crawls, query archived crawl tasks, and read task data through REST or MCP-style HTTP calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use platform cookies that should be treated as account secrets. <br>
Mitigation: Provide cookies only when intentionally needed, keep them scoped to the trusted local crawler service, and avoid sharing them in prompts or logs. <br>
Risk: Changing the crawler service URL away from localhost could send requests or secrets to an unintended service. <br>
Mitigation: Keep BIL_CRAWL_URL set to localhost or 127.0.0.1 unless the user has explicitly verified and trusts the destination. <br>
Risk: The generic MCP helper can call named tools exposed by the local service. <br>
Mitigation: Use the generic helper only for the documented crawler, archive listing, and task data tools. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sansan-mei/media-crawl) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, PowerShell, JavaScript, JSON, and HTTP request examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Helper scripts and command examples call a local REST/MCP service and typically return JSON or plain text responses.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
