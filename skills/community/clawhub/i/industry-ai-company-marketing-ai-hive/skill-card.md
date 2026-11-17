## Description:

Helps AI company teams create fact-checked image, short-video, and content marketing plans with prompts, channel rewrites, AI-HIVE task records, and review gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, product teams, developers, and channel partners use this skill to plan AI-company image, video, and content marketing campaigns. It produces audience and value-proposition strategy, 30-day calendars, asset matrices, storyboards, prompts, platform rewrites, task records, and review criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys and uploaded campaign media could be exposed if the API endpoint is changed to an untrusted server.

Mitigation: Use the default AI-HIVE endpoint, avoid AI_HIVE_BASE_URL or --base-url unless the server is controlled and trusted, and use a limited API key.

Risk: Marketing outputs can misstate product capabilities, pricing, customer evidence, or platform constraints if source facts are not verified.

Mitigation: Require human review of facts, rights to reference media, model or price snapshots, and platform requirements before generation or publication.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API](https://ai-hive.iclip.cn/api)
- [AI公司图片视频内容营销行业手册](references/industry-playbook.md)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/industry-ai-company-marketing-ai-hive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and inline bash or Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create campaign brief JSON, AI-HIVE image or video task records, downloaded media, and deterministic edited video files when the user runs the included scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
