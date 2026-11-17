## Description:

Security audit for multi-tenant OpenClaw Telegram bots that checks workspace isolation, filesystem sandboxing, session scoping, auth separation, error leaking, and other multi-user security concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill before launching or updating public OpenClaw Telegram bots that serve multiple users. It guides audits for cross-user data leakage, session isolation, sandboxing, credential separation, safe error handling, and related multi-tenant controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared auth-profile copying could expose bot credentials across users in a public multi-user deployment.

Mitigation: Use separate credentials per trust boundary and review any credential-copying workflow before installation or deployment.

Risk: An unsandboxed fallback can leave shell commands able to access files outside a user's workspace.

Mitigation: Use enforced sandboxing or separate hosts for mixed-trust users, and do not rely on workspace-only filesystem controls as the sole boundary.

Risk: Keyword-count checks can miss real security regressions.

Mitigation: Run behavioral tests that attempt cross-user reads, prompt leaks, path traversal, and unsafe error disclosure.

## Reference(s):

- [OpenClaw Gateway Security](https://docs.openclaw.ai/gateway/security)
- [Canlah AI](https://canlah.ai)
- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-openclaw-multibot-audit)
- [ClawHub Publisher Profile](https://clawhub.ai/user/phy041)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown checklist with inline JSON, Python, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pass/fail audit items and a quick audit command for selected OpenClaw bot files.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
