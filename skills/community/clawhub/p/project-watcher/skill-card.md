## Description: <br>
项目规划与进度追踪。维护 roadmap，git commit 通知，远程部署感知，与飞书集成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[altaircardinal](https://clawhub.ai/user/altaircardinal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to create and maintain project roadmaps, track implementation progress, and keep roadmap entries aligned with work performed in a Git repository. It can also support Feishu commit notifications when the optional hook and credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional post-commit hook can persistently send repository, branch, commit hash, and commit message details to a configured Feishu recipient. <br>
Mitigation: Install the hook only in repositories where ongoing Feishu notifications are intended, and avoid enabling it where commit messages may include customer, incident, ticket, credential, or other sensitive information. <br>
Risk: Feishu credentials and recipient/project settings must be supplied or edited before use. <br>
Mitigation: Review and replace configs/feishu.json, configs/projects.yaml, recipient IDs, and related environment variables before installing or running the notification workflow. <br>


## Reference(s): <br>
- [Project Watcher on ClawHub](https://clawhub.ai/altaircardinal/project-watcher) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance, roadmap files, shell hook commands, JSON configuration, and Feishu interactive message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project.md and ROADMAP.md and may send commit metadata to Feishu when the optional hook is installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
