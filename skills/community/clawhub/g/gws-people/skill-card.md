## Description: <br>
Google People: Manage contacts and profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and run Google People CLI commands for contacts, contact groups, other contacts, directory profiles, and contact photos through an authenticated gws installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify real Google People contact data through the authenticated gws CLI. <br>
Mitigation: Verify the active Google account and shared gws auth rules before use, and require explicit approval before create, update, delete, batch, photo, or contact-group mutations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-people) <br>
- [Google API error details](https://cloud.google.com/apis/design/errors#error_info) <br>
- [Search other contacts](https://developers.google.com/people/v1/other-contacts#search_the_users_other_contacts) <br>
- [Search contacts](https://developers.google.com/people/v1/contacts#search_the_users_contacts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and authenticated Google People access.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
