## Description: <br>
Fetches and analyzes Amazon product reviews by ASIN across 15 Amazon marketplaces, with filters for star rating, marketplace, recency or helpfulness, verified purchase status, keywords, and media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and e-commerce operators use this skill to retrieve Amazon customer reviews for a single ASIN, filter by marketplace and review attributes, and summarize customer feedback into product, competitor, and improvement insights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Amazon review queries and the LINKFOXAGENT_API_KEY authorization value to LinkFox endpoints. <br>
Mitigation: Install and use it only when sharing those queries and credentials with LinkFox is acceptable, and scope or rotate the API key according to local policy. <br>
Risk: The security review states that the skill instructs the agent to send interaction feedback to a separate LinkFox endpoint without asking first. <br>
Mitigation: Require explicit user or administrator approval before feedback submission, or disable that behavior where policy requires consent. <br>
Risk: Large review responses saved with response_io.py may contain PII, pricing, or auth-sensitive data and are not automatically deleted. <br>
Mitigation: Write response files outside git worktrees, avoid committing them, and delete them after the task is complete. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-amazon-reviews) <br>
- [API Reference](references/api.md) <br>
- [Amazon Reviews API Endpoint](https://tool-gateway.linkfox.com/amazon/reviews/list) <br>
- [LinkFox Skills](https://skill.linkfox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and review listings, with optional JSON API responses and shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can persist large API responses to local files for selective reading; persisted files are not automatically deleted.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
