## Description: <br>
Autonomous 24/7 affiliate content production pipeline for OpenClaw agents that orchestrates research, briefing, article writing, quality checks, and deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sonnenberglauramarie-afk](https://clawhub.ai/user/sonnenberglauramarie-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content operators and developers use this skill to run a multi-agent affiliate content workflow from keyword backlog through SEO article production, quality checks, and Cloudflare Workers or Pages deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish content, update sitemaps, deploy to Cloudflare, and purge cache on live sites. <br>
Mitigation: Use it only for sites where those actions are intended, and require an explicit staging or production confirmation before any live deployment. <br>
Risk: A Cloudflare API token used by the workflow could permit unintended changes if it is over-scoped or stored unsafely. <br>
Mitigation: Store the token in a secret manager or environment variable and scope it to the minimum zone and permissions needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/sonnenberglauramarie-afk/max-content-machine) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with workflow steps, file examples, shell commands, and configuration instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide an agent to create briefs, HTML articles, quality gate outputs, sitemap updates, Cloudflare deployment commands, and cache purge actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact metadata and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
