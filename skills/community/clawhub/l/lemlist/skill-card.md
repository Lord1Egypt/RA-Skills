## Description: <br>
Lemlist API integration with managed OAuth for managing campaigns, leads, activities, schedules, sequences, and unsubscribes in Lemlist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, sales operations teams, and developers use this skill to operate Lemlist outreach workflows through Maton-managed OAuth, including campaign, lead, schedule, activity, and unsubscribe management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and access to a connected Lemlist account. <br>
Mitigation: Keep MATON_API_KEY private and install only when Maton is trusted to broker access to the Lemlist account. <br>
Risk: Write and delete operations can change campaigns, leads, schedules, unsubscribes, or OAuth connections. <br>
Mitigation: Confirm the exact target resource and intended effect with the user before any create, update, pause, or delete request. <br>
Risk: Multiple Lemlist connections can cause requests to affect the wrong account. <br>
Mitigation: Use the Maton-Connection header when multiple active Lemlist connections exist. <br>


## Reference(s): <br>
- [Maton](https://maton.ai) <br>
- [Lemlist API Documentation](https://developer.lemlist.com/) <br>
- [Lemlist API Reference](https://developer.lemlist.com/api-reference) <br>
- [Lemlist Help Center - API](https://help.lemlist.com/en/collections/17109856-api-webhooks) <br>
- [ClawHub Lemlist Skill](https://clawhub.ai/byungkyu/lemlist) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with Python, JavaScript, HTTP, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a MATON_API_KEY credential, and explicit approval before write or delete API calls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
