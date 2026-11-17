## Description:

Multi-channel mortgage marketing campaign engine - one brief generates email, social, ad, and listing copy with audience segmentation, A/B variants, and inline compliance flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

Mortgage marketing professionals and agents use this skill to turn a campaign brief into coordinated email, social, ad, and listing copy for selected borrower segments. It also provides A/B variant guidance and compliance-oriented flags for claims that require review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated mortgage marketing copy can contain compliance-sensitive claims, urgency framing, or borrower qualification language.

Mitigation: Review all generated copy against applicable advertising, fair-lending, NMLS, state, and platform requirements; treat the skill's compliance flags as prompts for review, not legal approval.

Risk: The release requires an Anthropic API key and installs an unpinned npm package.

Mitigation: Install only in environments where sharing an Anthropic API key is acceptable, and review or pin the npm dependency according to local dependency-management policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/drivenautoplex1/skills/mortgage-marketing)
- [Publisher Profile](https://clawhub.ai/user/drivenautoplex1)
- [OpenClaw Skills Repository](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON campaign copy organized by channel, platform, audience segment, A/B variant, and compliance flag.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include email subjects and bodies, social posts, ad hooks, listing copy, audience segment notes, A/B testing notes, and compliance review flags.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
