## Description:

Investment Buddy Pet helps agents provide pet-persona investment companionship, personality matching, recurring reminders, market-volatility reassurance, and investor education while avoiding product recommendations and return promises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to match a user with an investment companion persona, provide investment education and reminders, and respond to market anxiety with compliant, non-advisory language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive investment profile, holdings, or preference data.

Mitigation: Review data handling before installation and avoid entering real holdings or sensitive financial details unless local storage, logging, sync, notification, and personalization controls are understood.

Risk: Proactive reminders and market responses could be mistaken for investment advice.

Mitigation: Treat outputs as education only, keep risk disclaimers visible, and prevent specific product recommendations, return promises, or urgent buy/sell instructions.

Risk: Cross-skill analysis flows can expand the advice surface.

Mitigation: Require explicit user consent before invoking related skills and restate that downstream analysis is reference material, not an investment decision.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lj22503/skills/investment-buddy-pet)
- [Compliance Rules](references/compliance-rules.md)
- [Pet Configurations](references/pet-configs.md)
- [Conversation Templates](references/conversation-templates.md)
- [Compliance Design](docs/COMPLIANCE_DESIGN.md)
- [Data API Specification](docs/DATA_API_SPEC.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples, code snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should remain educational and include risk framing for finance-related responses.]

## Skill Version(s):

1.1.4 (source: ClawHub server release evidence; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
