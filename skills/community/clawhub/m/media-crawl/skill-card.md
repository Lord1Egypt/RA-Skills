## Description:

media-crawler-local helps agents collect Bilibili, Douyin, YouTube, and Zhihu content through a locally running media-agent-crawler HTTP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sansan-mei](https://clawhub.ai/user/sansan-mei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill when they have the local media-agent-crawler application running and need an agent to start media crawls, list archived crawl tasks, or read task data for supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crawl targets, keywords, task IDs, optional platform cookies, and MCP arguments can be sent to the configured media-crawler service endpoint.

Mitigation: Keep BIL_CRAWL_URL pointed at a trusted localhost endpoint unless a remote HTTPS service is deliberately trusted.

Risk: Browser cookies may be exposed through shell history or to an endpoint the user does not control.

Mitigation: Avoid passing browser cookies through command-line arguments and only provide cookies to endpoints under the user's control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sansan-mei/skills/media-crawl)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell, PowerShell, JavaScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, crawl status, archive listings, selected task data, and troubleshooting guidance.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
