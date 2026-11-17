## Description:

Autonomously identifies trending X discussions and drafts or posts contextual affiliate replies using xAI (Grok), X OAuth 2.0, and ThumbGate rate, relevance, and sentiment gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorganapolsky](https://clawhub.ai/user/igorganapolsky)

### License/Terms of Use:

MIT-0

## Use Case:

External users and growth operators use this skill to monitor niche X discussions, generate contextual replies, and manage affiliate-link posting with configured safety gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous X posting and affiliate promotion can create spam, policy, or brand-safety risk.

Mitigation: Require explicit human approval before posts go live, keep ThumbGate enabled, and enforce the documented rate-limit, sentiment, relevance, duplicate-reply, and link-throttle checks.

Risk: The skill requires X OAuth credentials and an xAI API key.

Mitigation: Use least-privilege X credentials, store secrets securely, isolate the setup, and rotate credentials if behavior is unexpected.

Risk: Affiliate automation and sending X content to xAI may be under-disclosed to affected audiences.

Mitigation: Use clear affiliate and automation disclosure and maintain a privacy policy for X content processed by xAI.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/igorganapolsky/skills/grok-x-growth-agent)
- [Publisher profile](https://clawhub.ai/user/igorganapolsky)
- [Make.com](https://make.com)
- [ElevenLabs affiliates](https://elevenlabs.io/affiliates)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce drafted social replies and setup guidance; posting should remain gated by human approval and configured safety controls.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
