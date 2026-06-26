## Description: <br>
LinkedIn Community provides managed OAuth access for creating and managing LinkedIn organization pages, posts, comments, reactions, and analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect an agent to LinkedIn Community Management workflows through Maton, including organization lookup, post publishing, comment and reaction management, and page or share analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, edit, react to, comment on, or delete LinkedIn content through a connected account or organization. <br>
Mitigation: Require explicit user confirmation before write actions, including the target resource, intended content, and LinkedIn identity. <br>
Risk: Requests may use the wrong LinkedIn account or organization when multiple Maton connections are available. <br>
Mitigation: List available connections, verify the intended Maton connection and organization, and send the Maton-Connection header for requests. <br>
Risk: The skill depends on sensitive credentials and delegated OAuth permissions through Maton. <br>
Mitigation: Install only when comfortable using Maton as the gateway, protect MATON_API_KEY, and use the least-privileged LinkedIn connection available. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [LinkedIn Community Management Overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview) <br>
- [LinkedIn Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api) <br>
- [LinkedIn Comments API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api) <br>
- [LinkedIn Reactions API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/reactions-api) <br>
- [LinkedIn Organization Lookup API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-lookup-api) <br>
- [LinkedIn Follower Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/follower-statistics) <br>
- [LinkedIn Page Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/page-statistics) <br>
- [LinkedIn Share Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/share-statistics) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with curl, JavaScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, a Maton LinkedIn OAuth connection, LinkedIn API headers, and the correct Maton-Connection header when multiple connections exist.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
