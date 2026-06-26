## Description: <br>
Use this skill for MailerLite requests involving reading, creating, updating, and deleting data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage MailerLite subscribers, groups, fields, and group membership through an OOMOL-connected MailerLite account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change MailerLite account state, including creating, updating, assigning, removing, or deleting subscribers and groups. <br>
Mitigation: Confirm the exact action, payload, and subscriber or group target before approving write or destructive commands. <br>
Risk: The skill requires a trusted OOMOL connection to a MailerLite account. <br>
Mitigation: Only complete the oo CLI and OOMOL connection flow for accounts the user intends to let the agent manage. <br>


## Reference(s): <br>
- [MailerLite homepage](https://www.mailerlite.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands return JSON data and execution metadata from the MailerLite connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
