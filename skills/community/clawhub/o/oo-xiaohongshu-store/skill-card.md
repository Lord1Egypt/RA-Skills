## Description:

Xiaohongshu Store (ark.xiaohongshu.com). Use this skill for ANY Xiaohongshu Store request — reading, creating, and updating data. Whenever a task involves Xiaohongshu Store, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External Xiaohongshu Store sellers and store operators can use an agent to read and manage product listings, inventory, orders, logistics, and after-sale records through their connected shop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup can execute a remote installer without a separate approval step.

Mitigation: Review and explicitly approve CLI installation before setup, preferably using a verified release; check whether setup installs or updates other agent skills.

Risk: Store operations may expose customer information or change shop data.

Mitigation: Connect only the intended shop, request customer information only when needed, and confirm the exact effect of each store change before running it.

## Reference(s):

- [Xiaohongshu Store](https://ark.xiaohongshu.com/)
- [Xiaohongshu API documentation](https://s.apifox.cn/apidoc/docs-site/1103512/doc-2810935)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured connector data with concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include store records and guidance for read or write actions; write actions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
