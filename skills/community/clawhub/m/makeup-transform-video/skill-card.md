## Description:

生成拟人动物化妆变身短视频，帮助用户用一句话创建素颜到精致妆容的快节奏反差视频。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to prepare and run WeryAI video-generation prompts for anthropomorphic animal makeup transformation clips and detailed makeup-step videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled helper can perform broader WeryAI video-generation actions than the makeup-specific workflow describes.

Mitigation: Review generated prompts and JSON parameters before execution, and restrict use to the intended makeup transformation or makeup-step workflows.

Risk: The skill sends prompts and optional image URLs to WeryAI remote endpoints using WERYAI_API_KEY.

Mitigation: Use a scoped API key where possible, avoid sensitive prompts or private image URLs, and confirm that remote processing is acceptable for the intended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/makeup-transform-video)
- [WeryAI Video API](https://api.weryai.com)
- [WeryAI Models API](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON parameters and Node.js shell commands; the helper script returns JSON status and video URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and WERYAI_API_KEY; can submit, poll, check status, list models, or dry-run WeryAI video requests.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
