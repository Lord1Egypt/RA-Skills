## Description: <br>
Provides Chatwork account access for reading, creating, updating, and deleting rooms, messages, contacts, and tasks through the OOMOL connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate Chatwork through an OOMOL-connected account for profile, contact, room, message, and task workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and modify data in the connected Chatwork account. <br>
Mitigation: Install it only when agent access to Chatwork is intended, and confirm the exact room, message, task, and payload before approving write or destructive actions. <br>
Risk: First-time setup may require installing the oo CLI. <br>
Mitigation: Run the installer only when needed and only if OOMOL's installer source is trusted. <br>


## Reference(s): <br>
- [ClawHub Chatwork skill page](https://clawhub.ai/oomol/oo-chatwork) <br>
- [Chatwork homepage](https://go.chatwork.com) <br>
- [oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent actions may return JSON from the oo CLI connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
