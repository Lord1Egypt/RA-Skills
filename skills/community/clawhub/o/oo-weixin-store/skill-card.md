## Description:

WeChat Store (channels.weixin.qq.com). Use this skill for ANY WeChat Store request — reading, creating, updating, and deleting data. Whenever a task involves WeChat Store, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External WeChat Store merchants use the skill to inspect shop data and manage products, orders, after-sales, fulfillment, and promotions through their connected account. It guides read operations and requests approval for state-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup may execute a changing online installer, and external installer and connector behavior is unverified.

Mitigation: Review the installation step, prefer a reviewed and pinned CLI installation, require approval for software changes, and grant only the permissions needed.

Risk: Write actions change WeChat Store data; some actions can be destructive or have external effects.

Mitigation: Confirm the exact action, target, payload, and effect with the user before writes; obtain explicit approval before destructive actions or external invitations.

## Reference(s):

- [WeChat Store API documentation](https://developers.weixin.qq.com/doc/store/API/basics/getaccesstoken.html)
- [WeChat Store](https://channels.weixin.qq.com/shop)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON connector responses with concise operational guidance and oo CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-specific store data or operation results; some actions change store state.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
