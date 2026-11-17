## Description:

End-to-end Meta advertising system orchestrator for strategy research, creative generation, campaign delivery, and post-campaign optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanbowai](https://clawhub.ai/user/lanbowai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and agency operators use this skill to plan, create, launch, monitor, and optimize Meta advertising campaigns across the full ad lifecycle.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent and the lanbow-ads CLI authority over Meta ad accounts.

Mitigation: Use platform secret fields or environment variables, provide least-privilege short-lived tokens, start with a test ad account and small budgets, and revoke credentials after use.

Risk: The release depends on installing a global lanbow-ads CLI package that the security evidence describes as unpinned.

Mitigation: Pin and verify the CLI package before use, and only run it in a trusted runtime.

Risk: Generated campaign recommendations or delivery commands could spend budget or publish unintended ads.

Mitigation: Create campaigns in paused status where supported, review campaign settings before activation, and require human approval for budget or status changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lanbowai/skills/lanbow-claw-skill)
- [Lanbow Homepage](https://lanbow.com/)
- [Lanbow Claw Skill Guide](https://lanbow.com/blog/lanbow-claw-skill)
- [lanbow-ads npm Package](https://www.npmjs.com/package/lanbow-ads)
- [Meta Graph API Explorer](https://developers.facebook.com/tools/explorer/)
- [Meta Developer Apps](https://developers.facebook.com/apps/)
- [Meta Ads Manager](https://adsmanager.facebook.com/)
- [Meta Business Settings](https://business.facebook.com/settings/)
- [Ad Delivery](references/ad-delivery.md)
- [Ad Delivery Commands](references/ad-delivery-commands.md)
- [Creative Generation](references/creative-generation.md)
- [Meta Account Setup](references/meta-account-setup.md)
- [Post-Campaign Review](references/post-campaign-review.md)
- [Strategy Research](references/strategy-research.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with JSON artifacts, shell command blocks, and generated image files when creative generation is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May configure and invoke the lanbow-ads CLI; creative generation can produce PNG image files and proposal JSON.]

## Skill Version(s):

1.0.5 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
