## Description:

Manage MyFeed things and groups via the MyFeed REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l-fy](https://clawhub.ai/user/l-fy)

### License/Terms of Use:


## Use Case:

External users use this skill to create MyFeed things, invite friends or groups, list groups, and configure reminders through the MyFeed REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real invitations and reminders to friends or groups.

Mitigation: Verify recipient phone numbers and group IDs before executing create_thing requests.

Risk: The API key provides access to the user's MyFeed account.

Mitigation: Store Myfeed_API_KEY securely and avoid exposing it in command history, logs, or shared transcripts.

## Reference(s):

- [MyFeed homepage](https://myfeed.life)
- [MyFeed skill API endpoint](https://skill.myfeed.life/api)
- [ClawHub skill page](https://clawhub.ai/l-fy/skills/myfeed)
- [Publisher profile](https://clawhub.ai/user/l-fy)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and the Myfeed_API_KEY environment variable.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
