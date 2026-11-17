## Description:

旧广告智能改版｜AI-HIVE helps brands and merchants turn authorized legacy ad assets into refreshed platform-specific creative plans, editing commands, AI-HIVE generation tasks, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing teams, brands, merchants, and their agents use this skill to refresh authorized TVC, information-feed, product, ecommerce, and social video assets for new platforms, durations, formats, subtitles, hooks, and calls to action. It also supports deterministic local video edits and optional AI-HIVE API generation after review of prompts, routing, model configuration, pricing snapshots, and source-media authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE client can send API keys and selected media to a configured API endpoint.

Mitigation: Before use, confirm AI_HIVE_BASE_URL and ~/.ai-hive/config.json point to the intended AI-HIVE endpoint and rotate the API key if endpoint or config integrity is uncertain.

Risk: Refreshing old advertisements can reuse sensitive, unlicensed, outdated, or misleading brand and product assets.

Mitigation: Use only authorized source media, verify current product claims, pricing, platform rules, and brand approvals, and avoid uploading sensitive or unlicensed files.

Risk: Image or video generation may create paid AI-HIVE tasks.

Mitigation: Review prompts, model configuration, routing mode, pricing snapshot, and sample outputs before submitting billable or batch generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/old-ad-creative-refresh-ai-hive)
- [AI-HIVE web entry point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local ffmpeg commands, AI-HIVE API task records, media upload references, pricing snapshots, task IDs, generated file paths, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
