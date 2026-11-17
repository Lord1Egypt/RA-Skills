## Description:

Katelynn Lead Gen helps agents find, qualify, profile, and draft multi-channel outreach for prospective customers based on a user's target customer profile and value proposition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dirtonyou](https://clawhub.ai/user/dirtonyou)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, marketing, and business development users use this skill to turn an ICP, value proposition, outreach goal, and channel choice into qualified prospect records, personalized outreach drafts, and a run summary. It is intended for permission-aware lead research and human-reviewed outreach workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collects and outputs personal business contact data such as names, titles, emails, phone numbers, LinkedIn profiles, and research hooks.

Mitigation: Use it only for lawful, permission-aware prospecting; limit exports to necessary business data and review records before storage or sharing.

Risk: The skill can draft or route outbound actions through email, SMS alerts, and phone transfer workflows.

Mitigation: Require explicit human confirmation before any outreach, SMS alert, phone transfer, or follow-up action is sent or initiated.

Risk: The skill uses a cross-run learned-rules file that could retain sensitive prospect or customer details.

Mitigation: Store only generalized failure patterns in learned-rules.md and remove personal, confidential, or unnecessary prospect details.

## Reference(s):

- [ICP Research Tactics](references/icp-research.md)
- [Outreach Copywriting Guide](references/copywriting.md)
- [Learned Failure Rules](references/learned-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/dirtonyou/skills/katelynn-lead-gen)
- [Publisher Profile](https://clawhub.ai/user/dirtonyou)
- [Publisher Homepage](https://gerika.ai)
- [Source Repository Metadata Link](https://gitlab.com/gerika-ai/agentic-ai-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or CSV lead tables, personalized outreach drafts, call scripts, SMS alert templates, and run summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain business contact data and should be reviewed before export, outreach, SMS alerts, or phone transfer.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
