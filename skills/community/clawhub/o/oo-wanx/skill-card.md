## Description:

Use the oo CLI to access Wanx image generation and video generation actions through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to generate images, submit video generation tasks, and check their status through an OOMOL-connected Wanx account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a remote installer that can make lasting local changes.

Mitigation: Review the oo CLI installer separately and require approval before running it; keep the skill's payload-confirmation step because generation may consume account credit.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Wanx homepage](https://tongyi.aliyun.com/wanxiang/)
- [Aliyun text-to-image API documentation](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Shell commands, JSON payloads and responses, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action payloads should follow the live connector schema; generation may consume account credit.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
