## Description:

Helps Chinese video creators, social media operators, and ecommerce advertising teams turn MiniMax H3 video requests into production plans, prompts, AI-HIVE video tasks, runnable commands, and quality checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to plan and execute MiniMax H3 text-to-video, image-to-video, and reference-to-video workflows for ecommerce, advertising, social media, short drama, and promotional content. It produces reviewable Chinese production guidance before submitting any potentially paid AI-HIVE generation task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can read local media selected by the user and upload it to AI-HIVE for video generation.

Mitigation: Use only media the user is authorized to process, keep original files, and review prompts and assets before submission.

Risk: The workflow may create paid generation tasks.

Mitigation: Confirm final parameters, routing, and budget before generation; use small samples before batch runs.

Risk: API keys may be stored locally or sent to a configurable API endpoint.

Mitigation: Prefer session-scoped AI_HIVE_API_KEY use, use custom base URLs only when trusted, avoid logging secrets, and rotate keys after possible exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/minimax-h3-video-toolkit-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production blueprints, storyboards, prompt sets, task records, downloaded file paths, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
