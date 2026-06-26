## Description: <br>
Search and read Mailchimp Marketing API audiences, members, campaigns, content, and reports through a local MCP wrapper. Use when the user asks about Mailchimp marketing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to let an agent inspect Mailchimp account, audience, member, campaign, campaign content, and report data from a connected Mailchimp account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Mailchimp OAuth token and can read connected account data such as audiences, members, campaigns, campaign content, and reports. <br>
Mitigation: Use a Mailchimp grant with the narrowest available scopes and avoid passing unrelated sensitive content through the tools. <br>
Risk: The runtime depends on mcporter and uv-managed Python dependencies, and the artifact notes that mcporter installation may use an unpinned latest package. <br>
Mitigation: Pin mcporter and uv-managed dependency versions in environments with stricter supply-chain requirements. <br>


## Reference(s): <br>
- [mcporter](https://github.com/steipete/mcporter) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON responses from Mailchimp Marketing API tools, with brief agent guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Mailchimp data access; list-style tools bound requested limits to a maximum of 100 where implemented.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
