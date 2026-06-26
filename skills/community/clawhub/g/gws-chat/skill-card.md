## Description: <br>
Google Chat: Manage Chat spaces and messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent inspect and compose Google Chat CLI commands for managing spaces, messages, media, custom emojis, and related Chat resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward powerful Google Chat operations, including deleting spaces, changing memberships, uploading media, or using administrator-access options. <br>
Mitigation: Confirm the active Google account and scopes before use, and require explicit user approval before destructive, membership-changing, media-upload, or admin-access actions. <br>
Risk: The artifact depends on shared GWS authentication and security instructions that may be absent from the installed skill set. <br>
Mitigation: Review the shared GWS auth/security instructions before use; if they are missing, generate or install the shared GWS skill materials before executing Chat commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-chat) <br>
- [Upload media as a file attachment](https://developers.google.com/workspace/chat/upload-media-attachments) <br>
- [Create a space](https://developers.google.com/workspace/chat/create-spaces) <br>
- [Delete a space](https://developers.google.com/workspace/chat/delete-spaces) <br>
- [Search for and manage spaces](https://developers.google.com/workspace/chat/search-manage-admin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Google Workspace Chat operations through the gws CLI; user confirmation is appropriate for destructive or administrative actions.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
