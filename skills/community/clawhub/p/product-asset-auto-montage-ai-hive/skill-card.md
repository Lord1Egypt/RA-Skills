## Description:

Turns product asset library auto-montage requests into a production workflow for SKU-based media indexing, shot labeling, edit decisions, AI-HIVE generation commands, deterministic ffmpeg edits, and reviewable deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, e-commerce operators, content teams, agency editors, and developers use this skill to turn authorized product media, SKU data, brand constraints, platform requirements, and budget goals into traceable short-video montage plans and runnable AI-HIVE or ffmpeg commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images, videos, audio, or references may be uploaded to AI-HIVE during generation or media upload commands.

Mitigation: Use only media you are authorized to upload and publish; review each prompt, route, and file path before running upload or generation commands.

Risk: AI-HIVE generation calls may be billable.

Mitigation: Confirm model, routing mode, prompt, pricing snapshot, and batch scope before submitting tasks; run a small sample before batch generation.

Risk: API keys could be exposed through logs, repositories, screenshots, or copied commands.

Mitigation: Use the documented placeholder in examples, store real keys only in the environment or local config, and avoid committing or sharing generated configuration files.

Risk: Generated product claims, prices, availability, model capabilities, or platform assumptions may be inaccurate or stale.

Mitigation: Mark unverified facts for review and validate product, price, inventory, platform, and model-availability claims against authoritative sources before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-asset-auto-montage-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sections, JSON artifacts, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local blueprint JSON, ffmpeg command plans, AI-HIVE task records, downloaded media paths, and review checklists.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
