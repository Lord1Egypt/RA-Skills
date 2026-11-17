## Description:

Creates and edits mobile-first advertising images with Nano Banana Pro via AI Hive, covering social feeds, product promotions, UGC-style stills, sale assets, resizing, and batch creative variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, designers, and developers use this skill to generate or edit brand-recognizable advertising images for mobile feeds, social ads, product cards, UGC-style stills, promotion layouts, and multi-placement resizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys are required for AI Hive calls and can be exposed if stored or shared carelessly.

Mitigation: Keep the API key private, prefer environment or local config storage with restricted file permissions, and avoid committing credentials.

Risk: Reference media is uploaded to AI Hive for generation or editing workflows.

Mitigation: Upload only media the user is comfortable sending to AI Hive and confirm the configured base URL is the intended endpoint.

Risk: The artifact installs the requests dependency without a pinned version.

Mitigation: Install in a virtual environment and review or pin the dependency before production use.

Risk: Generated files are downloaded and saved locally by default.

Mitigation: Use an appropriate output directory and review generated files before reuse or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-ad-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline bash commands; generated image files and task JSON from the AI Hive CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are saved locally by default, typically under ~/Downloads/AiHive unless an output directory is provided.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
