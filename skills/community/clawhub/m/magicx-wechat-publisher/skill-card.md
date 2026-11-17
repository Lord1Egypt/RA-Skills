## Description:

Converts completed Markdown or text into WeChat public-account HTML, uploads images, and submits the result to the WeChat draft box without generating article content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youyouyoumagic](https://clawhub.ai/user/youyouyoumagic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents with access to a WeChat official account use this skill to prepare an already-written article for WeChat and submit it as a reviewable draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable WeChat official-account AppID/AppSecret credentials and can save them to a local config file.

Mitigation: Install only where that credential access is acceptable, protect the config file, avoid --save-config unless needed, never commit it, and rotate any secret exposed through local files or command history.

Risk: Article HTML and images are sent to WeChat/Tencent APIs during upload.

Mitigation: Review article content, images, account permissions, and destination account before running uploads.

Risk: Generated drafts may include maintainer branding in the footer or author fields.

Mitigation: Review the WeChat draft, especially footer and author fields, before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youyouyoumagic/skills/magicx-wechat-publisher)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline HTML and bash/Node.js commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat-compatible HTML and may submit drafts through WeChat/Tencent APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
