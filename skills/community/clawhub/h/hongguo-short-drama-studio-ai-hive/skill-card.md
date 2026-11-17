## Description:

Helps vertical short-drama and commerce content teams turn authorized concepts or scripts into episode hooks, character and scene boards, shot prompts, runnable AI-HIVE commands, and continuity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, scriptwriters, and short-video production teams use this skill to plan authorized vertical short-drama content for platforms such as Hongguo/Fanqie-style channels. It produces reviewable story structure, shot-level prompts, AI-HIVE generation commands, task records, and delivery checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE generate and upload commands can send user media to a remote service and consume quota or funds.

Mitigation: Review commands and final generation parameters before execution, use small samples before batch jobs, and keep task records for cost and retry auditing.

Risk: API keys or media may be exposed if users configure an untrusted endpoint or mishandle credentials.

Mitigation: Use only trusted AI_HIVE_BASE_URL or --base-url values, keep AI_HIVE_API_KEY scoped and private, and avoid storing real keys in prompts, logs, or committed files.

Risk: Short-drama adaptation work can create copyright, endorsement, product-claim, or platform-compliance issues.

Mitigation: Confirm rights and factual claims before generation; when rights are unclear, use only abstract structure guidance and create new characters, dialogue, scenes, and visuals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/hongguo-short-drama-studio-ai-hive)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON plans, prompt tables, bash commands, and local files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit asynchronous AI-HIVE image or video generation jobs and download generated media after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
