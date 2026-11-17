## Description:

WeChat Official Account (mp.weixin.qq.com). Use this skill for ANY WeChat Official Account request — reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Account owners and their agents use this skill to read and manage WeChat Official Account content, media, messages, and account metrics through OOMOL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute unverified remote code and may add agent skills without clearly describing those changes.

Mitigation: Review and approve CLI setup separately, prefer a verified pinned release, inspect added skills, and check how to disable automatic synchronization.

Risk: The connected service mediates account operations and holds credentials; publishing, messaging, and deletion can affect external users or account data.

Mitigation: Keep payload approval enabled for publishing, messaging, and deletion, and confirm the intended action and target before approving.

## Reference(s):

- [WeChat Official Account homepage](https://mp.weixin.qq.com/)
- [WeChat Official Account API documentation](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Structured connector responses with text summaries and JSON action payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read account data or change account state; publishing, messaging, and deletion require user approval under the skill instructions.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
