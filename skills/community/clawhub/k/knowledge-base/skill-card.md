## Description:

Ingests WeChat, WeChat Channels, Douyin, Xiaohongshu, official-account articles, and local files into a Tencent Docs knowledge base with an indexed smart sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to capture links or local files, download or parse supported social content, upload it to Tencent Docs, and append an index row for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command execution in agent.py could allow local command injection.

Mitigation: Avoid agent.py until shell=True command construction is fixed; run the skill only in a constrained environment with trusted links and files.

Risk: Content and metadata are uploaded to Tencent Docs/COS during normal operation.

Mitigation: Use least-privilege Tencent Docs authorization and confirm that each file or link is approved for upload before running the workflow.

Risk: WeChat Channels links are sent to an external parser endpoint.

Mitigation: Require explicit user consent before processing WeChat Channels links and disclose that the link is sent to the external parser service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hitjcl/skills/knowledge-base)
- [Tencent Docs](https://docs.qq.com)
- [Python](https://python.org)
- [WeChat Channels parser endpoint](https://sph.litao.workers.dev/api/fetch_video_profile)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, JSON parser results, and uploaded file or index records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload supported local files and link-derived media or articles to Tencent Docs/COS when user authorization and environment variables are configured.]

## Skill Version(s):

2.4.1 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
