## Description:

Google People: Manage contacts and profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect and run Google Workspace People API commands for contacts, contact groups, other contacts, directory people, and profile data through the gws CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to read, create, update, or delete Google contacts, contact groups, and contact photos through authenticated Google People access.

Mitigation: Require review of the exact contact, group, photo, fields, and command parameters before allowing write or delete operations.

Risk: Some People API mutation operations can fail or behave unexpectedly when sent concurrently for the same user.

Mitigation: Run mutating requests sequentially for a given user and inspect gws schema output before building command parameters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-people)
- [Google API error details](https://cloud.google.com/apis/design/errors#error_info)
- [Search other contacts](https://developers.google.com/people/v1/other-contacts#search_the_users_other_contacts)
- [Search contacts](https://developers.google.com/people/v1/contacts#search_the_users_contacts)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and CLI parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and authenticated Google People access; users should inspect method schemas before execution.]

## Skill Version(s):

1.0.13 (source: server-resolved release metadata; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
