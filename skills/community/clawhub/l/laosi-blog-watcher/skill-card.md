## Description: <br>
Blog Watcher monitors blog and website updates by checking RSS feeds or webpage changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to track public or trusted blogs, RSS feeds, and webpages for new posts or content changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs outbound requests to monitored feed or webpage URLs, which can expose private-network or sensitive internal endpoints if users add untrusted targets. <br>
Mitigation: Use it only with public or trusted URLs, and avoid localhost, private-network addresses, internal admin panels, cloud metadata endpoints, and other sensitive services unless intentionally monitored. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces update summaries with blog name, title, link, and publication or update status when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
