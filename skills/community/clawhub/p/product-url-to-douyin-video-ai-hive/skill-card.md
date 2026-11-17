## Description:

This skill helps Douyin, Taobao, JD, and short-video commerce teams turn product links or detail-page assets into a reviewable Chinese e-commerce video workflow, including product facts, hooks, narration scripts, shot plans, runnable AI-HIVE commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, marketing teams, and developers use this skill to structure product-link-to-Douyin video work into fact checks, content strategy, AI-HIVE image or video generation commands, local video edits, task records, and launch-ready review checklists. It is intended for authorized e-commerce materials and requires human confirmation before paid generation tasks are submitted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be sent to custom AI-HIVE base URLs if a user overrides the default endpoint.

Mitigation: Use only the official AI-HIVE endpoint unless the custom endpoint is fully trusted, and keep API keys scoped, revocable, and out of logs or committed files.

Risk: Generated task outputs can be downloaded to user-selected locations without strong path containment.

Mitigation: Run downloads into a disposable output directory and review generated files before moving them into shared or production locations.

Risk: Image and video generation may incur paid API usage if commands are run at scale or without review.

Mitigation: Review prompts, routing mode, model selection, and expected cost before execution; start with a small sample before batch generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/product-url-to-douyin-video-ai-hive)
- [AI-HIVE Chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files, download generated media outputs, and emit AI-HIVE task identifiers when generation commands are run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
