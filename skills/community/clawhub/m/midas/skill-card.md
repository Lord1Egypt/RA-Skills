## Description:

Midas helps agents turn user-provided daily-life information streams into money-signal reports, opportunity rankings, deal analyses, and pattern matches against reference wealth playbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realteamprinz](https://clawhub.ai/user/realteamprinz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use Midas to analyze voluntarily provided or public daily-life inputs, surface monetization opportunities, and structure next-action recommendations or deal reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may provide broad private, workplace, or sensitive personal data while asking the skill to mine everyday information streams.

Mitigation: Use only sanitized, user-owned, public, or explicitly authorized inputs; avoid employer Slack exports, DMs, raw browsing history, receipts, photos with people or locations, secrets, customer data, and confidential business details.

Risk: The self-learning workflow can encourage retained cumulative logs of prior inputs and opportunity profiles.

Mitigation: Disable or avoid evolution logs unless retained state is intentional, and delete prior inputs, generated logs, and derived examples after use.

Risk: Monetization and deal recommendations may be mistaken for financial, legal, tax, or investment advice.

Mitigation: Treat outputs as brainstorming and analysis only; independently validate assumptions and consult qualified professionals before acting on financial, legal, tax, or investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realteamprinz/skills/midas)
- [Signal Extraction Framework](references/signal-extraction-framework.md)
- [Noise-to-Gold Pipeline](references/noise-to-gold-pipeline.md)
- [Deal Analysis Template](references/deal-template.md)
- [Sources Guide](references/sources-guide.md)
- [Famous Wealth Operating Systems](references/famous-models/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports with optional JSON evolution log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores, ranked opportunities, deal analysis fields, and next-action recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
