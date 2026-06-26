## Description: <br>
Backs up an agent workspace to a GitHub repository by guiding token discovery, repository setup, git commits, and pushes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to back up an agent workspace to a private GitHub repository after important memory, skill, or configuration changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential exposure while finding, storing, or embedding GitHub tokens. <br>
Mitigation: Use a secure credential helper or secret manager, avoid PATs in chat, plaintext files, or remote URLs, and prefer a fine-grained least-privilege token. <br>
Risk: Broad or silent workspace backups can upload sensitive files or configuration. <br>
Mitigation: Narrow the backup scope, use a dedicated private repository, keep visible backup logs, disable silent scheduled pushes by default, and review staged files before pushing. <br>


## Reference(s): <br>
- [ClawHub Git Backup page](https://clawhub.ai/netanel-abergel/git-backup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes git, curl, token handling, .gitignore, and cron examples; review commands and files before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
