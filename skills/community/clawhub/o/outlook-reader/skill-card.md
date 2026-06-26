## Description: <br>
Searches a user's local Outlook mailbox for subject keywords and saves matching email attachments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[die0921](https://clawhub.ai/user/die0921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users with a configured Windows Outlook profile use this skill to have an agent search recent mail by subject keyword and download matching attachments for follow-up processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive mailbox content through the logged-in Outlook profile. <br>
Mitigation: Install only when this access is intentional, and keep searches limited to specific folders and keywords. <br>
Risk: Downloaded or extracted email attachments may be untrusted. <br>
Mitigation: Check filenames, paths, archive contents, and file types before opening or using saved attachments. <br>
Risk: Broad automation such as recurring checks or auto-forwarding financial email can expose sensitive information. <br>
Mitigation: Avoid the auto-forward and recurring cron examples unless they have been reviewed and tightly scoped. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/die0921/outlook-reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; script output is console text and saved attachment files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Windows Outlook profile and writes downloaded attachments to a configured directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
