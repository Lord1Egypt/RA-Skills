## Description: <br>
Collects daily GitLab commits, merge requests, issues, and pipeline data, summarizes project activity, and can prepare confirmed Feishu report content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengxiansheng1](https://clawhub.ai/user/chengxiansheng1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and project managers use this skill to gather daily GitLab activity across configured repositories, review structured summaries, and publish confirmed updates to Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles private GitLab repository activity and credentials. <br>
Mitigation: Store config.json securely and use a least-privilege read-only GitLab token. <br>
Risk: TLS verification is disabled in the GitLab and Feishu HTTP client behavior. <br>
Mitigation: Fix or avoid disabled TLS verification before use, especially outside a trusted internal environment. <br>
Risk: Running without preview mode can post reports to configured Feishu webhooks. <br>
Mitigation: Use --preview unless posting is intentional, confirm webhook recipients, and enable cron, webhook, or CI automation only after explicit approval. <br>


## Reference(s): <br>
- [GitLab Daily Report reference README](references/README.md) <br>
- [ClawHub skill page](https://clawhub.ai/chengxiansheng1/gitlab-daily-report) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style reports, JSON data summaries, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports concise, detailed, and executive report styles; preview mode avoids Feishu posting.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
