## Description:

Issue Request Manager helps create, classify, track, update, reply to, and close issue requests, with local persistence and optional WeChat/WeCom notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viv888-ai](https://clawhub.ai/user/viv888-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project managers, and support teams use this skill to manage issue request lifecycle tasks such as creation, tracking, assignment, comments, priority changes, and closure. Teams can optionally configure WeChat/WeCom notifications for issue events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Issue metadata may be sent to WeChat/WeCom when notification functions are enabled or called.

Mitigation: Restrict recipients and avoid sending notifications for issues that contain secrets, incident details, regulated data, or customer-sensitive information.

Risk: WeChat/WeCom CorpID, Secret, and AgentID values can expose notification infrastructure if stored in tracked configuration.

Mitigation: Keep secrets out of tracked config files; use environment variables or a secret manager and grant only the permissions needed for notification delivery.

Risk: Issue records may be persisted locally as JSON files by the database helper.

Mitigation: Store local issue data in an access-controlled location and avoid placing secrets or regulated information in issue titles, descriptions, labels, or comments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/viv888-ai/skills/issue-request-manager)
- [Publisher Profile](https://clawhub.ai/user/viv888-ai)
- [Skill Definition](artifact/SKILL.md)
- [Issue Request Manager README](artifact/README.md)
- [WeChat Notification Guide](artifact/NOTIFICATION_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance, Python snippets, issue dictionaries, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist issue records to local JSON files and may call WeChat/WeCom APIs when notification functions are configured and invoked.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
