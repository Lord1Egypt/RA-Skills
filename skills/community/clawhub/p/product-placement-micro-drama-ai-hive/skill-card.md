## Description:

Helps agents turn Chinese product-placement micro-drama requests into production briefs, story structure, scene and shot plans, prompts, runnable AI-HIVE commands, task records, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, ecommerce, short-drama, and content-agency users can use this skill to plan product-placement micro-dramas from product facts, audience, platform, budget, and brand constraints. Developers and operators can also use its scripts to create briefs, call AI-HIVE image or video generation APIs, process video with ffmpeg, and record generated task outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can store and use AI-HIVE API credentials locally.

Mitigation: Use a scoped and revocable API key, avoid placing credentials in prompts or committed files, and remove local credentials when the skill is no longer needed.

Risk: Credential-bearing requests can be sent to a configurable API endpoint.

Mitigation: Keep the default AI-HIVE endpoint unless the replacement endpoint is fully trusted, and review any base URL supplied by CLI arguments, environment variables, or local configuration.

Risk: Media generation calls may upload user-provided assets and incur cost.

Mitigation: Confirm asset rights, prompts, model choice, routing mode, and budget before running generation commands; use a small sample before batch generation.

Risk: Generated product-placement content may overstate claims, omit ad disclosure, or resemble protected source material too closely.

Mitigation: Require factual claim review, platform disclosure review, and originality checks before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-placement-micro-drama-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE default API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Chinese narrative planning sections, inline shell commands, JSON task records, and checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API task IDs, pricing snapshots, generated media file paths, and video processing commands when the user authorizes generation.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
