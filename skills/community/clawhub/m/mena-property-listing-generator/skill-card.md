## Description:

AI-powered bilingual property listing generator for MENA real estate agents that turns basic property specs into SEO-optimized Arabic and English listings, social posts, and WhatsApp follow-up scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jzargona](https://clawhub.ai/user/jzargona)

### License/Terms of Use:

MIT-0

## Use Case:

External real estate agents, property managers, and sales teams in MENA use this skill to generate bilingual property listing copy, social media content, and WhatsApp lead follow-up scripts from basic property specs.

### Deployment Geography for Use:

Middle East and North Africa (MENA)

## Known Risks and Mitigations:

Risk: The skill sends property details and agent contact details to a remote LLM service for generation.

Mitigation: Review the skill before installing, avoid entering unnecessary personal data, and install it only if sending those details to the configured LLM service is acceptable.

Risk: Security evidence reports that listing data and a MiniMax API key may be sent to undeclared LLM hosts if the environment is configured that way.

Mitigation: Keep LLM_BASE_URL unset unless the routing behavior is understood, and use a restricted MiniMax API key.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jzargona/skills/mena-property-listing-generator)
- [Reference docs index](references/README.md)
- [Marketing copy](references/marketing.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Markdown and plain text listing content with local JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated listings, agent profiles, and monthly counters under ~/.openclaw/mena-property-listing-generator/.]

## Skill Version(s):

1.0.1 (source: frontmatter, release metadata, script __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
