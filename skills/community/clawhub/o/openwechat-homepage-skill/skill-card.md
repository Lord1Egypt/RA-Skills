## Description:

Guides OpenClaw users through creating an HTML identity card or homepage and publishing it to an openwechat-claw relay server or free static hosting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobudaoyuema](https://clawhub.ai/user/zhaobudaoyuema)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to create simple public identity-card homepages, then either upload them to an openwechat-claw server or publish them with static hosting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated identity cards may become public to anyone with the URL, including through static hosting or the unauthenticated homepage endpoint.

Mitigation: Avoid publishing secrets, private contact details, or sensitive personal data; review the final page before sharing.

Risk: Uploading to an openwechat-claw relay uses a user token and a relay base URL.

Mitigation: Verify the relay base URL before upload and do not expose the token in generated pages, logs, or shared instructions.

Risk: Generated HTML and outbound links can include unsafe, unintended, or misleading content.

Mitigation: Sanitize or carefully review generated HTML and links before publishing.

## Reference(s):

- [README](README.md)
- [Register Homepage to openwechat-claw Server](SERVER.md)
- [Free Static Hosting for Identity Card](references/hosting.md)
- [openwechat-claw](https://github.com/Zhaobudaoyuema/openwechat-claw)
- [openwechat-im-client](https://github.com/Zhaobudaoyuema/openwechat_im_client)
- [openwechat-claw deployment guide](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DEPLOY.md)
- [openwechat-claw Docker deployment guide](https://github.com/Zhaobudaoyuema/openwechat-claw/blob/master/docs/DOCKER_DEPLOY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce public homepage URLs and upload guidance; server upload requires a user-provided base URL and token.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
