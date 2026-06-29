## Description: <br>
Mybooks helps agents manage a MyBooks/Talebook personal library by searching and browsing books, retrieving details and statistics, editing metadata, uploading or adding books, and sending books to email or reader devices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poxenstudio](https://clawhub.ai/user/poxenstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a configured MyBooks server use this skill to operate a personal library through agent-issued API calls, including querying library and reading statistics, managing metadata and reading state, uploading books, and sending books to devices or email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files to the configured MyBooks server. <br>
Mitigation: Use least-privileged MyBooks credentials and confirm exact local file paths before permitting upload actions. <br>
Risk: The skill can send books to user-supplied email addresses or reader device destinations. <br>
Mitigation: Supervise transfer requests and verify destination email addresses, device types, and device URLs before execution. <br>
Risk: The skill requires stored MyBooks credentials that may allow library changes. <br>
Mitigation: Provide credentials through session-scoped environment variables or a dedicated secret manager, and avoid shared global configuration files. <br>


## Reference(s): <br>
- [MyBooks Homepage](https://www.mybooks.top) <br>
- [ClawHub Mybooks Skill Page](https://clawhub.ai/poxenstudio/skills/mybooks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and the MYBOOKS_HOST, MYBOOKS_USER, and MYBOOKS_PASSWORD environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
