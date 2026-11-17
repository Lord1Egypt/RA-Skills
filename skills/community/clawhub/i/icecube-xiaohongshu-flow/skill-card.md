## Description:

IceCube Xiaohongshu Flow coordinates diary generation, content optimization, title and hashtag planning, and Xiaohongshu publishing through related skills and an MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, developers, and operators use this skill to plan, optimize, publish, and log Xiaohongshu posts based on IceCube diary content and related content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to run an unverified third-party Xiaohongshu MCP binary with access to a logged-in Xiaohongshu session.

Mitigation: Install only from a trusted source, pin and verify the binary before use, and run it only in an environment where the account access is acceptable.

Risk: A background local service remains available for posting while it is running.

Mitigation: Start the service only when needed, confirm the expected PID or port before use, and stop it immediately after the publishing session.

Risk: The workflow can publish posts, send private-message replies, write activity logs, and route followers toward WeChat or paid offerings.

Mitigation: Require manual review and approval before publishing, replying, recording account activity, or using monetization routing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ares521521-design/skills/icecube-xiaohongshu-flow)
- [ClawHub publisher profile](https://clawhub.ai/user/ares521521-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command blocks, workflow examples, content templates, publishing checklists, and logging templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates required skills: xiaohongshu-content, xiaohongshu-mcp-skill, icecube-diary, and icecube-content-factory; publishing requires a logged-in Xiaohongshu MCP service and at least one image.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
