## Description: <br>
Official Lemlist API integration for sales automation and multichannel outreach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[micktaiwan](https://clawhub.ai/user/micktaiwan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and sales operations teams use this skill to guide agent interactions with the Lemlist API for campaigns, leads, outbound messages, webhooks, schedules, exports, enrichment, unsubscribes, and inbox workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to send outreach, start or pause campaigns, change lead and contact records, manage unsubscribes, export data, and create external webhooks. <br>
Mitigation: Use a dedicated or least-privilege Lemlist API key when possible and require explicit confirmation before sending messages, changing campaign or lead data, exporting data, changing unsubscribes, or creating webhooks. <br>
Risk: Actions may affect real customer or prospect data in a Lemlist account. <br>
Mitigation: Start with test campaigns and review proposed API calls, payloads, and target records before execution. <br>


## Reference(s): <br>
- [Lemlist API endpoint reference](references/api-endpoints.md) <br>
- [Official Lemlist API documentation](https://developer.lemlist.com/api-reference) <br>
- [Lemlist app API key settings](https://app.lemlist.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with API paths, JSON configuration, shell commands, and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LEMLIST_API_KEY and explicit review before account-changing or message-sending actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
