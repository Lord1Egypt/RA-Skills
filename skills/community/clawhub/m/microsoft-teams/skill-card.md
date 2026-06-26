## Description: <br>
Microsoft Teams API integration with managed OAuth for managing teams, channels, messages, meetings, recordings, and transcripts via Microsoft Graph API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to make Microsoft Teams requests through Maton's managed OAuth proxy, including listing teams and channels, sending channel or chat messages, scheduling meetings, and retrieving meeting recordings or transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Teams messages, chats, meetings, recordings, transcripts, and metadata are routed through Maton's OAuth proxy. <br>
Mitigation: Install only when Maton is trusted for the connected Teams account and the organization allows this data path. <br>
Risk: A leaked MATON_API_KEY or unintended OAuth connection selection could expose or change Teams resources in the connected account. <br>
Mitigation: Keep MATON_API_KEY private, specify the Maton-Connection header when multiple accounts exist, and revoke unused connections. <br>
Risk: Write-capable API calls can create, update, or delete Teams channels, messages, meetings, or connections. <br>
Mitigation: Require explicit user approval after checking the exact team, channel, message, meeting, or connection and the intended effect. <br>


## Reference(s): <br>
- [Microsoft Teams API Overview](https://learn.microsoft.com/en-us/graph/api/resources/teams-api-overview) <br>
- [Microsoft Graph API Reference](https://learn.microsoft.com/en-us/graph/api/overview) <br>
- [Maton](https://maton.ai) <br>
- [ClawHub Skill Listing](https://clawhub.ai/byungkyu/microsoft-teams) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline HTTP routes, shell commands, and Python or JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include requests that read or modify Microsoft Teams resources; write actions require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
