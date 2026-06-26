## Description: <br>
NexLink connects Nextcloud, Microsoft Exchange, and YouTube so agents can work with email, calendars, tasks, contacts, files, document understanding, analytics, and transcript extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asistent-alex](https://clawhub.ai/user/asistent-alex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to manage Exchange mail, calendars, tasks, contacts, Nextcloud files, document workflows, and YouTube transcripts through a single agent interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make live changes to email, calendars, tasks, contacts, and files. <br>
Mitigation: Review commands before execution and require explicit human confirmation for mailbox switching, sending mail, public link creation, attachment downloads, and cross-user task actions. <br>
Risk: Broad Exchange delegate or impersonation permissions could expose or modify data across users. <br>
Mitigation: Use dedicated low-privilege service accounts and avoid broad delegate or impersonation rights. <br>
Risk: Disabling TLS verification can weaken transport security. <br>
Mitigation: Keep TLS verification enabled except for temporary, controlled exceptions. <br>
Risk: File sharing and attachment workflows may expose business data. <br>
Mitigation: Apply local allowlists and review public links, downloaded attachments, and file transfer destinations before execution. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/asistent-alex/nexlink) <br>
- [Publisher profile](https://clawhub.ai/user/asistent-alex) <br>
- [Project homepage](https://firmade.ai) <br>
- [Repository](https://github.com/asistent-alex/openclaw-nexlink) <br>
- [Setup guide](references/setup.md) <br>
- [Security best practices](references/security-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, JSON-like command results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger live Exchange, Nextcloud, or YouTube operations depending on the invoked command and configured credentials.] <br>

## Skill Version(s): <br>
0.15.9 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
