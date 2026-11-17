## Description:

多轮商务谈判虾 helps procurement teams send supplier inquiry emails, parse replies, run up to three negotiation rounds, and summarize final quotes and terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement employees and business operators use this skill to coordinate bulk supplier inquiries, negotiate pricing or terms by email, compare returned quotes, and prepare a recommended supplier choice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk outbound negotiation emails can affect supplier relationships or send incorrect proposals at scale.

Mitigation: Require explicit human approval before bulk sends and use a dedicated procurement mailbox.

Risk: Mailbox access and generated reports can expose supplier communications or pricing data.

Mitigation: Avoid general-purpose inboxes and keep generated reports out of shared or source-controlled folders.

Risk: The security review reports unsafe script patterns around configuration loading and generated Python snippets.

Mitigation: Review and harden the script before real credential use, including replacing sourced config and heredoc generation with safer data-only parsing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/negotiation-bot-claw)
- [Negotiation Scripts](references/negotiation-scripts.md)
- [Price Benchmarks](references/price-benchmarks.md)
- [Supplier Profiles](references/supplier-profiles.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash command examples, plain-text email templates, and CSV quote reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMTP/IMAP configuration before email sending or inbox parsing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
