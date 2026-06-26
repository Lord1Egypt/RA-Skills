## Description: <br>
Real-time world news briefings with AI-clustered events, topic classification, and geographic filtering. No API key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pranciskus](https://clawhub.ai/user/pranciskus) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch current news events from newsmcp.io, filter them by topic or geography, and present concise multi-story briefings with source links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News queries and filters are sent to the external newsmcp.io API. <br>
Mitigation: Avoid highly personal or identifying search terms when requesting news. <br>
Risk: News summaries and source aggregation can be incomplete or misleading for important events. <br>
Mitigation: Verify important news against trusted primary sources before relying on it. <br>


## Reference(s): <br>
- [newsmcp homepage](https://newsmcp.io) <br>
- [newsmcp API base](https://newsmcp.io/v1) <br>
- [ClawHub skill page](https://clawhub.ai/pranciskus/newsmcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown news briefings with source links and inline curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses newsmcp.io responses to summarize multiple events with time windows, source counts, topic tags, and geography tags.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
