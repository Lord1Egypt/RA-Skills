## Description:

Happy Horse 视频工具箱｜AI-HIVE helps creators and commercial teams turn Happy Horse video requests into T2V, I2V, and R2V mode recommendations, prompts, executable AI-HIVE tasks, and delivery checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketing teams, and commerce teams use this skill to plan and run AI-HIVE video generation or editing workflows for ads, social posts, short dramas, product content, and seeding campaigns. It produces reviewable plans before any potentially billable generation task is submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys.

Mitigation: Use scoped and revocable keys, keep them out of logs and shared files, and review configuration before running commands.

Risk: The skill can submit billable generation tasks.

Mitigation: Confirm prompts, model routing, and pricing snapshots before generation, and start with a small sample for batch work.

Risk: Downloaded outputs may overwrite or clutter local files.

Mitigation: Choose an explicit output directory where accidental overwrites will not damage important files.

Risk: Changing the API base URL can redirect requests away from the expected AI-HIVE service.

Mitigation: Use the default AI-HIVE endpoint or only a trusted endpoint, and avoid taking AI_HIVE_BASE_URL values from untrusted instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/happy-horse-video-toolkit-ai-hive)
- [Publisher Profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON records and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production blueprints, storyboard prompts, AI-HIVE task records, downloaded file paths, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
