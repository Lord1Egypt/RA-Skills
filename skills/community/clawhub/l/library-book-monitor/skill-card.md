## Description: <br>
Monitor library book availability and get notified when books become available for borrowing. Supports Shenzhen Library and extensible for other libraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yszheda](https://clawhub.ai/user/yszheda) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to track books at Shenzhen Library, check whether copies are available for borrowing, and receive notifications when monitored books become available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores monitored book data on disk. <br>
Mitigation: Use a private working directory and restrictive permissions for local data and configuration files. <br>
Risk: The skill contacts Shenzhen Library for availability checks. <br>
Mitigation: Run scheduled monitoring only when ongoing checks are needed and use reasonable check intervals. <br>
Risk: Email notifications can require SMTP credentials in config.yaml. <br>
Mitigation: Use an app-specific email password and restrict permissions on config.yaml. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yszheda/library-book-monitor) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [Shenzhen Library OPAC](https://www.szlib.org.cn/opac/) <br>
- [Shenzhen Library API service](https://www.szlib.org.cn/api/opacservice) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local JSON configuration/data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write a local book list, read config.yaml, contact Shenzhen Library, and send console or SMTP notifications when configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter and package metadata list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
