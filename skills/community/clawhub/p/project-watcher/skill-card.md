## Description:

Project Watcher helps agents plan projects, maintain roadmaps, track progress after project work, and send Feishu notifications for Git commits and deployment-aware project activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[altaircardinal](https://clawhub.ai/user/altaircardinal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create and maintain project roadmaps, connect work sessions to planned roadmap items, summarize project progress, and notify configured Feishu recipients after Git commits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send repository, branch, commit hash, and commit message metadata to a configured Feishu recipient.

Mitigation: Install the commit hook only for repositories that should send notifications, review commit messages and branch names for sensitive content, and remove the hook when automatic notifications are no longer desired.

Risk: Feishu credentials may be stored in configs/feishu.json if environment variables or a secret manager are not used.

Mitigation: Prefer FEISHU_APP_ID and FEISHU_APP_SECRET, another secret manager, or placeholder-only config files; avoid committing real app credentials.

Risk: The packaged project configuration includes fixed recipient, host, path, user, and SSH key examples that may not match the installing user's environment.

Mitigation: Replace the Feishu recipient and project or deployment settings with values under the user's control before enabling notifications or deployment-aware workflows.

## Reference(s):

- [Project Watcher release page](https://clawhub.ai/altaircardinal/skills/project-watcher)
- [Feishu Open APIs](https://open.feishu.cn/open-apis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, roadmap files, shell hook commands, Python notification calls, and JSON or YAML configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send commit metadata to Feishu when the post-commit hook and credentials are configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
