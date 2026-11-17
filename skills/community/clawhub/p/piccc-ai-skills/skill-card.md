## Description:

Generate images, videos, and audio with Piccc AI (皮可AI), and query or download completed media tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoyaocz](https://clawhub.ai/user/xiaoyaocz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to authorize a Piccc AI account, discover available media models and voices, submit image, video, or audio generation tasks, and wait for or download completed outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Linking a Piccc AI account and storing a local API key can expose account tokens on shared or untrusted machines.

Mitigation: Install only from a reviewed source, keep the credentials file private, and run auth logout when finished on shared machines.

Risk: Custom Piccc AI API or authorization base URLs can redirect credential or task traffic outside the intended service.

Mitigation: Avoid setting PICCC_API_BASE_URL or PICCC_AUTH_BASE_URL outside controlled testing.

Risk: Generated media downloads may place files in user-selected locations.

Mitigation: Review output directories before downloading completed image, video, or audio results.

## Reference(s):

- [Piccc AI media API reference](references/api.md)
- [Piccc AI website](https://picccai.cn)
- [ClawHub skill page](https://clawhub.ai/xiaoyaocz/skills/piccc-ai-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown responses with shell commands and downloaded media files when tasks complete]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded image, video, or audio files after asynchronous Piccc AI tasks complete.]

## Skill Version(s):

0.1.4 (source: server release evidence; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
