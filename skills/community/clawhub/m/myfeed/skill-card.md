## Description: <br>
Manage MyFeed things and groups via the MyFeed REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[l-fy](https://clawhub.ai/user/l-fy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can ask an agent to prepare MyFeed REST API commands for creating things, inviting friends or groups, listing groups, and setting reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A MyFeed API key gives the agent full access to the user's MyFeed account. <br>
Mitigation: Install only if the publisher is trusted, keep Myfeed_API_KEY secret, and avoid exposing it in logs, prompts, or shared transcripts. <br>
Risk: Create commands can send reminders or invites to groups and phone numbers. <br>
Mitigation: Confirm event descriptions, times, alarm settings, group IDs, and phone numbers before running any create command. <br>
Risk: Inviting contacts may affect other people. <br>
Mitigation: Only invite contacts where the user has appropriate permission and a clear reason to send the invitation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/l-fy/myfeed) <br>
- [MyFeed homepage](https://myfeed.life) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq and the Myfeed_API_KEY environment variable.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
