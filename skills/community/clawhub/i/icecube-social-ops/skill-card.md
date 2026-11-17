## Description:

IceCube Social Ops manages login, publishing, engagement, and reporting workflows for X/Twitter and Xiaohongshu social accounts after one-time account authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

External social account operators use this skill to run scheduled publishing, engagement handling, login checks, and operational reporting for X/Twitter and Xiaohongshu accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad logged-in browser control over real social accounts.

Mitigation: Use a dedicated browser profile or isolated account, avoid normal browsing sessions, and avoid saving raw cookies unless the security impact is understood.

Risk: The artifact defaults to automatic public posting and message handling after one-time authorization.

Mitigation: Require manual approval for posts, replies, follows, and direct-message responses at first, then expand automation only after behavior is reviewed.

Risk: Engagement tracking and direct-message handling can capture private messages or personal data.

Mitigation: Avoid logging private messages unless users have consented and retention rules are defined.

Risk: Automated posting, replies, and follows can trigger platform policy, spam, or rate-limit issues.

Mitigation: Respect platform rules, keep conservative posting intervals, pause on rate limits, and review generated content for sensitive or prohibited terms.

## Reference(s):

- [ClawHub skill page for IceCube Social Ops](https://clawhub.ai/ares521521-design/skills/icecube-social-ops)
- [ares521521-design ClawHub publisher profile](https://clawhub.ai/user/ares521521-design)
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, operational checklists, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes posting schedules, approval posture, platform limits, and a daily social operations report structure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
