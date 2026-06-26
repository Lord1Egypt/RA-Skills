## Description: <br>
Plan and manage events, including scheduling, invitations, and logistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workspace agents use this skill to coordinate event planning in Google Workspace, including calendar entries, invitations, event materials, announcements, and RSVP or logistics tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send emails, post Chat updates, upload Drive files, create attendee calendar events, and edit Sheets in a real Google Workspace account. <br>
Mitigation: Require the agent to show and get approval for recipients, attendee lists, message text, calendar details, Drive folders and sharing settings, Chat spaces, and Sheet targets before it sends, posts, uploads, invites, or appends anything. <br>
Risk: Event logistics actions may expose or modify business information across Google Workspace services. <br>
Mitigation: Install and run the skill only with appropriately scoped Workspace access, and review planned changes before applying them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/persona-event-coordinator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown instructions with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws command and Google Workspace utility skills for Calendar, Gmail, Drive, Chat, and Sheets.] <br>

## Skill Version(s): <br>
1.0.12 (source: ClawHub release evidence; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
