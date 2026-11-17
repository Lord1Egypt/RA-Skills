## Description:

LocalMiniDrama 本地短剧助手通过自然语言控制短剧项目全流程，包括剧本、角色、场景、道具、分镜、图片、视频、剧集合成、小说导入和工程导入导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuanyustudio](https://clawhub.ai/user/xuanyustudio)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to operate a LocalMiniDrama backend from an agent conversation, generating and managing short-drama projects from story setup through storyboard, image/video generation, composition, and project import/export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and private project content may be sent to the configured backend over plain HTTP.

Mitigation: Use only a backend you control, prefer HTTPS for any non-local backend, and avoid entering high-value API keys over plain HTTP.

Risk: Powerful actions such as delete, import/export, upload, bulk generation, and key updates may affect the wrong project if context is stale or ambiguous.

Mitigation: Confirm the exact project, episode, and requested action before delete, import/export, upload, bulk generation, or key-update operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuanyustudio/skills/local-mini-drama)
- [Publisher profile](https://clawhub.ai/user/xuanyustudio)
- [Project homepage](https://github.com/xuanyustudio/LocalMiniDrama)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint descriptions, JSON request examples, configuration commands, and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured backend URL and remembers current drama and episode identifiers during a session.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
