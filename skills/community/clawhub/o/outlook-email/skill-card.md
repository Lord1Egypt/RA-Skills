## Description: <br>
Microsoft Outlook/Live.com email client via Microsoft Graph API. List, search, read, send, and reply to emails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhiramee08b021](https://clawhub.ai/user/abhiramee08b021) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and technical users use this skill to configure and operate an Outlook/Live/Hotmail command-line email client for listing, searching, reading, sending, and replying to email through Microsoft Graph API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires mailbox access and depends on external CLI source that is not included in the package. <br>
Mitigation: Review the external CLI source before installing or granting Microsoft account access, and test first with a non-production mailbox. <br>
Risk: Send and reply actions can transmit email to real recipients. <br>
Mitigation: Confirm recipients and message bodies before any send or reply action. <br>
Risk: Local credentials and OAuth tokens may retain mailbox access after setup. <br>
Mitigation: Use a dedicated Azure app registration with the narrowest available permissions and revoke or delete stored tokens when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhiramee08b021/outlook-email) <br>
- [Project homepage](https://github.com/abhiramee08b021/outlook-cli) <br>
- [Azure Portal app registrations](https://portal.azure.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that access, send, or reply to email after Microsoft account authentication.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
