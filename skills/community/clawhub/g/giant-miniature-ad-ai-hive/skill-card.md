## Description:

把巨物与微缩奇观广告需求变成可审查的中文制作蓝图、分镜脚本、提示词、AI-HIVE 视频任务和验收清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand creative, ecommerce, marketing, short-form video, and social media teams use this skill to turn product and campaign inputs into giant-object or miniature-world advertising concepts, shot plans, prompts, runnable AI-HIVE commands, task records, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles AI-HIVE API keys and may persist them in a local configuration file.

Mitigation: Use revocable or limited API keys where possible, prefer environment variables for temporary use, inspect ~/.ai-hive/config.json before reuse, and avoid committing logs, screenshots, or files that expose secrets.

Risk: The skill can upload user media to AI-HIVE and download generated results.

Mitigation: Upload only media the user is authorized to share with the service, and avoid sensitive, private, or regulated content unless the user has confirmed the permitted workflow.

Risk: Custom AI_HIVE_BASE_URL or --base-url values can redirect API requests away from the default service endpoint.

Mitigation: Use the default AI-HIVE endpoint unless the alternate endpoint is explicitly trusted and reviewed.

Risk: Generation calls can incur cost and repeated submissions can duplicate charges.

Mitigation: Show final prompts, model mode, routing mode, and price snapshot before execution; run a small sample before batch work and keep task records for deduplication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/giant-miniature-ad-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown with inline shell commands, optional JSON files, and downloaded media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE image or video generation tasks and download resulting media after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
