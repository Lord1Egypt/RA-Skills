## Description:

Helps ecommerce sellers, product operators, and short-video directors turn product-video needs into reviewable Chinese production briefs, storyboard scripts, voiceover copy, shot prompts, AI-HIVE generation commands, and acceptance checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce and marketing users use this skill to create product short-video plans, scripts, prompts, AI-HIVE task commands, and quality checks from confirmed product facts, audience, channel, duration, and style constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AI-HIVE API key and supports a configurable API base URL, which can expose credentials if directed to an untrusted server.

Mitigation: Use the default AI-HIVE API endpoint unless there is a trusted reason to change it, keep the API key low-privilege where possible, and avoid logging or sharing the key.

Risk: Image, video, or audio inputs selected for generation may be uploaded to AI-HIVE or to a returned storage endpoint.

Mitigation: Review local media before upload and use only materials the user is authorized to submit.

Risk: Video generation can incur paid API usage.

Mitigation: Confirm prompts, model mode, routing, and price snapshot before submitting generation jobs, and use small samples before batch runs.

Risk: Marketing scripts can contain unsupported product claims, copied reference content, or implied endorsements.

Mitigation: Ground claims in supplied facts, keep reference use structural rather than copied, and review the final script for platform, copyright, trademark, privacy, and authenticity constraints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-video-script-generator-ai-hive)
- [AI-HIVE chat entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production briefs, storyboard tables, prompts, AI-HIVE task records, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
