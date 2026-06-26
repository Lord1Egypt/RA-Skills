## Description: <br>
PostQube Threads Publisher helps an agent draft, confirm, publish, and monitor Threads posts or chained threads through the PostQube REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanfahmi11](https://clawhub.ai/user/wanfahmi11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to publish single Threads posts, create chained threads, check post status and history, and monitor PostQube API usage after reviewing and confirming the drafted content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a PostQube API key and can publish visible social media content. <br>
Mitigation: Use a dedicated or limited API key where possible, keep POSTQUBE_API_KEY out of post content and logs, and review every drafted post before confirming an API call. <br>
Risk: The skill depends on the external postqube.quickbitsoftware.com service. <br>
Mitigation: Install only if the user trusts PostQube and accepts that post publishing, status checks, history, and quota reporting depend on that service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanfahmi11/postqube-threads-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/wanfahmi11) <br>
- [PostQube dashboard](https://postqube.quickbitsoftware.com/dashboard) <br>
- [PostQube API base](https://postqube.quickbitsoftware.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTQUBE_API_KEY and curl on darwin or linux; posts should be confirmed by the user before API calls are made.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata; artifact frontmatter lists 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
