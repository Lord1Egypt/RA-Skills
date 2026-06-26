## Description: <br>
Access Pilt fundraising data -- investor matches, campaign stats, outreach events, and deck analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[babpilt](https://clawhub.ai/user/babpilt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and fundraising teams use this skill to let an agent retrieve account-scoped Pilt fundraising data, including investor matches, campaign statistics, outreach events, and deck analysis summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a personal Pilt API key to access account-scoped fundraising data. <br>
Mitigation: Keep PILT_API_KEY out of logs and chat transcripts, store it only in the agent's secret configuration, and revoke it from the Pilt dashboard if exposure is suspected. <br>
Risk: Returned investor matches, campaign statistics, outreach events, and deck analysis can contain sensitive fundraising information. <br>
Mitigation: Share outputs only with authorized users and avoid pasting full responses into public or untrusted workspaces. <br>
Risk: An agent could be prompted to send the API key or requests to an endpoint outside Pilt. <br>
Mitigation: Verify requests use only https://pilt.ai/api/v1/gateway before execution. <br>


## Reference(s): <br>
- [Pilt homepage](https://pilt.ai) <br>
- [Pilt API gateway endpoint](https://pilt.ai/api/v1/gateway) <br>
- [ClawHub skill page](https://clawhub.ai/babpilt/pilt) <br>
- [Publisher profile](https://clawhub.ai/user/babpilt) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with curl examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a PILT_API_KEY environment variable; API responses are account-scoped fundraising data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
