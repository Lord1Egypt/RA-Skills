## Description:

OpenLX 微信公众号免白名单发布 routes prepared WeChat Official Account draft, publish, status, and media-upload requests through OpenLX after administrator QR authorization, without writing, editing, or generating content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlxcn](https://clawhub.ai/user/openlxcn)

### License/Terms of Use:

MIT

## Use Case:

External developers, operators, and WeChat Official Account administrators use this skill to hand prepared article, image-post, authorized-reprint, media-upload, and status-check requests to OpenLX when changing client IPs would otherwise interrupt WeChat allowlist workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A scoped API key can authorize WeChat Official Account operations if exposed or used for the wrong account.

Mitigation: Keep OPENLX_WEIXIN_API_KEY scoped to the intended account, store it outside skill files and logs, and verify target_account and appid before each request.

Risk: Public publish requests can make content externally visible.

Mitigation: Create drafts by default, require an explicit current instruction and explicit_publication_confirmation=true for public publication, and query the original publish_id for status.

Risk: Ambiguous write outcomes can cause duplicate or unintended operations if retried blindly.

Mitigation: Do not automatically retry writes; report SUBMITTED_UNVERIFIED and query the original operation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/openlxcn/skills/openlx-weixin-baimindan)
- [OpenLX Skill Homepage](https://wx.openlx.cn/skills/openlx-weixin-baimindan)
- [Authorization](references/AUTHORIZATION.md)
- [Handoff Contract](references/HANDOFF_CONTRACT.md)
- [Security and Privacy](references/SECURITY_AND_PRIVACY.md)
- [Install](references/INSTALL.md)
- [Update](references/UPDATE.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON handoff requirements and shell command examples; gateway responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires prepared user content and OPENLX_WEIXIN_API_KEY; public publication requires explicit confirmation.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter, VERSION, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
