## Description:

该技能使用 AI Hive Seedance 2.5 将 PixVerse/PixVerse AI 常见社媒特效短片工作流迁移为可审的动作、转场和视频编辑方案，并明确不复制 PixVerse 模板或表示官方合作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers can use this skill to turn PixVerse-style social video requests into auditable Seedance 2.5 prompts and CLI calls for text-to-video, image-start video, reference-paced video, video editing, and ending extension workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that downloaded output files could overwrite important files if an API response is compromised or malformed.

Mitigation: Run downloads in a dedicated non-sensitive output directory, avoid privileged or shared working folders, and use --no-download when reviewing task responses before retrieving generated media.

Risk: The skill requires an AI Hive API key for authenticated requests.

Mitigation: Use a scoped, replaceable API key, prefer environment-based configuration when possible, and rotate the key if it may have been exposed.

Risk: The workflow uploads user-provided media to AI Hive for video generation or editing.

Mitigation: Upload only media the user is authorized to process and retain source authorization records alongside the task ID and release ratio.

Risk: The artifact depends on a Python requests-based CLI.

Mitigation: Install dependencies in a virtual environment and review the skill before running it in production accounts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/pixverse-video-generation-alternative)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included CLI may submit AI Hive video jobs, print JSON task responses, and download generated media files to a configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
