## Description: <br>
Postiz Litiao helps agents use the Postiz CLI to schedule, publish, upload media for, manage, and analyze social posts across 28+ connected channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI agents use this skill to configure the Postiz CLI, discover connected integrations and provider settings, create scheduled or draft social posts, upload media, manage posts, and review analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent publish, schedule, upload media, or delete content on live Postiz-connected social accounts. <br>
Mitigation: Use draft or test integrations first and require explicit confirmation before posting, scheduling, batch runs, uploads, or deletion. <br>
Risk: POSTIZ_API_KEY grants access to connected Postiz accounts and can leak through shell profiles, terminals, or logs. <br>
Mitigation: Store the key in a controlled secret store or tightly scoped environment file and avoid printing it in terminals or logs. <br>
Risk: Incorrect integration IDs, audience or privacy settings, content, media URLs, or scheduled dates can publish to the wrong destination or time. <br>
Mitigation: Verify account IDs, provider settings, content, media URLs, and ISO 8601 dates before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/litiao1224/postiz-litiao) <br>
- [Postiz API documentation](https://docs.postiz.com/public-api/introduction) <br>
- [Postiz npm package](https://www.npmjs.com/package/postiz) <br>
- [Postiz application repository](https://github.com/gitroomhq/postiz-app) <br>
- [Postiz website](https://postiz.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTIZ_API_KEY and may use POSTIZ_API_URL for custom API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
