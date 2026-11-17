## Description:

Monitor library book availability and get notified when books become available for borrowing. Supports Shenzhen Library and extensible for other libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yszheda](https://clawhub.ai/user/yszheda)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to track books at Shenzhen Library, check availability, maintain a monitored book list, and receive notifications when monitored books become available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local shell commands and change the monitored book list.

Mitigation: Review generated commands before execution and use state-changing actions only with clear book IDs and explicit intent.

Risk: SMTP notification setup may place email credentials in config.yaml.

Mitigation: Use an app-specific SMTP password or environment-based secret and avoid storing a real account password directly in the configuration file.

Risk: Scheduled monitoring can run continuously and make repeated network requests to Shenzhen Library.

Mitigation: Set reasonable check intervals, stop the monitor when it is no longer needed, and follow the target library's acceptable-use expectations.

Risk: Installer and Python dependencies are not tightly pinned.

Mitigation: Pin installer and Python dependency versions before production use and review updates before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yszheda/skills/library-book-monitor)
- [Shenzhen Library](https://www.szlib.org.cn/)
- [Shenzhen Library OPAC](https://www.szlib.org.cn/opac/)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance, local JSON state]

**Output Format:** [Markdown and terminal text with command examples, configuration snippets, and local JSON book records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run continuously for scheduled monitoring and can send console or SMTP email notifications.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
