## Description:

Turns livestream replay clipping requests into reviewable highlight timecodes, clip scripts, subtitle points, cover concepts, vertical video commands, and delivery checklists for ecommerce and marketing teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Livestream ecommerce operators, host teams, brand store teams, and knowledge livestream teams use this skill to identify independently understandable replay highlights and turn them into short-form production plans. It can also provide deterministic video-editing commands and AI-HIVE generation commands when authorized media and API credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload user-selected media to AI-HIVE and can submit potentially billable remote video generation tasks.

Mitigation: Confirm media authorization, final prompts, routing mode, model choice, and budget before running generation commands; start with a small sample for batch work.

Risk: The bundled API client is broader than the narrow livestream-clipping workflow and includes account, upload, chat, image, video, task, and download operations.

Mitigation: Review each command before execution and limit credentials to the intended AI-HIVE workflow and environment.

Risk: API keys could be exposed if pasted into commands, logs, screenshots, or committed configuration files.

Mitigation: Prefer the AI_HIVE_API_KEY environment variable or an approved secret store, and avoid sharing generated config files or terminal logs that include credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/livestream-highlight-clips-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON, ffmpeg command plans, AI-HIVE task identifiers, downloaded media file paths, and acceptance checklists when the user runs the bundled commands.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
