## Description:

Turns GPT Image 2 and Nano Banana image-generation API relay requests into production-ready AI-HIVE workflows, runnable commands, prompts, task tracking, and quality checks for ecommerce, advertising, marketing, and social content teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and ecommerce or media production teams use this skill to convert image and video generation requirements into AI-HIVE integration plans, commands, prompts, routing choices, and delivery checklists. It is intended for authorized commercial content workflows that need reviewable model selection, uploads, polling, downloads, and task records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key-bearing network code can send requests to a configurable base URL for a billable service.

Mitigation: Use only trusted AI-HIVE endpoints, do not set --base-url or AI_HIVE_BASE_URL unless the endpoint is fully trusted, and prefer a limited or disposable API key.

Risk: The skill can upload selected media, submit image or video generation jobs, poll tasks, and download results.

Mitigation: Confirm prompts, routing, budget, media authorization, and expected costs before execution; start with a small sample before batch work.

Risk: Generated ecommerce or marketing content may include unlicensed references, misleading claims, or unsupported performance promises.

Mitigation: Require human review of source rights, product facts, platform rules, and claim substantiation before publication.

## Reference(s):

- [AI-HIVE chat console](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-nano-banana-api-relay-ai-hive)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown with inline shell commands, code snippets, and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create JSON briefs and download generated media after user confirmation for billable AI-HIVE tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
